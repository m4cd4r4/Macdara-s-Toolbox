from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import base64
import os

# Assuming the sanitize_filename and download_image functions are defined as previously provided

def get_first_n_links(driver, num_links):
    """Extract the first `num_links` links from the current page."""
    links_elements = driver.find_elements(By.TAG_NAME, 'a')
    links = [link.get_attribute('href') for link in links_elements if link.get_attribute('href')]
    return links[:num_links]

def follow_links_and_download_content(driver, num_links):
    """Follow links, download images, and save text blocks from linked pages."""
    initial_url = driver.current_url
    links = get_first_n_links(driver, num_links)

    for index, link in enumerate(links, start=1):
        try:
            driver.get(link)
            # Download images from the current linked page
            image_urls = get_image_urls(driver)
            for image_url in image_urls:
                download_image(image_url)

            # Save text blocks from the current linked page
            text_blocks = get_text_blocks(driver)
            for text_index, text_block in enumerate(text_blocks, start=1):
                save_text_block(text_block, f"{index}_{text_index}", folder_name='downloaded_texts_from_links')

            # Return to the initial URL to avoid issues with navigation
            driver.get(initial_url)
        except Exception as e:
            print(f"An error occurred while processing {link}: {e}")
            driver.get(initial_url)  # Ensure driver returns to initial page if an error occurs


def sanitize_filename(url):
    # Replace invalid characters with underscores or remove them
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        url = url.replace(char, '_')
    return url

def download_image(image_url, folder_name='downloaded_images'):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    try:
        image_content = requests.get(image_url).content
        sanitized_filename = sanitize_filename(image_url.split('/')[-1])
        filename = os.path.join(folder_name, sanitized_filename)
        with open(filename, 'wb') as image_file:
            image_file.write(image_content)
            print(f"Downloaded {image_url} into {filename}")
    except Exception as e:
        print(f"An error occurred downloading {image_url}: {e}")


def get_image_urls(driver):
    """Extract image URLs from the current page."""
    image_elements = driver.find_elements(By.TAG_NAME, 'img')
    return [image.get_attribute('src') for image in image_elements]

def get_text_blocks(driver):
    """Extract text blocks from the current page."""
    text_blocks = []
    text_elements = driver.find_elements(By.XPATH, "//p | //h1 | //h2 | //h3 | //h4 | //h5 | //h6")
    for element in text_elements:
        try:
            text = element.text.strip()
            if text:
                text_blocks.append(text)
        except Exception:
            print("Encountered a problem with a text element, skipping...")
    return text_blocks

def save_text_block(text, index, folder_name='downloaded_texts', file_prefix='text_block'):
    """Save a given text block to a file, preserving paragraph form."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename = os.path.join(folder_name, f"{file_prefix}_{index}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text + "\n")
    print(f"Saved text block to {filename}")

def save_page_as_pdf(driver, url, folder_name='downloaded_pdfs', file_prefix='page'):
    """Save the current page as a PDF file."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    sanitized_url = sanitize_filename(url)
    filename = os.path.join(folder_name, f"{file_prefix}_{sanitized_url}.pdf")
    
    # Prepare the command to print the page as PDF
    pdf = driver.execute_cdp_cmd("Page.printToPDF", {
        "landscape": False,
        "displayHeaderFooter": False,
        "printBackground": True,
        "preferCSSPageSize": True,
    })
    
    # Decode the PDF data from base64 and save it to a file
    with open(filename, 'wb') as file:
        file.write(base64.b64decode(pdf['data']))
    print(f"Saved {url} as PDF to {filename}")

def main():
    url = input("Enter the URL of the website: ")
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    num_links = int(input("Enter the number of links to follow: "))
    num_links = min(num_links, 100)  # Limit for practicality

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Enable headless mode for PDF printing
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    save_page_as_pdf(driver, url)  # Save the main page as PDF

    # Download images from the main page
    image_urls = get_image_urls(driver)
    for image_url in image_urls:
        download_image(image_url)

    # Save text blocks from the main page
    text_blocks = get_text_blocks(driver)
    for index, text_block in enumerate(text_blocks, start=1):
        save_text_block(text_block, index)

    # Follow links and download content from those pages
    follow_links_and_download_content(driver, num_links)

    initial_url = driver.current_url
    links = get_first_n_links(driver, num_links)
    for index, link in enumerate(links, start=1):
        try:
            driver.get(link)
            # Existing code to download images and save text blocks
            save_page_as_pdf(driver, link, file_prefix=f"linked_page_{index}")  # Save the linked page as PDF
            driver.get(initial_url)
        except Exception as e:
            print(f"An error occurred while processing {link}: {e}")
            driver.get(initial_url)


    driver.quit()


if __name__ == "__main__":
    main()
