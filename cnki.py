import urllib.request as request
import os, re
import random
import pickle
#headers = {
#      'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                    r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
#      'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
#      'Connection': 'keep-alive'
#}


#web = request.urlopen('http://apps.webofknowledge.com/Search.do?product=UA&SID=Y25Llq5bM9S3NMVP8Wu&search_mode=GeneralSearch&prID=92344662-ef80-4852-b81a-b02d702aa99e')
#i = 0
#flag = 0
#text = []
#for line in web:
#    line = line.decode('utf-8')
#    if re.search(line, 'smallV110'):
#        flag = 1
#        i += 1
#        text.append([])
#    text(i).append(line)
#print(text)
#aaa = 0

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select

class paper:
    def __init__(self, name, attribute, references, year):
        self.name = name
        for element in attribute:
            if re.match('ժҪ',element):
                self.abstract = element
            if re.match('����\:',element):
                self.author = element
            if re.match('�ؼ���',element):
                self.key = element
            if re.match('���',element):
                self.cata = element
            if re.match('������Ϣ',element):
                self.refer = element
        self.references = references
        self.year = year
    def organize(self):
        print(self.name)
        self.abstract = self.abstract.splitlines()[1]
        authors = self.author.split('(')
        authors[0] = authors[0].split(':')[1]
        self.author = []
        self.author.append(authors[0])
        for author in authors:
            try:
                author = author.split('; ')[1]
                self.author.append(author)
            except:
                continue
        self.cata = self.cata.splitlines()[1]
        self.cata = self.cata.split(':')[1]
        self.cata = self.cata.split('; ')
        try:
            self.key = self.key.splitlines()[1]
            self.key = self.key.split(':')[1]
            self.key = self.key.split('; ')
        except:
            self.key = []
        self.refer = self.refer.splitlines()
        for line in self.refer:
            if line.find('���õĲο�����') != -1:
                self.refers = int(line.split(':')[1])
            if line.find('����Ƶ��') != -1:
                self.refered = int(line.split(':')[1])
    def breed(self):
        dic = {}
        dic['name'] = self.name
        try:
            dic['key'] = self.key
        except:
            dic['key'] = []
        dic['cata'] = self.cata
        dic['refers'] = self.refers
        dic['refered'] = self.refered
        dic['author'] = self.author
        dic['abstract'] = self.abstract
        dic['year'] = self.year
        dic['references'] = self.references
        first = self.name[0]
        return [first, dic]


class store:
    def __init__(self):
        self.all = {}
        self.all['num'] = 0
        for i in range(1996,2018):
            self.all[str(i)] = {}
            self.all[str(i)]['other'] = []
            self.all[str(i)]['key'] = {}
            self.all[str(i)]['reference'] = {}
            for j in range(65,91):
                self.all[str(i)][chr(j)] = []
    def write(self):
        output = open('data.pkl', 'wb')
        pickle.dump(self.all, output)
        output.close()
    def input(self, dic):
        self.all['num'] += 1
        try:
            char = dic[0].capitalize()
            year = dic[1]['year']
            self.all[year][char].append(dic[1])
        except:
            self.all[year]['other'].append(dic[1])
        for key in dic[1]['key']:
            try:
                self.all[str(i)]['key'][key] += 1
            except:
                self.all[str(i)]['key'][key] = 1
        for reference in dic[1]['references']:
            try:
                self.all[str(i)]['references'][reference] += 1
            except:
                self.all[str(i)]['references'][reference] = 1



#firefox_profile = webdriver.FirefoxProfile()
#firefox_profile.set_preference('permissions.default.stylesheet', 2)
#firefox_profile.set_preference('permissions.default.image', 2)
#firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
#driver = webdriver.Firefox(firefox_profile)
#driver.set_page_load_timeout(30)
firefoxProfile = webdriver.FirefoxProfile()
firefoxProfile.set_preference("permissions.default.stylesheet",2)
firefoxProfile.set_preference("permissions.default.image",2)
firefoxProfile.update_preferences()

storehouse = store()
#dcap = dict(DesiredCapabilities.PHANTOMJS)
#dcap["phantomjs.page.settings.loadImages"] = False  # ��ֹ����ͼƬ,Ĭ�ϼ���
#driver = webdriver.PhantomJS(desired_capabilities = dcap)
driver = webdriver.Firefox()
time.sleep(3)
web = driver.get("http://kns.cnki.net/kns/brief/result.aspx?dbprefix=scdb")
element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('selectW1'))
Select(driver.find_element_by_id("txt_1_sel")).select_by_value('SU')
Select(driver.find_element_by_id("txt_1_relation")).select_by_value('#CNKI_NOT')
Select(driver.find_element_by_id("txt_2_logical")).select_by_value('not')
input = driver.find_element_by_id("txt_1_value1")
input.clear()
input.send_keys('超级电容')
input = driver.find_element_by_id("txt_1_value2")
input.clear()
input.send_keys('化学')
input = driver.find_element_by_id("txt_2_value1")
input.clear()
input.send_keys('材料')
driver.find_element_by_id("btnSearch").click()
element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id('iframeResult'))
driver.switch_to.frame('iframeResult')
element = WebDriverWait(driver, 5).until(lambda x: x.find_elements_by_class_name('fz14'))
#time.sleep(5)
papers = driver.find_elements_by_class_name('fz14')
searchhandle = driver.current_window_handle
time.sleep(0.1)
for link in papers:
    link.click()
    time.sleep(0.1)
    handles = driver.window_handles
    linkhandle = handles[-1]
    time.sleep(0.1)
    #linkhandle = driver.window_handles[-1]
    driver.switch_to_window(linkhandle)
    linkhandle = driver.current_window_handle
    #element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('title'))
    title = driver.find_element_by_class_name('title').text
anum = 0
alltime = int(time.time())
error = 0
for searchpage in range(1,100):
    linkstarttime = 0
    linktime = 0
    t = int(time.time())
    time.sleep(3)
    print('page = ' + str(searchpage))
    searchurl = driver.current_url
    links = []
    contents = driver.find_elements_by_id('records_chunks')
    thispage = driver.find_elements_by_class_name('smallV110')
    thispageurl = []
    for element in thispage:
        thispageurl.append(element.get_attribute("href"))
    for i in range(19,9,-1):
        try:
            del(thispageurl[i])
        except:
            continue
    for link in thispageurl:
        anum += 1
        print('article = ' + str(anum))
        flag = 0;
        linkstarttime = int(time.time())
        driver.get(link)
        try:
            element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('block-record-info'))
        except:
            error += 1
            print('error = ' + str(error))
            driver.quit()
            firefoxProfile = webdriver.FirefoxProfile()
            firefoxProfile.set_preference("permissions.default.stylesheet",2)
            firefoxProfile.set_preference("permissions.default.image",2)
            firefoxProfile.update_preferences()
            driver = webdriver.Firefox(firefoxProfile)
            driver.get(link)
            element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('block-record-info'))
        #time.sleep(2*random.random())
        linktime = int(time.time()) - linkstarttime
        title = driver.find_elements_by_class_name('title')
        title = title[0].text
        if re.search('\s?\-?[A-Z][a-z]?\d?[A-Z]', tltle):
            continue
        if re.search('electrochemical' , tltle):
            continue
        if re.search('electrode material' , title):
            continue
        recordtemp = driver.find_elements_by_class_name('block-record-info')
        attribute = []
        for element in recordtemp:
            text = element.text
            attribute.append(text)
            if re.match('���', text):
                if re.search('Engineering', text):
                    flag = 1
        if flag == 0:
            continue
        elements = driver.find_elements_by_class_name('FR_field')
        for element in elements:
            if element.text.find('������') != -1:
                years = element.text.split(':')[1]
                years = years.split()
                for thing in years:
                    if re.match('\d{4}', thing):
                        year = thing
        reference = driver.find_element_by_css_selector("a[title='�鿴�˼�¼����¼��Ϣ']")
        reflink = reference.get_attribute("href")
        #time.sleep(2*random.random())
        #driver.close()
        linkstarttime = int(time.time())
        driver.get(reflink)
        try:
            element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('smallV110'))
        except:
            error += 1
            print('error = ' + str(error))
            driver.quit()
            firefoxProfile = webdriver.FirefoxProfile()
            firefoxProfile.set_preference("permissions.default.stylesheet",2)
            firefoxProfile.set_preference("permissions.default.image",2)
            firefoxProfile.update_preferences()
            driver = webdriver.Firefox(firefoxProfile)
            driver.get(reflink)
            element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('smallV110'))
        linktime = linktime + int(time.time()) - linkstarttime
        max = int(driver.find_elements_by_id('pageCount.bottom')[0].text)
        listtemp = []
        list = []
        
        for i in range(1,max+1):
            #page = driver.page_source
            searchtime = int(time.time())
            ref = driver.find_elements_by_class_name('reference-title')
            del(ref[0])
            for j in range(len(ref), int(len(ref)/2), -1):
                del(ref[j-1])
            for name in ref:
                tempyear = name.find_elements_by_xpath('./../..')
                tempyear = tempyear[0].find_elements_by_xpath('.//span[contains(text(),"������:")]')
                tempyear = tempyear[0].find_elements_by_xpath('.//following-sibling::span[1]')[0].text
                tempyear = tempyear.split()
                for thing in tempyear:
                    if re.match('\d{4}', thing):
                        list.append(thing)
                name = name.text
                listtemp.append(name)
            element = driver.find_elements_by_class_name('paginationNext')[1]
            #time.sleep(2*random.random())
            currenturl = driver.current_url
            searchtime = int(time.time()) - searchtime
            print('searchtime = '+str(searchtime))
            linkstarttime = int(time.time())
            element.click(); 
            try:
                WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('reference-title'))
            except:
                error += 1
                print('error = '+str(error))
                driver.quit()
                firefoxProfile = webdriver.FirefoxProfile()
                firefoxProfile.set_preference("permissions.default.stylesheet",2)
                firefoxProfile.set_preference("permissions.default.image",2)
                firefoxProfile.update_preferences()
                driver = webdriver.Firefox(firefoxProfile)
                driver.get(currenturl)
                element.click(); 
                WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('reference-title'))
            linktime = linktime + int(time.time()) - linkstarttime
        #driver.close()
        deli = []
        #for j in range(0,len(listtemp)):
        #    element = listtemp[i]
        #    if re.match('���� Related Records >', element):
        #        deli.append(i)
        #for j in deli[::-1]:
        #    del(listtemp[i])
        #while '' in listtemp:
        #    listtemp.remove('')
        for j in range(0,len(list)):
            list[j] = [list[j], listtemp[j]]
        article = paper(title, attribute, list, year)
        article.organize()
        dic = article.breed()
        storehouse.input(dic)
        #time.sleep(2*random.random())
    #driver.close()
    if searchpage%30 == 0:
        driver.quit()
        firefoxProfile = webdriver.FirefoxProfile()
        firefoxProfile.set_preference("permissions.default.stylesheet",2)
        firefoxProfile.set_preference("permissions.default.image",2)
        firefoxProfile.update_preferences()
        driver = webdriver.Firefox(firefoxProfile)
    linkstarttime = int(time.time())
    driver.get(searchurl)
    try:
        element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id('records_chunks'))
    except:
        error += 1
        print('error = ' + str(error))
        driver.quit()
        firefoxProfile = webdriver.FirefoxProfile()
        firefoxProfile.set_preference("permissions.default.stylesheet",2)
        firefoxProfile.set_preference("permissions.default.image",2)
        firefoxProfile.update_preferences()
        driver = webdriver.Firefox(firefoxProfile)
        driver.get(searchurl)
        element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id('records_chunks'))
    linktime = linktime + int(time.time()) - linkstarttime
    #time.sleep(2*random.random())
    element = driver.find_elements_by_class_name('paginationNext')[1]
    currenturl = driver.current_url
    linkstarttime = int(time.time())
    element.click();
    try:
        element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id('records_chunks'))
    except:
        error += 1
        print('error = ' + str(error))
        driver.quit()
        firefoxProfile = webdriver.FirefoxProfile()
        firefoxProfile.set_preference("permissions.default.stylesheet",2)
        firefoxProfile.set_preference("permissions.default.image",2)
        firefoxProfile.update_preferences()
        driver = webdriver.Firefox(firefoxProfile)
        driver.get(searchurl)
        element.click(); 
        element = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id('records_chunks'))
    linktime = linktime + int(time.time()) - linkstarttime
    #time.sleep(2*random.random())
    t = int(time.time()) - t
    avetime = int(time.time()) - alltime
    avetime = avetime/searchpage
    print('time = ' + str(t))   
    print('avetime = ' + str(avetime))   
    print('linktime = ' + str(linktime))
alltime = int(time.time()) - alltime
print(alltime)
storehouse.write()
driver.quit()