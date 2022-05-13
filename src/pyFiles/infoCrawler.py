import sys 
import io 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# 나중에 따로 분리하기
uk_british = 'https://www.britishmuseum.org/exhibitions-events'
fr_pompidou = 'https://www.centrepompidou.fr/en/'
uk_londonNatl = "https://www.nationalgallery.org.uk/exhibitions"
us_cincinnati = 'https://www.cincinnatiartmuseum.org/art/exhibitions/?gclid=Cj0KCQjw3v6SBhCsARIsACyrRAlU8C9ymrvNSV-ts7ZSz3C6QGU7ctlrzUOwSSRAMgeCD2Po5DSI7L0aAsxFEALw_wcB'
es_prado = 'https://www.pradomuseumtickets.com/prado-museum-exhibitions/'
at_wien = 'https://www.wienmuseum.at/en/exhibitions/current-exhibitions'
at_belvedere = 'https://www.belvedere.at/ausstellungen-aktuell'
fr_orsay = 'https://www.musee-orsay.fr/fr'
fr_lodin = 'https://www.musee-rodin.fr/musee/expositions'
us_chicago = 'https://www.artic.edu/exhibitions'
es_thyssen = 'https://www.museothyssen.org/en/exhibitions'
es_guggenheim = 'https://www.guggenheim-bilbao.eus/exposiciones'
es_malagaAutomovil = 'https://www.cristobalbalenciagamuseoa.com/descubre/exposiciones-actuales/'
it_ducale = 'https://palazzoducale.visitmuve.it/category/en/mostre-en/mostre-in-corso-en/'


def print_msm_data(url, exb_nums, titles_selector, dates_selector, thumbnails_selector, details_links_selector, details_content_selector):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome('C:\JaeGyeong\codedriver\chromedriver', options=options)
    
    driver.implicitly_wait(10)
    driver.get(url)
    driver.set_window_position(0, 0)
    driver.set_window_size(3000, 1000)
    global exb_titles
    global exb_dates
    global exb_thumbnails
    global exb_details_links
    global exb_details

    exb_titles, exb_dates, exb_thumbnails = [], [], []
    
    # 쿠키 알람 처리
    if url == uk_british:
        driver.find_element(by=By.CSS_SELECTOR, value="#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
    if url == es_guggenheim:
        driver.find_element(by=By.CSS_SELECTOR, value="#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
    if url == at_belvedere:
        driver.find_element(by=By.CSS_SELECTOR, value="#select-all-cookies-btn").click()
    if url == es_malagaAutomovil:
        driver.find_element(by=By.CSS_SELECTOR, value=".icon__glyph").click()
        driver.execute_script("window.scrollTo(0, 1000)")
    def load_data():
        global exb_titles
        global exb_dates
        global exb_thumbnails

        
        time.sleep(1)
        exb_titles = driver.find_elements(by=By.CSS_SELECTOR, value=titles_selector)
        exb_dates = driver.find_elements(by=By.CSS_SELECTOR, value=dates_selector)
        exb_thumbnails = driver.find_elements(by=By.CSS_SELECTOR, value=thumbnails_selector)
        
    load_data()
    exb_details_links = driver.find_elements(by=By.CSS_SELECTOR, value=details_links_selector)
    exb_details = []

    def load_details_and_mediate_numbers():
        global exb_titles
        global exb_dates
        global exb_thumbnails
        global exb_details
        global exb_details_links
        
        
        # 디테일 데이터 조정
        for i in range(exb_nums):
            # 전시 개별 링크 들어가지 않아도 되는 사이트들 처리
            time.sleep(1)
            if url in [us_cincinnati, es_prado, es_malagaAutomovil, it_ducale]:
                exb_details = [x.text for x in exb_details_links]
                break
            if url in [es_thyssen]:
                break

            exb_details_links = driver.find_elements(by=By.CSS_SELECTOR, value=details_links_selector)
            driver.implicitly_wait(3)
            driver.get(exb_details_links[i].get_attribute("href"))
            detail = ""

            if url == at_wien:
                if i == 0:
                    detail = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, details_content_selector)))
                else:
                    detail = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#main p")))
            else:
                detail = driver.find_element(by=By.CSS_SELECTOR, value=details_content_selector)
                # detail = WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, details_content_selector)))
            exb_details.append(detail.text)
            driver.get(url) # back
        
        # 타이틀, 날짜 데이터 조정
        load_data()
        exb_titles = exb_titles[:exb_nums]
        exb_dates = exb_dates[:exb_nums]

        
        # 썸네일 데이터 조정
        if url == uk_british:
            exb_thumbnails = ["https://www.britishmuseum.org" + x.get_attribute("data-srcset").split("h=")[0] for x in exb_thumbnails]
            exb_thumbnails = exb_thumbnails[:exb_nums]
        elif url == uk_londonNatl:
            exb_thumbnails = [x.get_attribute("style").strip("\"background-image: url(") for x in exb_thumbnails]
            exb_thumbnails = ["https://www.nationalgallery.org.uk/" + x[:x.find(".jpg?") + 4] for x in exb_thumbnails]
            exb_thumbnails = exb_thumbnails[:exb_nums]
        elif url == es_prado:
            exb_thumbnails = [x.get_attribute("data-srcset") for x in exb_thumbnails]
            exb_thumbnails = exb_thumbnails[:exb_nums]    
        elif url == us_chicago:
            exb_thumbnails = [x.get_attribute("data-pin-media") for x in exb_thumbnails]
            exb_thumbnails = exb_thumbnails[:exb_nums]
        elif url == it_ducale:
            exb_thumbnails = [x.get_attribute("style") for x in exb_thumbnails]
            exb_thumbnails = [x[x.find("url(") + 5:-3] for x in exb_thumbnails]
            exb_thumbnails = exb_thumbnails[:exb_nums]
        
        else:
            exb_thumbnails = [x.get_attribute("src") for x in exb_thumbnails]
            exb_thumbnails = exb_thumbnails[:exb_nums]

    load_details_and_mediate_numbers()
    
    for title in exb_titles:
        print("[TITLE]", title.text)
        print("SPLITER")
    print("FILTER")
    for date in exb_dates:
        print("[DATE]", date.text)
        print("SPLITER")
    print("FILTER")
    for thumbnail_src in exb_thumbnails:
        print(thumbnail_src)
        print("SPLITER")
    print("FILTER")
    for detail in exb_details:
        print("[DETAIL]", detail)
        print("SPLITER")
    print("FILTER")

    driver.close()