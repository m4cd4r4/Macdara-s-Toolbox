from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import os

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
    image_elements = driver.find_elements(By.TAG_NAME, 'img')
    return [image.get_attribute('src') for image in image_elements]

def get_first_n_links(driver, num_links):
    """Extract the first `num_links` links from the current page."""
    links = driver.find_elements(By.TAG_NAME, 'a')[:num_links]
    return [link.get_attribute('href') for link in links if link.get_attribute('href')]

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

def get_first_n_links(driver, num_links):
    """Extract the first `num_links` links from the current page."""
    links_elements = driver.find_elements(By.TAG_NAME, 'a')
    links = [link.get_attribute('href') for link in links_elements if link.get_attribute('href')]
    return links[:num_links]

def main():
    url = input("Enter the URL of the website: ")
    num_links = int(input("Enter the number of links to follow: "))

    chrome_options = webdriver.ChromeOptions()
    path_to_chrome = "C:/Program Files/Google/Chrome/Application/Chrome.exe"
    chrome_options.binary_location = path_to_chrome

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # Download images from the main page
    image_urls = get_image_urls(driver)
    for image_url in image_urls:
        download_image(image_url)

    # Follow links and download images, text blocks from those pages
    follow_links_and_download_content(driver, num_links)

    driver.quit()

if __name__ == "__main__":
    main()