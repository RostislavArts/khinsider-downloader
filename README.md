# KHInsider Music Downloader

A Python script to automatically download music tracks from KHInsider (downloads.khinsider.com), a popular video game music archive.

## Features

- Download entire soundtracks from KHInsider
- Automatic file organization and sanitization
- Retry mechanism for failed downloads
- Progress tracking with visual progress bar
- Rate limiting to be respectful to the server
- Smart filename cleaning (removes invalid characters)
- Configurable delays between downloads

## Prerequisites

- Python 3.6 or higher
- Required Python packages (install via `pip install -r requirements.txt`):
  - `requests`
  - `beautifulsoup4`
  - `tqdm`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/khinsider-downloader.git
cd khinsider-downloader
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests beautifulsoup4 tqdm
```

## Usage

Run the script with a KHInsider album page URL:

```bash
python khinsider_downloader.py <album_url>
```

### Example

```bash
python khinsider_downloader.py "https://downloads.khinsider.com/game-soundtracks/album/gex"
```

The script will:
1. Parse the album page to find all available tracks
2. Create a `downloaded` folder in the current directory
3. Download each MP3 file with a progress bar
4. Skip any invalid or inaccessible files
5. Show a summary of successful downloads

## Configuration

You can modify these settings at the top of the script:

- `DOWNLOAD_DIR`: Directory where files will be saved (default: "downloaded")
- `TIMEOUT`: Request timeout in seconds (default: 30)
- `MAX_RETRIES`: Number of retry attempts for failed downloads (default: 3)
- `DELAY`: Delay between downloads in seconds (default: 2)

## File Naming

The script automatically:
- URL-decodes filenames
- Replaces invalid characters with underscores
- Converts file extensions to lowercase
- Prevents duplicate underscores

## Error Handling

The script includes robust error handling:
- Validates MP3 URLs before attempting downloads
- Retries failed downloads with exponential backoff
- Continues processing even if individual tracks fail
- Provides detailed error messages

## Respectful Usage

This script is designed to be respectful to KHInsider's servers:
- Includes proper User-Agent headers
- Implements delays between requests
- Uses reasonable timeout values
- Includes retry limits

Please use responsibly and consider supporting the artists and game developers whose music you download.

## Sample Output

```
Getting track list...
Found 25 tracks. Starting download...
Downloading: 100%|██████████| 25/25 [02:30<00:00,  1.20it/s]
 Success: 01_-_Opening_Theme.mp3
 Success: 02_-_Main_Menu.mp3
...

Done! Successfully downloaded 23/25 tracks
```

## Troubleshooting

**"Table songlist not found!"**
- The URL might be incorrect or the page structure has changed
- Make sure you're using the main album page URL, not individual track URLs

**"No tracks to download!"**
- The album page might not contain any downloadable tracks
- Some albums might have different page structures

**Downloads failing consistently**
- Check your internet connection
- The server might be experiencing issues
- Try increasing the `TIMEOUT` and `DELAY` values

## Legal Notice

This tool is for educational purposes and personal use only. Please respect copyright laws and the terms of service of KHInsider. Consider purchasing official releases to support the artists and developers.

