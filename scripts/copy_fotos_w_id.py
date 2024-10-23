import os
import shutil

# Carpeta original con las imágenes
source_folder = 'data/diputados_imagenes'

# Nueva carpeta donde se guardarán las imágenes renombradas
destination_folder = 'data/diputados_imagenes_id'

# Crear la nueva carpeta si no existe
os.makedirs(destination_folder, exist_ok=True)

# Recorrer los archivos en la carpeta original
for filename in os.listdir(source_folder):
    if filename.endswith('.jpg'):
        # Extraer el ID del diputado del nombre del archivo original
        parts = filename.split('_')
        diputado_id = parts[-1].split('.')[0]  # El ID es la última parte antes de la extensión
        
        # Crear el nuevo nombre de archivo solo con el ID
        new_filename = f"{diputado_id}.jpg"
        
        # Ruta completa del archivo original y del archivo nuevo
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, new_filename)
        
        # Copiar el archivo al nuevo destino con el nombre renombrado
        shutil.copy(source_path, destination_path)
        print(f"Imagen {filename} copiada como {new_filename}.")
