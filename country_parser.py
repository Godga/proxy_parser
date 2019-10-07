from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from elevate import elevate
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import lxml.html
import re
import sys
import os
import shutil
from time import sleep
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from stem import Signal
from stem.control import Controller
import random
import requests
import json
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

elevate()

proxy = 0
options = Options()
options.headless = True #запуск браузера в headless режиме
hidemy = True #Сбор прокси с hidemy.name
freeproxy = False #Сбор прокси с free-proxy.cz
using_proxy = False

if (os.stat("proxy_0.txt").st_size > 0 and using_proxy == True):
    try:
        if (os.stat("proxy/proxy_0.txt").st_size > 0):
            src_dir= os.path.join(os.curdir , "proxy")
            dst_dir= os.curdir
            src_file = os.path.join(src_dir, "proxy_0.txt")
            shutil.copy(src_file,dst_dir)
        with open('proxy_0.txt') as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        myproxy = random.choice(content)
        myproxy = re.match("(([\d]{1,3}\.?){4})\:(([\d]{1,10}))", myproxy)
        print("Используем прокси ", myproxy.group(0))
        full_proxy = myproxy.group(0)
        proxy_ip = myproxy.group(1)
        proxy_port = myproxy.group(3)
        print(proxy_ip + "\n" + proxy_port + "\n" + full_proxy)
        user_a = "Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"
        #cap["marionette"] = False
        #profile = webdriver.FirefoxProfile()
        #profile.set_preference("network.proxy.type", 1)
        #profile.set_preference("network.proxy.http", str(proxy_ip))
        #profile.set_preference("network.proxy.http_port", int(proxy_port))
        #profile.set_preference("network.proxy.ssl", str(proxy_ip))
        #profile.set_preference("network.proxy.ssl_port", int(proxy_port))
        #profile.set_preference("network.proxy.ftp", str(proxy_ip))
        #profile.set_preference("network.proxy.ftp_port", int(proxy_port))
        #profile.set_preference("network.proxy.socks", str(proxy_ip))
        #profile.set_preference("network.proxy.socks_port", int(proxy_port))
        #profile.set_preference("network.proxy.socks_version", 4)
        #profile.set_preference("network.http.use-cache", False)
        #profile.set_preference("general.useragent.override", user_a)
        #profile.update_preferences()
        #binary = FirefoxBinary("C:\Program Files\Mozilla Firefox")
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.auto_detect = False   
        proxy.http_proxy = str(full_proxy)
        proxy.socks_proxy = str(full_proxy)
        proxy.socks_version = int(4)
        proxy.ssl_proxy = str(full_proxy)
        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities)
        
        driver = webdriver.Chrome(desired_capabilities=capabilities)
        
        driver.get("http://ip-api.com/json/")
        #driver.get("https://hidemy.name/ru/proxy-list/?country=RU&maxtime=2000&type=4&anon=34&end=9999#list")
        response = json.loads(driver.find_element_by_xpath("*").text)
        print(response["query"])
        #driver.close()
    except Exception as exc:
        print('{}: {}'.format(type(exc).__name__, exc))
        #driver.close()
        sleep(10)
        pass
else:
    print("отключено прокси или пустой файл")
countries_dict = {
    "0":"RU",
    "1":"UA",
    "2":"KZ",
    "3":"CN",
    "4":"PH",
    "5":"MM",
    "6":"ID",
    "7":"MY",
    "8":"KE",
    "10":"VN",
    "11":"KG",
    "12":"US",
    "13":"IL",
    "14":"HK",
    "15":"PL",
    "16":"GB",
    "17":"MG",
    "19":"NG",
    "20":"MO",
    "21":"EG",
    "22":"IN",
    "23":"IE",
    "24":"KH",
    "31":"ZA",
    "33":"CO",
    "36":"CA",
    "37":"MA",
    "38":"GH",
    "44":"LT",
    "45":"HR",
    "48":"NL",
    "49":"LV",
    "55":"TW",
    "58":"DZ",
    "63":"CZ",
    "65":"PE",
    "68":"GN",
    "67":"NZ",
    "70":"VE"
}


log = open("log.txt", 'w')
countries = ""


if (len(sys.argv) > 1 and (hidemy or freeproxy)):
    for i in range(1, len(sys.argv)):
        cid = sys.argv[i]
        try:
            filename = "proxy/proxy_" + str(cid) + ".txt"
            file = open(filename, 'w')
            if hidemy == True:
                #hidemy.name
                country = str(countries_dict[cid])
                filename = "proxy/proxy_" + str(cid) + ".txt"  
                file = open(filename, 'w')
                if (proxy):
                    driver = webdriver.Firefox(options=options)
                else:
                    driver = webdriver.Firefox(options=options)
                driver.get("https://hidemy.name/ru/proxy-list/?country=" + country + "&maxtime=2000&type=4&anon=34&end=9999#list")
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'headline proxy_headline')]"))
                    )
                finally:
                    elements = driver.find_element_by_tag_name("tbody").text
                    #root = lxml.html.fromstring(elements)
                    #arr = root.xpath('//tr/td//text()')
                    cunt = 0
                    if elements != "":
                        reg = re.findall('(([\d]{1,3}\.?){4})\s([\d]{1,10})', elements)              
                        for elem in reg:
                            res = str(elem[0]) + ":" + elem[2] + ":socks4 \n"
                            file.write(res)
                            cunt += 1
                    #assert "No results found." not in driver.page_source
                    if cunt > 0:
                        print ("Cобрано {} серверов для {} c hidemy.name".format(cunt, country))
                        log.write("Cобрано {} серверов для {} c hidemy.name \n".format(cunt, country))
                    else:
                        print("На hidemy.name нет серверов для {}".format(country))
                        log.write("На hidemy.name нет серверов для {} \n".format(country))
                    driver.close()

            #free-proxy.cz
            if freeproxy == True:
                if (proxy):
                    driver = webdriver.Firefox(options=options)
                else:
                    driver = webdriver.Firefox(options=options)
                try:
                    driver.get("http://free-proxy.cz/ru/proxylist/country/" + country + "/socks4/ping/all")
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'paginator')]"))
                        )
                    finally:
                        elems = driver.find_elements_by_xpath("//div[contains(@class, 'paginator')]")
                        if len(elems) == 0:
                            count = 1
                        else:
                            count = driver.find_element_by_xpath("//div[contains(@class, 'paginator')]").find_elements_by_tag_name("a")
                            count = len(count)
                        cunt = 0
                        for list in range(1, count+1):
                            driver.get("http://free-proxy.cz/ru/proxylist/country/" + country + "/socks4/ping/all/" + str(list))
                            #assert "hidemy" in driver.title
                            elem = driver.find_elements_by_xpath(".//*[@id='clickexport']")
                            if len(elem) > 0:                        
                                driver.find_element_by_id("clickexport").click()
                                elements = driver.find_element_by_id("zkzk").text
                                if elements != "":
                                    reg = re.findall('(([\d]{1,3}\.?){4})\:([\d]{1,10})', elements)
                                    for elem in reg:
                                        res = str(elem[0]) + ":" + elem[2] + ":socks4 \n"
                                        file.write(res)
                                        cunt += 1
                                        sleep(random.randrange(int(0.2), int(1)))
                            else:
                                print("На free-proxy.cz нет серверов для {}".format(country))
                                log.write("На free-proxy.cz нет серверов для {} \n".format(country))
                        if cunt > 0:
                            print ("Cобрано {} серверов для {} с free-proxy.cz. Обработано {} из {}.".format(cunt, country, i, len(sys.argv))) 
                            log.write("Cобрано {} серверов для {} c free-proxy.cz \n".format(cunt, country))
                except Exception as e:
                    print(repr(e))
                    log.write("Невозможно подключиться к free-proxy.cz.")
                    run_frep = False
                driver.close()
                file.close()        
        except KeyError as e:
            log.write('Несуществующий ID: {} \n'.format(cid))
            #time.sleep(2)        
else: 
    log.write("Please enter country ID")
log.write("выполнено успешно \n")
log.close()
