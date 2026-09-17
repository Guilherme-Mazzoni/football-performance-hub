import os
from rembg import remove
from PIL import Image
import glob

def process_photos():
    photos_dir = "assets/photos"
    extensions = ("*.jpg", "*.jpeg", "*.webp")
    files_to_process = []
    
    for ext in extensions:
        files_to_process.extend(glob.glob(os.path.join(photos_dir, ext)))
        
    for input_path in files_to_process:
        print(f"Processando imagem: {input_path}")
        try:
            # Pega o nome do arquivo sem extensão
            filename = os.path.basename(input_path)
            name_without_ext = os.path.splitext(filename)[0]
            output_path = os.path.join(photos_dir, f"{name_without_ext}.png")
            
            # Remove fundo
            input_image = Image.open(input_path)
            output_image = remove(input_image)
            
            # Salva como PNG transparente
            output_image.save(output_path, "PNG")
            
            # Deleta original
            input_image.close()
            os.remove(input_path)
            print(f"Sucesso! Salvo como {output_path}")
            
        except Exception as e:
            print(f"Erro ao processar {input_path}: {e}")

if __name__ == "__main__":
    process_photos()
