# Youtube-Scraping

This project allows you to scrape videos from a YouTube channel, download them, and save their descriptions.

## Features

- Retrieve videos from a YouTube channel.
- Download videos in the best available format.
- Save video descriptions to text files.
- Store video information in a JSON file.

## Requirements

- Python 3.x
- `google-api-python-client`
- `python-dotenv`
- `yt-dlp`
- `ffmpeg`

## Setup

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd Youtube-Scraping
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your YouTube API key:
    ```sh
    cp env.template .env
    # Edit .env and add your YOUTUBE_API_KEY
    ```

4. Download and install FFmpeg:
    - **Windows**:
        1. Download the FFmpeg zip file from [FFmpeg Download Page](https://ffmpeg.org/download.html).
        2. Extract the zip file and place the `bin` folder in a directory of your choice.
        3. Add the path to the `bin` folder to your system's PATH environment variable.
    - **macOS**:
        ```sh
        brew install ffmpeg
        ```
    - **Linux**:
        ```sh
        sudo apt update
        sudo apt install ffmpeg
        ```

## Usage

1. Run the script:
    ```sh
    python scraping_all_channel.py
    ```

2. Enter the YouTube channel URL when prompted.

## File Structure

- `scraping_all_channel.py`: Main script to scrape and download videos.
- `.env`: Environment file containing the YouTube API key.
- `env.template`: Template for the environment file.
- `requirements.txt`: List of required Python packages.
- `downloads/`: Directory where downloaded videos and descriptions are saved.

## Logging

Logs are generated to provide information about the scraping and downloading process. They include details about the number of videos found, download status, and any errors encountered.