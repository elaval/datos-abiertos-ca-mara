#!/usr/bin/env python3

import requests
import xmltodict
import json
import os

def fetch_and_convert():
    endpoints = {
        'diputados': 'https://opendata.camara.cl/camaradiputados/WServices/WSDiputado.asmx/retornarDiputados',
        'diputadosPeriodoActual': 'https://opendata.camara.cl/camaradiputados/WServices/WSDiputado.asmx/retornarDiputadosPeriodoActual?',  # Replace with actual URL
        # Add more endpoints as needed
    }

    for filename, url in endpoints.items():
        try:
            response = requests.get(url)
            response.raise_for_status()
            xml_content = response.content
            data_dict = xmltodict.parse(xml_content)
            json_data = json.dumps(data_dict, ensure_ascii=False, indent=4)

            os.makedirs('data', exist_ok=True)
            with open(f'data/{filename}.json', 'w', encoding='utf-8') as f:
                f.write(json_data)

            print(f"{filename}.json successfully updated.")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching {filename}: {e}")

if __name__ == "__main__":
    fetch_and_convert()
