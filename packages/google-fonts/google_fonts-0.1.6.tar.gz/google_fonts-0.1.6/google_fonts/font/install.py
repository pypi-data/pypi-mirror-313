import os
import platform
import time
from pathlib import Path

import requests
from shutil import copyfileobj
from tqdm import tqdm
from google_fonts.utils.font_data import fetch_ttf_url_download_list_by_name, fetch_ofl_list_json, get_font_names


def download_and_install_font(font_name, font_url, install_dir, max_retries=3, retry_delay=2):
    """
    Download and install a font from the given URL with a progress bar and automatic retries.
    """
    retry_count = 0

    while retry_count < max_retries:
        try:
            tqdm.write(f"Downloading {font_name} (Attempt {retry_count + 1}/{max_retries})...")
            response = requests.get(font_url, stream=True, timeout=10)
            response.raise_for_status()

            # Get total file size from headers
            total_size = int(response.headers.get('content-length', 0))

            # Save the font file locally
            font_path = os.path.join(install_dir, f"{font_name}")  # Use .otf if necessary
            with open(font_path, "wb") as f, tqdm(
                    desc=f"Installing {font_name}",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
                    bar.update(len(chunk))

            tqdm.write(f"{font_name} installed successfully at {install_dir}!")
            return  # Exit function on success
        except requests.exceptions.RequestException as e:
            retry_count += 1
            tqdm.write(f"Error downloading {font_name}: {e}")
            if retry_count < max_retries:
                tqdm.write(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                tqdm.write(f"Failed to install {font_name} after {max_retries} attempts.")
                break


def get_install_dir():
    system = platform.system()
    if system == "Linux":
        install_dir = Path.home() / ".fonts"
    elif system == "Darwin":  # macOS
        install_dir = Path.home() / "Library/Fonts"
    elif system == "Windows":
        install_dir = Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'Windows' / 'Fonts'
    else:
        raise OSError(f"Unsupported operating system: {system}")
    return install_dir


API_URL = "https://api.github.com/repos/google/fonts/contents/ofl"


def install_fonts(names: list[str], force=False):
    """
    Install predefined fonts.
    """
    # 根据操作系统确定字体安装目录
    install_dir = get_install_dir()
    all_list_to_download = []
    # 创建字体目录（如果不存在的话）
    os.makedirs(install_dir, exist_ok=True)

    tqdm.write("Fetching fonts formulas from https://api.github.com/repos/google/fonts/contents/ofl")
    ofl_list = fetch_ofl_list_json(API_URL)
    tqdm.write("Successfully fetched fonts formulas")

    all_font_names = get_font_names(ofl_list)

    for name in names:
        if name not in all_font_names and not force:
            print(f"\033[31m{name}\033[0m not found in ofl_list")
            print("\033[33mUsing following command to see font list: `google-fonts list`\033[0m")
            return exit(-1)
        for item in fetch_ttf_url_download_list_by_name(ofl_list, name, force=force):
            all_list_to_download.append(item)
    for item in all_list_to_download:
        download_and_install_font(item["name"], item["download_url"], install_dir)


def install_all_fonts():
    ofl_list = fetch_ofl_list_json()
    all_fonts = get_font_names(ofl_list)
    install_fonts(all_fonts)
