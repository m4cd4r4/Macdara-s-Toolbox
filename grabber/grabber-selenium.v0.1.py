from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import requests
import os

def download_image(image_url, folder_name='downloaded_images'):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    try:
        image_content = requests.get(image_url).content
        filename = os.path.join(folder_name, image_url.split('/')[-1])
        with open(filename, 'wb') as image_file:
            image_file.write(image_content)
            print(f"Downloaded {image_url} into {filename}")
    except Exception as e:
        print(f"An error occurred   downloading {image_url}: {e}")

def get_image_urls(driver):
    image_elements = driver.find_elements_by_tag_name('img')
    return [image.get_attribute('src') for image in image_elements]

def main():
    url = input("Enter the URL of the website: ")

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    image_urls = get_image_urls(driver)
    for image_url in image_urls:
        download_image(image_url)

    driver.quit()

if __name__ == "__main__":
    main()