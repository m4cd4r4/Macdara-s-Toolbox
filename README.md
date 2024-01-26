# Grabber - Website Content Scraper

## Project Description
Grabber is a Python script designed for scraping and extracting content from websites. It automatically downloads all images and text blocks from the specified URL, saving them into a local directory. Additionally, it compiles all the extracted text into a spreadsheet, organizing the content for easy review and analysis. This tool is ideal for content creators, data analysts, and web developers looking to gather resources or data from web pages.

## How to Install and Run the Project
To use Grabber, follow these steps:

1. Ensure you have Python installed on your system. If not, download and install it from [Python's official website](https://www.python.org/downloads/).

2. Install the required Python libraries: BeautifulSoup, requests, and openpyxl. You can do this by running:
pip install beautifulsoup4 requests openpyxl


3. Download the `grabber.py` script to your local machine.

4. Open a terminal or command prompt, navigate to the directory containing `grabber.py`, and run the script using:
python grabber.py


## How to Use the Project
1. Open the `grabber.py` script in a text editor.

2. Modify the `url` variable at the top of the script to the website you want to scrape:
```python
url = 'https://example.com'


Run the script as mentioned in the installation and running section.

Once completed, check the downloaded_content folder for images and text blocks, and a spreadsheet named text_blocks_[domain].xlsx for the text content.

License
This project is available under the MIT License. This means you can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software under the following conditions:

Appropriate credit is given, and the copyright notice and this permission notice are included in all copies or substantial portions of the Software.

The software is provided "as is", without warranty of any kind.
For the full license text, refer to the MIT License.
