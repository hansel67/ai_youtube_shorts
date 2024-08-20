import requests, os
import browser_cookie3
import urllib.request

# Extract cookies from Firefox
cj = browser_cookie3.firefox()

def read_file_to_list(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Remove newline characters from each line
            lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        print("Url list not found.")
        return []

def download_images(project_directory_path):
    url_list_path = os.path.join(project_directory_path,"url_list.txt")
    url_list = read_file_to_list(url_list_path)
    session = requests.Session()
    session.cookies.update(cj)
    for i,image_url in enumerate(url_list):
        print(f"Downloading image {i+1}/{len(url_list)}...",end="")
        response = session.get(image_url)
        if response.status_code == 200:
            name = os.path.join(project_directory_path,"images",f'downloaded_image_{i}.jpg')
            urllib.request.urlretrieve(image_url, name)
            print("done.")
        else:
            print("Failed to retrieve the image. Status code:", response.status_code)