import requests
import xml.etree.ElementTree as ET
import pandas as pd

def fetch_boletin_details(boletin_number):
    """
    Fetch the details of a given boletin from the API and return its description.
    """
    base_url = 'https://opendata.camara.cl/camaradiputados/WServices/WSLegislativo.asmx/retornarProyectoLey'
    url = f'{base_url}?prmNumeroBoletin={boletin_number}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        xml_content = response.content
        
        # Parse XML
        root = ET.fromstring(xml_content)
        
        # Find the 'Nombre' element which contains the description
        namespace = {'ns': 'http://opendata.camara.cl/camaradiputados/v1'}
        nombre_element = root.find('ns:Nombre', namespace)
        
        # If the element is found, return its text content, otherwise return a default message
        if nombre_element is not None:
            return nombre_element.text
        else:
            return 'No description available'
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for boletin {boletin_number}: {e}")
        return 'Error fetching data'

def process_boletines(file_path):
    """
    Read the TSV file containing boletin numbers, fetch their descriptions, and save the results to a new file.
    """
    # Read the TSV file
    boletines_df = pd.read_csv(file_path, sep='\t', names=['Boletin'])
    
    # Fetch descriptions for each boletin
    boletines_df['Description'] = boletines_df['Boletin'].apply(fetch_boletin_details)
    
    # Save the updated DataFrame to a new TSV file
    output_file = '../data/boletines/2006/boletines_with_descriptions.tsv'
    boletines_df.to_csv(output_file, sep='\t', index=False)
    print(f"Data saved to {output_file}")

# Example usage
# Assuming the TSV file is named 'boletines.tsv' and located in the current directory
process_boletines('../data/boletines/2006/boletines.tsv')
