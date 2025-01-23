import os
import zipfile
from PIL import Image
import logging
#Establece tu directorio donde está tu archivo
def search_render_directory(directory):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if "render" in dir_name.lower(): #esta es la palabra clave que tendrá el archivo, modifica a tus necesidades
                return os.path.join(root, dir_name)
        for file_name in files:
            if "render" in file_name.lower() and file_name.lower().endswith('.zip'):
                return os.path.join(root, file_name)
    return None
#Descomprimir carpeta zip
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to
#encontrar imágenes dentro de la carpeta
def find_images(directory):
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.png',".jpeg")): #ajusta aquí alguna otra extensión que necesites
                image_files.append(os.path.join(root, file))
    return image_files
#Redimensionar imagenes
def resize_image(image_path, output_path):
    with Image.open(image_path) as img:
        size = (int(img.width / 2), int(img.height / 2))
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path)
#Convertir imagenes a jpg
def convert_to_jpg(image_path, output_path):
    with Image.open(image_path) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output_path, 'JPEG')
#procesar las imagenes
def process_images(image_files, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    log_file = os.path.join(output_directory, 'error.log')
    logging.basicConfig(filename=log_file, level=logging.ERROR)
    
    for file in image_files:
        try:
            base, ext = os.path.splitext(file)
            output_file = os.path.join(output_directory, os.path.basename(base) + ".jpg")

            if ext.lower() == '.png':
                convert_to_jpg(file, output_file)
            else:
                resize_image(file, output_file)
        except Exception as e:
            logging.error(f"Failed to process {file}: {e}")
#Ejecutar el programa
def main():
    downloads_dir = os.path.expanduser("~/Downloads") #Cambia el nombre de la carpeta en donde esta el .zip o la carpeta a procesar
    render_path = search_render_directory(downloads_dir)
    
    if render_path:
        if render_path.lower().endswith('.zip'):
            extracted_dir = extract_zip(render_path, os.path.join(downloads_dir, "extracted"))
        else:
            extracted_dir = render_path

        image_files = find_images(extracted_dir)
        output_directory = os.path.join(downloads_dir, "img_procesadas")
        
        process_images(image_files, output_directory)
        
        print(f"Images processed and saved to {output_directory}")
    else:
        print("No directory or zip file found with 'render' in its name.")

if __name__ == "__main__":
    main()

