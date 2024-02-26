import json
from bs4 import BeautifulSoup

# Load the JSONL file
file_path = 'jsonl/page-1-warehouse-02252024.jsonl'

# Function to get attribute safely


def get_attribute(element, attribute):
    value = element.attrs.get(attribute, '')
    return 'n/a' if not value else value


def extract_info(file_path):
    with open(file_path, 'r') as file:
        # As it's a JSONL file, each line is a separate JSON object
        for line in file:
            data = json.loads(line)
            # Get the HTML data from the 'response' -> 'body' property
            html_data = data['response']['body']
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_data, 'html.parser')

    # Extract the information from the elements with the specified class
    info_elements = soup.find_all(class_='ListingCell-AllInfo ListingUnit')

    # Extracting the property details with updated attribute check
    property_details = []  # List to store all property details
    for element in info_elements:
        details_dict = {
            'title': element.find('a', class_='js-listing-link')['title'] if element.find('a', class_='js-listing-link') else 'n/a',
            'price': get_attribute(element, 'data-price'),
            # Seen in warehouse
            'price_condition': get_attribute(element, 'data-price_conditions'),
            'category': get_attribute(element, 'data-category'),
            'subcategories': get_attribute(element, 'data-subcategories'),
            'year_built': get_attribute(element, 'data-year_built'),
            'condo_name': get_attribute(element, 'data-condominiumname'),
            # For warehouse
            'subdivision_name': get_attribute(element, 'data-subdivisionname'),
            'car_spaces': get_attribute(element, 'data-car_spaces'),
            'bedrooms': get_attribute(element, 'data-bedrooms'),
            'bathrooms': get_attribute(element, 'data-bathrooms'),
            # floor area
            'building_size': get_attribute(element, 'data-building_size'),
            # sqm
            'land_size': get_attribute(element, 'data-land_size'),
            'furnished': get_attribute(element, 'data-furnished'),
            'classification': get_attribute(element, 'data-classification'),
            'block': get_attribute(element, 'data-block'),
            'subdivision_name': get_attribute(element, 'data-subdivisionname'),
            'sku': get_attribute(element, 'data-sku'),
            'geo_point': [float(coord.strip('[]')) for coord in get_attribute(element, 'data-geo-point').split(',')] if get_attribute(element, 'data-geo-point') != 'n/a' else 'n/a',
            'listing_link': element.find('a', class_='js-listing-link')['href'] if element.find('a', class_='js-listing-link') else None
        }
        property_details.append(details_dict)

    print(json.dumps(property_details, indent=4))
    print(len(property_details))


# Provide the path to your JSONL file
extract_info(file_path)
