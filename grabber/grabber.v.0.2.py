# Grabber - Pulls all images & text blocks from any website
# Populates a spreadsheet with the text block content
# Author: Macdara O Murchu
# 26-01-24

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import base64
import openpyxl

# Ensure this URL is correct and you have permission to scrape the website
url = 'https://felixmobile.com.au'

# Make a request to the website
r = requests.get(url)
html_content = r.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Create a directory to save the downloaded content
folder_name = 'downloaded_content'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

# Initialize a counter for images to ensure unique filenames
total_images = 0

# Function to save content
def save_content(src, content_type):
    # Use the global keyword to indicate that we are using the global total_images variable
    global total_images
    try:
        # Check if src is a data URL
        if src.startswith('data:image'):
            header, data = src.split(',')
            file_ext = header.split(';')[0].split('/')[1]
            img_data = base64.b64decode(data)
            filename = os.path.join(folder_name, f'image{total_images}.{file_ext}')
            # Increment the counter after using it to ensure unique filenames
            total_images += 1
            with open(filename, 'wb') as file:
                file.write(img_data)
            print(f"Downloaded {content_type}: {filename}")
        else:
            abs_src = urljoin(url, src)
            content = requests.get(abs_src)
            filename = os.path.join(folder_name, f'image{total_images}{os.path.splitext(abs_src)[1]}')
            total_images += 1
            with open(filename, 'wb') as file:
                file.write(content.content)
            print(f"Downloaded {content_type}: {filename}")
    except Exception as e:
        print(f"An error occurred with {src}: {e}")

# Find and save all images
for img in soup.find_all('img'):
    img_src = img.get('src')
    save_content(img_src, 'image')

# Find and save all text blocks (p tags as an example)
for text_block in soup.find_all('p'):
    text = text_block.get_text()
    filename = os.path.join(folder_name, f"text_block_{soup.find_all('p').index(text_block)}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Saved text block: {filename}")

# Find and save all icons (assuming they are i tags with classes like 'fa' for font-awesome)
for icon in soup.find_all('i'):
    if 'fa' in icon.get('class', []):
        icon_class = ' '.join(icon.get('class'))
        filename = os.path.join(folder_name, f"icon_{soup.find_all('i').index(icon)}.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(icon_class)
        print(f"Saved icon classes: {filename}")


# Function to write text blocks to a spreadsheet
import urllib.parse

def write_text_to_spreadsheet(folder_name):
    # Create a new workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    
    # Set the title of the worksheet
    ws.title = 'Text Blocks'
    
    # Find all text files and append content to the worksheet
    for text_file in os.listdir(folder_name):
        if text_file.startswith("text_block_") and text_file.endswith(".txt"):
            file_path = os.path.join(folder_name, text_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read().strip()
                if text:  # Only append if there is text content
                    ws.append([text])
    
    # Save the workbook
    spreadsheet_name = f'text_blocks_{urllib.parse.urlparse(url).netloc}.xlsx'
    wb.save(os.path.join(folder_name, spreadsheet_name))
    print(f"Spreadsheet saved as: {spreadsheet_name}")


# Call the function after all text blocks have been saved
write_text_to_spreadsheet(folder_name)