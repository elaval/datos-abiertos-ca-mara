#!/usr/bin/env python3

import requests
import xmltodict
import json
import os
import time

def fetch_and_convert():
    # Existing code to fetch other data sources
    # For example, fetching diputados or other endpoints
    pass

def fetch_votaciones_2006():
    # URL to get the list of votaciones for 2024
    url_votaciones_2006 = 'https://opendata.camara.cl/camaradiputados/WServices/WSLegislativo.asmx/retornarVotacionesXAnno?prmAnno=2006'

    try:
        # Fetch the XML data
        response = requests.get(url_votaciones_2006)
        response.raise_for_status()
        xml_content = response.content

        # Convert XML to dict
        data_dict = xmltodict.parse(xml_content)

        # Convert dict to JSON
        json_data = json.dumps(data_dict, ensure_ascii=False, indent=4)

        # Ensure the data directory exists
        os.makedirs('data', exist_ok=True)

        # Save the JSON data
        with open('data/votacionesAño_2006.json', 'w', encoding='utf-8') as f:
            f.write(json_data)

        print("votacionesAño_2006.json successfully updated.")

        return data_dict  # Return the data dictionary for further processing

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching votaciones for 2024: {e}")
        return None

def fetch_votaciones_details():
    # Fetch the list of votaciones for 2024
    data_dict = fetch_votaciones_2006()
    if data_dict is None:
        print("Failed to fetch votaciones for 2006. Exiting.")
        return

    # Access the list of votaciones
    votaciones_list = data_dict['VotacionesColeccion']['Votacion']

    # Ensure the directory for votaciones details exists
    os.makedirs('data/votaciones_detalles', exist_ok=True)

    for votacion in votaciones_list:
        votacion_id = votacion['Id']
        details_filename = f'data/votaciones_detalles/2006/detallesVotacion_{votacion_id}.json'

        # Check if the details file already exists
        if not os.path.exists(details_filename):
            # Fetch the details
            url_votacion_detalle = f'https://opendata.camara.cl/camaradiputados/WServices/WSLegislativo.asmx/retornarVotacionDetalle?prmVotacionId={votacion_id}'

            try:
                response_detalle = requests.get(url_votacion_detalle)
                response_detalle.raise_for_status()
                xml_content_detalle = response_detalle.content

                # Convert XML to dict
                data_dict_detalle = xmltodict.parse(xml_content_detalle)

                # Convert dict to JSON
                json_data_detalle = json.dumps(data_dict_detalle, ensure_ascii=False, indent=4)

                # Save the details JSON file
                with open(details_filename, 'w', encoding='utf-8') as f:
                    f.write(json_data_detalle)

                print(f'Details for votación {votacion_id} saved.')

                # Optional: Delay between requests to be polite to the server
                time.sleep(0.1)  # Sleep for 100 milliseconds

            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching details for votación {votacion_id}: {e}")
        else:
            print(f'Details for votación {votacion_id} already exist. Skipping download.')

if __name__ == "__main__":
    # Existing function to fetch other data
    fetch_and_convert()

    # Fetch votaciones details
    fetch_votaciones_details()