from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pickle
import os


durl= "https://archive.thehated3.workers.dev/0:/Station%20X%20-%20The%20Complete%20Cyber%20Security%20Course!/"

dpath="./Station_X_The_Complete_Cyber_Security_Course"

count=0
rcount=0
failed_links=[]
failed_paths=[]

def download(url,path):
    global count, failed_links, failed_paths
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument("--headless")
    # brower = webdriver.Firefox(firefox_options=fireFoxOptions)

    driver = webdriver.Firefox(executable_path="./geckodriver.exe",options=fireFoxOptions)
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

    try:
        element = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME, "list-group-item")))
    except:
        count+=1
        print(f"FILE NOT DOWNLOADED:\npath: {path}\n count:{count}")
        print("TIMEOUT not LOADING ELEMENTS BY CLASS NAME list-grout-items EXCEPTION")
        return

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
        # cmd=f'wget -c -P '+'"'+f'{path}'+'" '+'"'+ f'{x}'+'"'
        print(f"****DOWNLOADING IN PATH****: {path}\nfiles_skipped_till_now={count} \n\n")
        failure=os.system(f"""wget -c -P "{path}" "{x}" """)
        if failure != 0:
            count+=1
            failed_links.append(x)
            failed_paths.append(path)
            print(f"FILE NOT DOWNLOADED:\npath: {path}\nfile: {x}\n count:{count}")

    driver.close()


def direct_download(dd_url,dd_path):
    rfc=os.system(f"""wget -c -P "{dd_path}" "{dd_url}" """)
    return rfc

def retry():
    global rcount
    new_links=[]
    new_paths=[]
    rcount=0
    try:
        failed_file_open=open("failed_links_info.pickle","rb")
    except:
        print('failed_links_info NOT Available, ABORTING...')
        return
       
    get_failed=pickle.load(failed_file_open)
    fetch_links=get_failed[0]
    fetch_paths=get_failed[1]
    failed_file_open.close()

    link_size=len(fetch_links)

    for k in range(link_size):
        l=fetch_links[k]
        p=fetch_paths[k]
        status=direct_download(l,p)
        if status!=0:
            rcount+=1
            new_links.append(l)
            new_paths.append(p)
            print(f"FILE NOT DOWNLOADED:\npath: {p}\nfile: {l}\n count:{rcount}")

    print(f"Number of files not downloaded: {rcount}")
    nf=len(new_paths)
    o_again=open("failed_links_info.pickle","wb")
    m_list=[new_links,new_paths]
    pickle.dump(m_list,o_again)
    o_again.close()

    for e in range(nf):
        ww=new_paths[e]
        tt=new_links[e]
        print(f"{ww}\n{tt}\n\n")





if __name__=='__main__':
    
    ui=input("Choose:\n1.Retry failed downloads\n2.Download from new link provided\nChoose either '1' or ('2') :")
    if ui==1 or ui=='1':
        retry()
    else:
        download(durl,dpath)
        print(f"Number of files not downloaded: {count}")
        number_failed=len(failed_paths)
        fo=open("failed_links_info.pickle","wb")
        combined_list=[failed_links,failed_paths]
        pickle.dump(combined_list,fo)
        fo.close()

        for i in range(number_failed):
            a=failed_paths[i]
            b=failed_links[i]
            print(f"{a}\n{b}\n\n")

        user_input=input("Do you want to retry {count} failed downloads? (Y)/N : ")
        if user_input.lower()=='n':
            pass
        else:
            retry()

    # print(turl)