import requests
from tqdm import tqdm
import schedule
import time
from datetime import datetime, timedelta
from halo import Halo
import threading

spinner_lock = threading.Lock()

def download_file(url, output_path, spinner):
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 102400  # 100 Kilobytes

            spinner.stop()
            with tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True) as progress_bar:
                with open(output_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)
            
            spinner.start()
    except requests.RequestException as e:
        with spinner_lock:
            spinner.stop()
            print("\nAn error occurred: {e}\n")
            spinner.start()
        return False
    except Exception as e:
        with spinner_lock:
            spinner.stop()
            print("\nAn error occurred: {e}\n")
            spinner.start()
        return False
    return True

def perform_download(url, output_file, spinner):
    with spinner_lock:
        spinner.stop()
        print("\nDownloading file...\n")
        spinner.start()
    success = download_file(url, output_file, spinner)
    if success:
        with spinner_lock:
            spinner.stop()
            print("\nDownload completed successfully.\n")
            spinner.start()
    else:
        with spinner_lock:
            spinner.stop()
            print("\nDownload failed.\n")
            spinner.start()

def scheduled_download():
    url = "https://images.dhan.co/api-data/api-scrip-master.csv"
    output_file = "sym.csv"

    spinner = Halo(text='Initializing scheduler...', spinner='dots')
    spinner.start()

    def download_thread():
        perform_download(url, output_file, spinner)

    schedule.every().day.at("09:00").do(download_thread)

    try:
        while True:
            schedule.run_pending()
            next_run = schedule.next_run()
            remaining_time = next_run - datetime.now()
            with spinner_lock:
                spinner.text = f'Next download at {next_run.strftime("%Y-%m-%d %H:%M:%S")}. Remaining: {str(remaining_time).split(".")[0]}'
            time.sleep(1)
    except KeyboardInterrupt:
        with spinner_lock:
            spinner.stop()
            print("\nScheduler stopped.\n")
    finally:
        spinner.stop()

if __name__ == "__main__":
    scheduled_download()
