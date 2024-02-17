import json
from bs4 import BeautifulSoup

def get_attribute(element, attribute):
    value = element.attrs.get(attribute, 'n/a')
    return 'n/a' if not value else value

def extract_lot_info(file_path):
    with open(file_path, 'r') as file:
        # As it's a JSONL file, each line is a separate JSON object
        for line in file:
            data = json.loads(line)
            html_data = data.get('result', '')  # Get the HTML data from the 'result' property

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_data, 'html.parser')

    # Extract the information from the elements with the specified class
    info_elements = soup.find_all(class_='ListingCell-AllInfo ListingUnit')

    # Extracting the property details with updated attribute check
    property_details = []  # List to store all property details
    for element in info_elements:
        details_dict = {
            'price': get_attribute(element, 'data-price'),
            'category': get_attribute(element, 'data-category'),
            'subcategories': get_attribute(element, 'data-subcategories'),
            'land_size': get_attribute(element, 'data-land_size'),
            'furnished': get_attribute(element, 'data-furnished'),
            'classification': get_attribute(element, 'data-classification'),
            'block': get_attribute(element, 'data-block'),
            'subdivision_name': get_attribute(element, 'data-subdivisionname'),
            'sku': get_attribute(element, 'data-sku'),
            'geo_point': get_attribute(element, 'data-geo-point'),
            'listing_link': element.find('a', class_='js-listing-link')['href'] if element.find('a', class_='js-listing-link') else None
        }
        property_details.append(details_dict)

    return len(property_details), property_details

# Path to the JSONL file
file_path = 'lot-job-818997-result.jsonl'

# Extracting lot information
lot_info_count, lot_info_details = extract_lot_info(file_path)
print(lot_info_details)
print(f'Total Lots: {lot_info_count}')
