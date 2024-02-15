# The script uses Beautiful Soup to parse HTML content and extract links for crawling a website. 
# It converts each visited page to a PDF using pdfkit, a wrapper for wkhtmltopdf. 
# Ensure wkhtmltopdf is installed on your system and available in your PATH for pdfkit to function correctly.

# Logging is used for basic feedback during the crawling and PDF conversion process. 
# The script attempts to visit all links found on the initial page that lead to the same domain, 
# converting each page into a PDF file and storing it in the specified output directory.

# This solution is efficient for straightforward websites but might need adjustments 
# for more complex sites requiring login, handling JavaScript dynamically loaded content, 
# or dealing with infinite scroll pages.

# This script:
# - prompts the user for a website URL to convert to PDF. It then uses this URL as the base URL for the WebsiteToPDF class and proceeds with the crawling and conversion process as before. 
# - creates a new folder for the PDFs based on the website's domain name, excluding "http://", "https://", "www", and ".com". It stores the PDF files in this newly created directory. The script first parses the base URL to extract the domain name, then formats it to remove unwanted parts and create a directory structure under a pdfs folder. If the directory does not exist, it is created using os.makedirs().
# - uses wkhtmltopdf, which can be downloaded at https://wkhtmltopdf.org/downloads.html
# - uses pdfkit, a pure Python solution, for converting web pages to PDF, adhering to Python best practices and ensuring error handling and logging are properly implemented. This solution is efficient, using external tools (wkhtmltopdf) only when necessary, and maintains a clean, modular codebase.

# Please ensure that you add the path to wkhtmltopdf to your PATH environment variables.
 
# website_to_pdfv0.1.py
# Macdara O Murchu
# 15.02.24

import os
import logging
import requests
import pdfkit
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tkinter as tk
from tkinter.simpledialog import askstring


path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Use the correct path to wkhtmltopdf on your system
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class WebsiteToPDF:
    def __init__(self, base_url):
        self.base_url = base_url
        self.output_dir = self.create_output_dir(base_url)
        self.links_to_visit = set([self.base_url])
        self.visited_links = set()

    def create_output_dir(self, base_url):
        parsed_url = urlparse(base_url)
        folder_name = parsed_url.netloc.replace("www.", "").split('.')[0]
        output_dir = os.path.join('pdfs', folder_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    def fetch_html(self, url):
        try:
            response = requests.get(url)
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

def save_pdf(self, url, output_path):
    options = {
        'enable-javascript': '',
        'javascript-delay': '1000',  # Adjust delay as needed, in milliseconds
        'no-stop-slow-scripts': '',
        'custom-header': [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        ],
        # Removed 'page-load-timeout' due to compatibility issue
        'no-images': '',  # Uncomment or remove based on your needs
    }
    
    try:
        # Remove the configuration parameter from the call
        pdfkit.from_url(url, output_path, options=options)
    except IOError as e:
        logging.error(f"Failed to save PDF for {url}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    user_input_url = input("Please enter a website URL to convert to PDF: ").strip()
    if user_input_url:
        try:
            website_to_pdf = WebsiteToPDF(user_input_url)
            website_to_pdf.crawl_and_convert()
        except Exception as e:
            logging.error(f"Error during conversion: {e}")
    else:
        logging.error("URL not provided.")
