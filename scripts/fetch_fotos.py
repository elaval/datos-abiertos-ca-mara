import json
import requests
import os

# Ruta al archivo JSON
json_file_path = 'data/diputados.json'

# Carpeta para almacenar las imágenes descargadas
output_folder = 'data/diputados_imagenes'

# Crear la carpeta si no existe
os.makedirs(output_folder, exist_ok=True)

# Cargar los datos JSON
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Iterar sobre los diputados y descargar sus imágenes
for diputado in data['DiputadosColeccion']['Diputado']:
    diputado_id = diputado['Id']
    nombre = diputado['Nombre']
    apellido_paterno = diputado['ApellidoPaterno']
    apellido_materno = diputado.get('ApellidoMaterno', '')

    # URL de la imagen
    image_url = f"https://www.camara.cl/img.aspx?prmID=GRCL{diputado_id}"

    # Nombre del archivo de imagen
    image_filename = f"{nombre}_{apellido_paterno}_{apellido_materno}_{diputado_id}.jpg".replace(" ", "_")
    print(image_filename)
    image_path = os.path.join(output_folder, image_filename)

    # Descargar la imagen
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as img_file:
                img_file.write(response.content)
            print(f"Imagen de {nombre} {apellido_paterno} descargada correctamente.")
        else:
            print(f"Error al descargar la imagen de {nombre} {apellido_paterno}. Código de respuesta: {response.status_code}")
    except Exception as e:
        print(f"Error al descargar la imagen de {nombre} {apellido_paterno}: {e}")
