import os
import pandas as pd
import numpy as np
from selenium import webdriver
import time
import tqdm
'''
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')
options.add_argument('headless')
driver = webdriver.Chrome('./chromedriver', options = options)
driver.close() #현재 탭 닫기
driver.quit()  #브라우저 닫기
'''
'''
trans_dict = {}
intr_list = pd.read_csv('unicode_artist_list.csv')
for i, j in intr_list.values:
    trans_dict[i.strip()] = j.strip()
data0 = pd.read_csv('wikiart_test_1205.csv')
data1 = pd.read_csv('wikiart_train_1205.csv')
data0['t_type'] = 'test'
data1['t_type'] = 'train'
data = pd.concat((data0, data1))
_list = []
for i in range(len(data)):
    artist = data.path.values[i].split('/')[1].split('_')[0]
    name = '_'.join(data.path.values[i].split('/')[1].split('_')[1:])
    name = os.path.splitext(name)[0]
    if artist in list(intr_list.keys()):
        artist = intr_list[artist]
    _list.append([artist, name])
data[['artist','name']] = _list
data.to_csv('./wikiart_data.csv')
'''

data = pd.read_csv('wikiart_data.csv')

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome('./chromedriver', options = option)
time.sleep(5)
res_data = {}
ii = 0
for ii in tqdm.tqdm(range(len(data))):
    artist = data.artist.values[ii]
    name = data.name.values[ii]

    painting = artist + '_' + name
    res_data[painting] = {}

    _path = painting.replace('_', '/')
    path = 'https://www.wikiart.org/en/'+_path

    try:
        driver.get(path)
        item_list = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/section[1]/main/div[2]/article/h3')
        for i in range(len(item_list)):
            res_data[painting]['name'] = item_list[i].text.strip()

        item_list = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/section[1]/main/div[2]/article/h5/span/a')
        for i in range(len(item_list)):
            res_data[painting]['artist'] = item_list[i].text.strip()

        item_list = driver.find_elements_by_class_name('dictionary-values')
        for i in item_list:
            cls, val = i.text.split(':')
            res_data[painting][cls.strip()] = val.strip()

        item_list = driver.find_elements_by_class_name('tags-cheaps__item__ref')
        res_data[painting]['tag'] = []
        for i in item_list:
            res_data[painting]['tag'].append(i.text)

        item_list = driver.find_elements_by_class_name('wiki-layout-artist-info-tab-switch')
        item_list2 = driver.find_elements_by_class_name('wiki-layout-artist-info-tab')
        for idx in range(len(item_list2)):
            item_list[idx].click()
            res_data[painting][f'wiki_{idx}'] = item_list2[idx].text
            time.sleep(0.1)
        res_data['except'] = False

    except:
        #print(f'except url at {painting}')
        res_data['except'] = True
        pass

    time.sleep(0.1)
    if ii % 100 == 0:
        print(ii)
    if ii % 100 == 0:
        np.save(f'wiki_crawl_result_{ii}.npy', res_data)