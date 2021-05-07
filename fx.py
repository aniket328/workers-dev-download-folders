from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

import os
import pathlib

durl="https://archive.thehated3.workers.dev/0:/Udemy/Udemy%20-%20Ethical%20Hacking%20-%20Hands-On%20Training%20-%20Part%20I/"
# durl="https://archive.thehated3.workers.dev/0:/Udemy/Udemy%20-%20Certified%20Kubernetes%20Security%20Specialist%202021/01%20Introduction/"
dpath='./Udemy-Ethical-Hacking-Hands-On-Training-Part-1'


def download(url,path):
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    # brower = webdriver.Firefox(firefox_options=fireFoxOptions)

    driver = webdriver.Firefox(executable_path="./geckodriver.exe",firefox_options=fireFoxOptions)
    driver.get(url)

    time.sleep(3)
    previous_height=driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)
        new_height=driver.execute_script('return document.body.scrollHeight')

        if new_height==previous_height:
            break
        previous_height=new_height


    element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "list-group-item")))
    tuna=driver.find_elements_by_class_name("list-group-item")
    dlinks=[]

    for i in tuna:

        folder=i.get_attribute('href')
        if folder==None:
            target_urls=i.find_elements_by_css_selector('a')
            furl=target_urls[1].get_attribute('href')
            dlinks.append(furl)
        else:
            fname=i.text
            formated_folder_name=fname.replace(" ","-")
            new_path=path+"/"+formated_folder_name
            download(folder,new_path)

    for x in dlinks:
        # print(x)
        print(f"downloading in path: {path}")
        os.system(f'wget -c -P {path} {x}')

    driver.close()

if __name__=='__main__':
    download(durl,dpath)