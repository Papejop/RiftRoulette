import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configuration
directory_url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/"
download_folder = "downloaded_files"

# Create download folder if it doesn't exist
os.makedirs(download_folder, exist_ok=True)

# Get the HTML of the directory
response = requests.get(directory_url)
response.raise_for_status()

# Parse HTML and extract all <a href=""> links
soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a")

# Download files (skip parent directory and folders)
for link in links:
    href = link.get("href")
    if not href or href.endswith('/') or href.startswith('?') or href.startswith('#'):
        continue  # Skip folders and junk links

    file_url = urljoin(directory_url, href)
    file_name = os.path.basename(href)
    local_path = os.path.join(download_folder, file_name)

    print(f"Downloading {file_url} -> {local_path}")
    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
