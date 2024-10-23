import json
import requests
import os
import time

# Ruta al archivo JSON
json_file_path = 'data/diputados.json'

# Carpeta para almacenar las imágenes descargadas
output_folder = 'data/diputados_imagenes'

# Crear la carpeta si no existe
os.makedirs(output_folder, exist_ok=True)

# Cargar los datos JSON
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Iterar sobre los diputados y descargar sus imágenes si no existen o son inválidas
for diputado in data['DiputadosColeccion']['Diputado']:
    diputado_id = diputado['Id']
    nombre = diputado['Nombre']
    apellido_paterno = diputado['ApellidoPaterno']
    apellido_materno = diputado.get('ApellidoMaterno', '')

    # Nombre del archivo de imagen
    image_filename = f"{nombre}_{apellido_paterno}_{apellido_materno}_{diputado_id}.jpg".replace(" ", "_")
    image_path = os.path.join(output_folder, image_filename)

    # Comprobar si el archivo ya existe y tiene un tamaño mayor a 0 bytes
    if os.path.exists(image_path) and os.path.getsize(image_path) > 0:
        print(f"Imagen de {nombre} {apellido_paterno} ya existe y es válida. Se omite la descarga.")
        continue

    # URL de la página de detalles del diputado
    details_url = f"https://www.camara.cl/diputados/detalle/pasajesaereos.aspx?prmId={diputado_id}"
    # URL de la imagen
    image_url = f"https://www.camara.cl/img.aspx?prmID=GRCL{diputado_id}"

    # Realizar una solicitud a la página de detalles para "cachear" la imagen
    try:
        response_details = requests.get(details_url)
        if response_details.status_code == 200:
            print(f"Página de {nombre} {apellido_paterno} accedida correctamente para cacheo.")
            # Pausa para asegurarse de que el servidor procese la petición (opcional)
            time.sleep(1)
            
            # Descargar la imagen
            response_image = requests.get(image_url)
            if response_image.status_code == 200:
                with open(image_path, 'wb') as img_file:
                    img_file.write(response_image.content)
                print(f"Imagen de {nombre} {apellido_paterno} descargada correctamente.")
            else:
                print(f"Error al descargar la imagen de {nombre} {apellido_paterno}. Código de respuesta: {response_image.status_code}")
        else:
            print(f"Error al acceder a la página de {nombre} {apellido_paterno}. Código de respuesta: {response_details.status_code}")
    except Exception as e:
        print(f"Error al procesar la información de {nombre} {apellido_paterno}: {e}")
