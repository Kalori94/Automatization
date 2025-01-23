import os
from PIL import Image

def main():
    respuesta = input("¿Quieres realizar la revisión de imágenes (.jpg)? (si/no): ").strip().lower()
    if respuesta != "si":
        print("¡Vuelve pronto!")
        return

    carpeta_usuario = input("¿Cómo se llama la carpeta en donde haré la revisión?: ").strip().lower()
    ruta_base = os.path.expanduser("~/Downloads")

    # Buscar carpeta que coincida parcialmente con el nombre ingresado
    carpeta_encontrada = None
    for root, dirs, _ in os.walk(ruta_base):
        for nombre_dir in dirs:
            if carpeta_usuario in nombre_dir.lower():
                carpeta_encontrada = os.path.join(root, nombre_dir)
                break
        if carpeta_encontrada:
            break

    if not carpeta_encontrada:
        print("No se encontró ninguna carpeta con ese nombre. ¡Vuelve pronto!")
        return

    # Buscar y redimensionar las imágenes en la carpeta
    imagenes_redimensionadas = 0

    for root, _, files in os.walk(carpeta_encontrada):
        for file in files:
            if file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                with Image.open(file_path) as img:
                    if os.path.getsize(file_path) > 1_000_000:  # Si la imagen pesa más de 1MB
                        img.save(file_path, quality=85)
                        while os.path.getsize(file_path) > 1_000_000 and img.size[0] > 100 and img.size[1] > 100:
                            img = img.resize((img.size[0] // 2, img.size[1] // 2), Image.Resampling.LANCZOS)
                            img.save(file_path, quality=85)
                        imagenes_redimensionadas += 1

    print(f"Las imágenes se han redimensionado. Total de imágenes redimensionadas: {imagenes_redimensionadas}")

if __name__ == "__main__":
    main()

