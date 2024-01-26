import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Make sure to replace this with the actual URL
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

# Function to save content
def save_content(src, content_type):
    # Get the absolute URL for the content
    abs_src = urljoin(url, src)
    # Get the content
    content = requests.get(abs_src)
    # Create a valid filename
    filename = os.path.join(folder_name, abs_src.split('/')[-1])
    # Write content to file
    with open(filename, 'wb') as file:
        file.write(content.content)
    print(f"Downloaded {content_type}: {filename}")

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
