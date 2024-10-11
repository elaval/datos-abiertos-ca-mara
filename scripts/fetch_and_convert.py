#!/usr/bin/env python3

import requests
import xmltodict
import json
import os

def fetch_and_convert():
    # URL of the web service
    url = "https://opendata.camara.cl/camaradiputados/WServices/WSDiputado.asmx/retornarDiputados"

    try:
        # Fetch the XML data
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        xml_content = response.content

        # Convert XML to dict
        data_dict = xmltodict.parse(xml_content)

        # Convert dict to JSON
        json_data = json.dumps(data_dict, ensure_ascii=False, indent=4)

        # Ensure the data directory exists
        os.makedirs('data', exist_ok=True)

        # Save the JSON data
        with open('data/diputados.json', 'w', encoding='utf-8') as f:
            f.write(json_data)

        print("Data successfully fetched and converted.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_convert()
