from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from elevate import elevate
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

elevate()
run_frep = True
src_dir= os.path.join(os.curdir , "proxy")
dst_dir= os.curdir
src_file = os.path.join(src_dir, "proxy_0.txt")
shutil.copy(src_file,dst_dir)
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

def proxy_driver(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    #fp.set_preference("network.proxy.type", 1)
    #fp.set_preference("network.proxy.socks",PROXY_HOST)
    #fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))
    #fp.update_preferences()
    options = Options()
    options.headless = False
    return webdriver.Firefox(options=options, firefox_profile=fp)

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        cid = sys.argv[i]
        try:
            #hidemy.name
            country = str(countries_dict[cid])
            filename = "proxy/proxy_" + str(cid) + ".txt"  
            file = open(filename, 'w')
            driver = proxy_driver("80.64.172.68", "4145")
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
            if run_frep == True:
                driver = proxy_driver("80.64.172.68", "4145")
                try:
                    driver.get("http://free-proxy.cz/ru/proxylist/country/" + country + "/socks4/ping/all")
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
                                    sleep(random.randrange(0.2, 1))
                        else:
                            print("На free-proxy.cz нет серверов для {}".format(country))
                            log.write("На free-proxy.cz нет серверов для {} \n".format(country))
                    if cunt > 0:
                        print ("Cобрано {} серверов для {} с free-proxy.cz. Обработано {} из {}.".format(cunt, country, i, len(sys.argv))) 
                        log.write("Cобрано {} серверов для {} c free-proxy.cz \n".format(cunt, country))
                except Exception:
                    print("Невозможно подключиться к free-proxy.cz.")
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
