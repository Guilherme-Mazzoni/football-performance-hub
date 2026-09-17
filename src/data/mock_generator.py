import random
from datetime import date, timedelta
from src.data.database import init_db, SessionLocal, Jogador, Partida, Evento
from faker import Faker

fake = Faker('pt_BR')

POSICOES = ['Goleiro', 'Zagueiro', 'Lateral', 'Volante', 'Meio-Campo', 'Atacante']

def generate_mock_data():
    init_db()
    db = SessionLocal()

    # Verificar se já existem dados
    if db.query(Jogador).count() > 0:
        print("Dados já existem no banco. Pulando geração.")
        db.close()
        return

    print("Gerando elenco...")
    jogadores = []
    
    # Gerando Goleiros
    for _ in range(3):
        j = Jogador(nome=fake.name_male(), posicao='Goleiro', numero=random.randint(1, 99), idade=random.randint(18, 38))
        jogadores.append(j)
    
    # Gerando Linha
    for _ in range(25):
        j = Jogador(nome=fake.name_male(), posicao=random.choice(POSICOES[1:]), numero=random.randint(2, 99), idade=random.randint(18, 36))
        jogadores.append(j)
        
    db.add_all(jogadores)
    db.commit()

    print("Gerando partidas e eventos...")
    data_inicial = date(2023, 4, 15)
    
    for i in range(38): # 38 rodadas
        gols_pro = random.randint(0, 4)
        gols_contra = random.randint(0, 3)
        vitoria = gols_pro > gols_contra
        empate = gols_pro == gols_contra
        derrota = gols_pro < gols_contra
        
        partida = Partida(
            data=data_inicial + timedelta(days=i*7),
            adversario=fake.company(),
            local=random.choice(['Casa', 'Fora']),
            gols_pro=gols_pro,
            gols_contra=gols_contra,
            vitoria=vitoria,
            empate=empate,
            derrota=derrota
        )
        db.add(partida)
        db.commit()

        # Gerar eventos para a partida
        jogadores_disponiveis = db.query(Jogador).all()
        jogadores_em_campo = random.sample(jogadores_disponiveis, 14) # 11 + 3 substituições
        
        for jogador in jogadores_em_campo:
            jogador.minutos_jogados += random.randint(15, 90)
            
            # Chutes (maior probabilidade para atacantes e meias)
            num_chutes = random.randint(0, 4) if jogador.posicao in ['Atacante', 'Meio-Campo'] else random.randint(0, 1)
            for _ in range(num_chutes):
                is_gol = (random.random() < 0.15) # 15% de chance de gol
                xg = random.uniform(0.01, 0.45)
                # Coordenadas do ataque: x de 60 a 120 (campo de 120x80)
                x_coord = random.uniform(70.0, 120.0)
                y_coord = random.uniform(10.0, 70.0)
                
                db.add(Evento(
                    partida_id=partida.id,
                    jogador_id=jogador.id,
                    tipo='Gol' if is_gol else 'Chute',
                    minuto=random.randint(1, 90),
                    x=x_coord,
                    y=y_coord,
                    xg=xg,
                    sucesso=is_gol
                ))
            
            # Passes chave e assistências
            num_passes = random.randint(0, 5) if jogador.posicao in ['Meio-Campo', 'Lateral'] else random.randint(0, 2)
            for _ in range(num_passes):
                is_assist = (random.random() < 0.1)
                xa = random.uniform(0.01, 0.3)
                x_coord = random.uniform(40.0, 110.0)
                y_coord = random.uniform(0.0, 80.0)
                
                db.add(Evento(
                    partida_id=partida.id,
                    jogador_id=jogador.id,
                    tipo='Assistência' if is_assist else 'Passe Chave',
                    minuto=random.randint(1, 90),
                    x=x_coord,
                    y=y_coord,
                    xa=xa,
                    sucesso=True
                ))
                
            # Defesas do goleiro
            if jogador.posicao == 'Goleiro':
                for _ in range(random.randint(2, 8)):
                    db.add(Evento(
                        partida_id=partida.id,
                        jogador_id=jogador.id,
                        tipo='Defesa',
                        minuto=random.randint(1, 90),
                        sucesso=True
                    ))
                    
    db.commit()
    db.close()
    print("Dados fictícios gerados com sucesso!")

if __name__ == "__main__":
    generate_mock_data()
