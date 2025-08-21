#!/usr/bin/env python3
import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import time
from tqdm import tqdm
import re

BASE_URL = "https://downloads.khinsider.com"
TABLE_ID = "songlist"
DOWNLOAD_DIR = "downloaded"
TIMEOUT = 30
MAX_RETRIES = 3
DELAY = 2

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": BASE_URL,
}

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(filename):
    decoded = unquote(filename)
    
    name, ext = os.path.splitext(decoded)
    
    sanitized_name = re.sub(r'[^\w]', '_', name)
    sanitized_name = re.sub(r'_+', '_', sanitized_name)
    
    return sanitized_name + ext.lower()

def is_valid_mp3_url(url):
    return url and url.endswith('.mp3') and not url.startswith('/cp')

def download_file(url, filename):
    if not is_valid_mp3_url(url):
        print(f"Skipping invalid URL: {url}")
        return False

    clean_filename = sanitize_filename(filename)
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                stream=True,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            
            filepath = os.path.join(DOWNLOAD_DIR, clean_filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f" Success: {clean_filename}")
            return True
            
        except Exception as e:
            print(f"Attempt {attempt + 1}/{MAX_RETRIES} for {clean_filename}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY * (attempt + 1))
    return False

def get_mp3_url(song_page_url):
    try:
        response = requests.get(song_page_url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if is_valid_mp3_url(href):
                return href if href.startswith('http') else urljoin(BASE_URL, href)
        
        download_btn = soup.find('span', class_='songDownloadLink')
        if download_btn:
            parent_link = download_btn.find_parent('a', href=True)
            if parent_link and is_valid_mp3_url(parent_link['href']):
                return parent_link['href'] if parent_link['href'].startswith('http') else urljoin(BASE_URL, parent_link['href'])
    
    except Exception as e:
        print(f"Error getting MP3 URL: {e}")
    
    return None

def parse_and_download(page_url):
    try:
        print("Getting track list...")
        response = requests.get(page_url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', id=TABLE_ID)
        if not table:
            print(f"Table {TABLE_ID} not found!")
            return
        
        rows = table.find_all('tr')[1:]
        if not rows:
            print("No tracks to download!")
            return
        
        print(f"Found {len(rows)} tracks. Starting download...")
        
        success_count = 0
        for row in tqdm(rows, desc="Downloading"):
            try:
                main_link = row.find('td', class_='clickable-row').find('a', href=True)
                if not main_link:
                    continue
                    
                song_page_url = urljoin(BASE_URL, main_link['href'])
                
                mp3_url = get_mp3_url(song_page_url)
                if not mp3_url:
                    print(f"MP3 link not found for {song_page_url}")
                    continue
                
                filename = os.path.basename(mp3_url)
                if download_file(mp3_url, filename):
                    success_count += 1
                
                time.sleep(DELAY)
                
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
                
        print(f"\nDone! Successfully downloaded {success_count}/{len(rows)} tracks")
        
    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <track_page_URL>")
        sys.exit(1)
    page_url = sys.argv[1]
    parse_and_download(page_url)

