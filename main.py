import os
import threading
import requests
import json
import sys

directory_name = "site_0B4564C9-B0CF-41D8-8AB0-78866006109F"
root = "/Users/"
URL = "https://test-util.sitetraxx.com/api/clock/lookup/"
counter = 0

def find_directory(directory_name, root_directory):
    for root, dirs, files in os.walk(root_directory):
        if directory_name in dirs:
            return os.path.join(root, directory_name)

    return None

def jpg_thread(folder_path, batch_size):
    files = [file for file in os.listdir(folder_path) if file.endswith(".jpg")]

    file_batches = [files[i:i+batch_size] for i in range(0, len(files), batch_size)]

    for batch in file_batches:
        thread = threading.Thread(target = process_items, args=(batch, folder_path))
        thread.start()
        thread.join()

def test_jpg(folder_path):
    files = [file for file in os.listdir(folder_path) if file.endswith(".jpg")]
    slice = files[:50]
    return slice
def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the request: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error occurred: {e.response.status_code} - {e.response.reason}")
    except json.JSONDecodeError as e:
        print(f"Error occurred while decoding JSON: {e}")
    else:
        response_text = response.text
        return response_text

def process_items(items, directory_path):
    dates = []
    for item in items:
        x = item.split("_")
        y = x[1]
        url = URL + y
        response = get_response(url)
        dates.append(response)

    for date in dates:
        if date == '':
            if not os.path.exists(os.path.join(directory_path, date)):
                path = os.path.join(directory_path, "trash")
                os.makedirs(path, exist_ok = True)
        else:
            if not os.path.exists(os.path.join(directory_path, date[:4])):
                path = os.path.join(directory_path, date[:4])
                os.makedirs(path, exist_ok = True)

    for date in dates:
        if date == '':
            pass
        else:
            if not os.path.exists(os.path.join(os.path.join(directory_path, date[:4]), date)):
                path = os.path.join(directory_path, os.path.join(date[:4], date))
                os.makedirs(path, exist_ok = True)

    for x, item in enumerate(items):
        new_path = os.path.join(os.path.join(directory_path, os.path.join(dates[x][:4], dates[x])), item)
        old_path = os.path.join(directory_path, item)
        os.rename(old_path, new_path)



if __name__ == '__main__':
    batch_size = 50
    if len(sys.argv) > 1:
        directory_name = sys.argv[1]
        directory_path = find_directory(directory_name, root)
        if directory_path:
            print(f"Directory found {directory_path}")
        else:
            print(f"Directory '{directory_name}' not found")
        jpg_thread(directory_path, batch_size)
    else:
        print("No arguments found")
        sys.exit(1)
