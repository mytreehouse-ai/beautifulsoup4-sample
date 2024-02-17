import json
from bs4 import BeautifulSoup

# Helper function to safely get attribute value


def get_attribute(element, attribute):
    value = element.attrs.get(attribute, '')
    return 'n/a' if not value else value

# Function to extract property details


def extract_property_info(file_path):
    with open(file_path, 'r') as file:
        # As it's a JSONL file, each line is a separate JSON object
        for line in file:
            data = json.loads(line)
            # Get the HTML data from the 'result' property
            html_data = data.get('result', '')

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
            'category': get_attribute(element, 'data-category'),
            'subcategories': get_attribute(element, 'data-subcategories'),
            'building_size': get_attribute(element, 'data-building_size'),
            'land_size': get_attribute(element, 'data-land_size'),
            'furnished': get_attribute(element, 'data-furnished'),
            'classification': get_attribute(element, 'data-classification'),
            'block': get_attribute(element, 'data-block'),
            'subdivision_name': get_attribute(element, 'data-subdivisionname'),
            'sku': get_attribute(element, 'data-sku'),
            'geo_point': get_attribute(element, 'data-geo-point'),
            'listing_link': element.find('a', class_='js-listing-link')['href'] if element.find('a', class_='js-listing-link') else 'n/a'
        }
        property_details.append(details_dict)

    return len(property_details), property_details


# Path to the JSONL file for warehouse data
warehouse_file_path = 'jsonl/page-1-warehouse-job-844249-result.jsonl'

# Extracting warehouse information
number_of_properties, properties_list = extract_property_info(
    warehouse_file_path)
pretty_json = json.dumps(properties_list, indent=4)
print(pretty_json)
print(number_of_properties)
