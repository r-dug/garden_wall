import os
import time
required_packages = ["requests", "fake_useragent","selenium", "webdriver_manager"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        os.system(f"pip install {package}")

        os.system(f"pip install {package}")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import requests
import csv
import random



def create_path_list(csv_file):
    path_list = []
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if count == 1:
                url = row[0]
                name = row[-1].replace(' ', '_')
                path_list.append((url, name))
            else:
                count+=1
    return path_list

def dl_image(src, dir, name, count):
    response = requests.get(src)
    if not os.path.isdir(f"./{dir}/{name}"):
        os.mkdir(f"./{dir}/{name}")

    try:
        with open(f"{dir}/{name}/{name}_{count}.jpg", "xb") as f:
            f.write(response.content)
    except Exception as e:
        print(e)

def main():
    csv_files = ["observations-446690.csv"]
    ua = UserAgent()
    user_agent = ua.random
    options = Options()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    img_count = 0
    for file in csv_files:
        
        path_list = create_path_list(file)
        for path in path_list:
            if img_count >= 1000:
                break
            driver.get(path[0])
            dl_image( path[0], "pest_images", path[1], img_count)
            img_count += 1
main()