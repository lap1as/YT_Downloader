# YouTube Downloader Telegram Bot

This Telegram bot allows users to download YouTube videos and audios directly within the Telegram platform.

## Installation

### Using `requirements.txt`

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/lap1as/YT_Downloader.git
    cd YT_Downloader
    ```

2. Install dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

### Using Poetry

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/lap1as/YT_Downloader.git
    cd YT_Downloader
    ```

2. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

## Configuration

1. Create a `.env` file in the root directory of your project.

2. Add the following configuration variables to the `.env` file:

    ```dotenv
    BOT_TOKEN=your_bot_token_here
    ADMIN_ID=your_admin_id_here
    ```

    Replace `your_bot_token_here` with your Telegram bot API token. You can obtain this token by creating a new bot using the BotFather on Telegram.

    Replace `your_admin_id_here` with your Telegram user ID. This step may not be necessary for all bots, depending on your implementation.

## Usage

Once installed and configured, you can start the bot by running the following command:

```bash
python3 main.py
```
Or if you installed using poetry:
```bash
poetry run python main.py
```

## Features
- Download YouTube videos and audios directly within Telegram.
- Easy-to-use interface for users.
