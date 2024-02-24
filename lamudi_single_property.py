import json
from bs4 import BeautifulSoup

def extract_property_details(jsonl_file):
    with open(jsonl_file, 'r') as file:
        # Reading line by line (assuming each line is a separate JSON object)
        for line in file:
            json_data = json.loads(line)
            
            # Assuming 'html' is the correct key holding the HTML content
            html_content = json_data['result']
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extracting property details
            property_details = {
                "address": extract_address(soup),
                "description": extract_description(soup),
                "images": extract_images(soup),
                "amenities": extract_amenities(soup)
            }
            
            return property_details

def extract_address(soup):
    address = soup.find(
        'h3',
        {
            'class': 'Title-pdp-address'
        }
    )
    
    return address.text.strip() if address else 'n/a'

def extract_description(soup):
    description_div = soup.find(
        'div',
        {
            'class': 'listing-section listing-description ViewMore js-ViewMoreSection'
        }
    )
    description_text = description_div.find(
        'div',
        {
            'class': 'ViewMore-text-description'
        }
    ) if description_div else None
    
    return description_text.text if description_text else 'n/a'

def extract_images(soup):
    images = []
    divs = soup.find_all(
        'div',
        {
            'class': 'Banner-Images'
        }
    )
    
    for div_tag in divs:
        img_tag = div_tag.find('img')
        if img_tag:
            data_src = img_tag.get('data-src')
            if data_src and data_src.endswith('.webp'):
                images.append(data_src)
                
    return images

def extract_amenities(soup):
    amenities_div = soup.find(
        'div',
        {
            'class': 'listing-amenities-list'
        }
    )
    amenities_span = amenities_div.find_all(
        'span',
        {
            'class': 'listing-amenities-name'
        }
    )
    amenities_list = [span.text.strip() for span in amenities_span]
    
    return amenities_list if amenities_div else []

# Provide the path to the JSONL file
jsonl_file = 'jsonl/warehouse-single-2-job-848553-result.jsonl'
property_details = extract_property_details(jsonl_file)
print(json.dumps(property_details, indent=4))