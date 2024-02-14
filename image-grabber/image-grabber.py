import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os

async def download_image(session, url, save_path):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                with open(save_path, 'wb') as f:
                    f.write(content)
            else:
                print(f"Error downloading {url}: Status code {response.status}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

async def fetch_and_download_images(page_url, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(page_url) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            images = soup.find_all('img')
            tasks = []
            for img in images:
                img_url = img['src'] if img['src'].startswith('http') else page_url + img['src']
                img_name = os.path.basename(img_url)
                save_path = os.path.join(download_folder, img_name)
                tasks.append(download_image(session, img_url, save_path))
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    page_url = "[enter-your-url-here]"
    download_folder = 'downloaded_images'
    asyncio.run(fetch_and_download_images(page_url, download_folder))
