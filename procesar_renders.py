import os
import zipfile
import shutil
from PIL import Image

# Directorios
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
output_folder = os.path.join(downloads_path, "Renders para pagina web")

# Crear carpeta de salida si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Función para descomprimir archivos zip
def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# Función para redimensionar y convertir imágenes
def process_images(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.png')):
                file_path = os.path.join(root, file)
                img = Image.open(file_path)
                
                # Redimensionar imagen a la mitad
                new_size = (img.width // 2, img.height // 2)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Convertir a JPG si es PNG
                if file.lower().endswith('.png'):
                    file = file.rsplit('.', 1)[0] + '.jpg'
                    img = img.convert('RGB')
                
                # Guardar imagen procesada en la carpeta de salida
                img.save(os.path.join(output_folder, file), 'JPEG')

# Buscar y procesar carpetas que contienen "Renders"
for root, dirs, files in os.walk(downloads_path):
    for dir_name in dirs:
        if "renders" in dir_name.lower():
            renders_folder = os.path.join(root, dir_name)
            print(f"Encontrada carpeta: {renders_folder}")
            
            # Verificar si la carpeta está comprimida y descomprimir
            if os.path.exists(renders_folder + ".zip"):
                print(f"Descomprimiendo: {renders_folder}.zip")
                unzip_file(renders_folder + ".zip", downloads_path)
            
            # Procesar imágenes en la carpeta "Renders"
            if os.path.exists(renders_folder):
                process_images(renders_folder, output_folder)
            else:
                print(f"No se encontró la carpeta '{dir_name}' después de descomprimir.")

print("Proceso completado.")


