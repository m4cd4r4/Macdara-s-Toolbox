import os
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import pdfkit
import tkinter as tk
from tkinter.simpledialog import askstring

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebsiteToPDF:
    def __init__(self, base_url):
        self.session = requests.Session()  # Using sessions to maintain cookies
        self.base_url = base_url
        self.output_dir = self.create_output_dir(base_url)
        self.links_to_visit = set([self.base_url])
        self.visited_links = set()

    def create_output_dir(self, base_url):
        parsed_url = urlparse(base_url)
        domain_parts = parsed_url.netloc.replace("www.", "").split('.')
        folder_name = domain_parts[0] if len(domain_parts) > 1 else domain_parts
        output_dir = os.path.join('pdfs', folder_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    def fetch_html(self, url):
        try:
            response = self.session.get(url)  # use the session object here
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None

    def extract_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not href.startswith('mailto:'):
                full_url = urljoin(self.base_url, href)
                if full_url.startswith(self.base_url):
                    self.links_to_visit.add(full_url)

    def save_pdf(self, url):
        output_path = os.path.join(self.output_dir, f"{urlparse(url).path.strip('/').replace('/', '_') or 'index'}.pdf")
        options = {
            'enable-javascript': '',
            'javascript-delay': '5000',  # Increased delay to ensure JavaScript content loads
            'no-stop-slow-scripts': '',
            'disable-javascript': False,  # Ensure JavaScript is not disabled
            'custom-header': [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36')
            ],
            'no-images': '',
        }
        try:
            pdfkit.from_url(url, output_path, options=options, configuration=config)
            logging.info(f"PDF saved for {url} at {output_path}")
        except IOError as e:
            logging.error(f"Failed to save PDF for {url}: {e}")

    def crawl_and_convert(self):
        while self.links_to_visit:
            url = self.links_to_visit.pop()
            if url not in self.visited_links:
                logging.info(f"Visiting {url}")
                html = self.fetch_html(url)
                if html:
                    self.visited_links.add(url)
                    self.extract_links(html)
                    self.save_pdf(url)

if __name__ == "__main__":
    # Ensure that the path to wkhtmltopdf is correct and it's added to the system's PATH
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    
    # Initialize the tkinter GUI
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Use tkinter's askstring to prompt the user for the URL
    user_input_url = askstring("URL Input", "Please enter a website URL to convert to PDF:")
    root.destroy()  # Destroy the root window after getting input

    if user_input_url:
        try:
            website_to_pdf = WebsiteToPDF(user_input_url)
            website_to_pdf.crawl_and_convert()
        except Exception as e:
            logging.error(f"Error during conversion: {e}")
    else:
        logging.error("URL not provided.")
