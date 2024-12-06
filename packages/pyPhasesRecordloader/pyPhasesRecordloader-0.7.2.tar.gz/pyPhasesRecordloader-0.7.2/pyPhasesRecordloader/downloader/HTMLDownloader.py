from pathlib import Path

from pyPhasesRecordloader.downloader.Downloader import Downloader


class HTMLDownloader(Downloader):
    def __init__(self, config) -> None:
       super().__init__(config)

    def downloadTo(self, filePath, patternString=None):        
        import os
        import requests
        from bs4 import BeautifulSoup

        # Base URL of the directory
        base_url = self.basePath

        def download_file(url, dest_folder):
            dest = Path(dest_folder)
            local_filename = dest.joinpath(url.split('/')[-1])
            if local_filename.exists():
                print(f"File {local_filename} already exists, skipping")
                return
            
            local_filename_tmp = local_filename.as_posix() + ".tmp"
            
            Path(dest_folder).mkdir(parents=True, exist_ok=True)
            response = requests.get(url, stream=True)
            with open(local_filename_tmp, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            Path(local_filename_tmp).rename(local_filename)
            print(f"Downloaded {local_filename}")

        def scrape_and_download(base_url, dest_folder):
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                if href and href not in ['../'] and href[0] not in ['/', '#'] and not href.startswith('http'):
                    full_url = f"{base_url}/{href}"
                    if href.endswith('/'):
                        full_url = full_url[:-1]
                        print(f"Scrape {full_url} to {os.path.join(dest_folder, href)}")
                        # Recursively download files in subdirectories
                        scrape_and_download(full_url, os.path.join(dest_folder, href))
                    else:
                        print(f"Downloading {full_url}")
                        download_file(full_url, dest_folder)

        # Start scraping and downloading
        scrape_and_download(base_url, dest_folder=filePath)
