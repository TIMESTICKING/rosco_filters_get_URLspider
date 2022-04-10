import json
import os
import re
import threading
import urllib.request
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pdf_dealer import *

import io
from argparse import ArgumentParser
from bs4 import BeautifulSoup

strange_semaphore = threading.Semaphore(1)


ids = None
out = None

headers = {
    'Host': 'cn.rosco.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36,',
    'Origin': 'https://cn.rosco.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'OptanonAlertBoxClosed=2022-03-28T06:45:04.387Z; _ga=GA1.2.931421663.1648449924; _hjSessionUser_2854874=' \
              'eyJpZCI6IjViNjhiYTRkLTA1OGItNTM0ZC05MzY0LWEyZWQzN2U5YWY5YSIsImNyZWF0ZWQiOjE2NDg0NTA1MDYxNTYsI' \
              'mV4aXN0aW5nIjp0cnVlfQ==; SSESS608e1a59f7ae7f970dc6abee20fc8e1b=VHDukLa0dIvrYlXr_QQN6V8WdsTx9d-' \
              'iPyk2I4MxZnU; rosco_language=zh; googtrans=/auto/zh; SL_G_WPT_TO=zh-CN; SL_GWPT_Show_Hide_tmp=1; ' \
              'SL_wptGlobTipTmp=1; _gid=GA1.2.640679356.1649422568; OptanonConsent=isIABGlobal=false&datestamp=' \
              'Fri+Apr+08+2022+21%3A40%3A15+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)' \
              '&version=5.13.0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0003%3A1%2CC0002%3A1&' \
              'hosts=hiy%3A1%2Cilq%3A1%2Cjgg%3A1%2Cmke%3A1%2Cmyq%3A1%2Chwy%3A1%2Cibu%3A1%2Cnhe%3A1%2Cfdc%3A1&' \
              'AwaitingReconsent=false&geolocation=%3B'
    }

postform = 'field_brand_target_id=41&field_type_target_id=All& \
sort_by=field_roscolux_sort_order_value&sort_order=ASC&items_per_page=20&view_name=filters& \
view_display_id=block_2&view_args=41&view_path=%2Fzh%2Fviews%2Fajax&view_base_path=& \
view_dom_id=3fa53268ddd7500f0e410b09b91b6d51911ba083384c22cc40f2d874cecf2c09&pager_element=0&_drupal_ajax=1& \
ajax_page_state%5Btheme%5D=rosco&ajax_page_state%5Btheme_token%5D=& \
ajax_page_state%5Blibraries%5D=core%2Fhtml5shiv%2Crosco%2Fglobal-styling%2Csystem%2Fbase%2Cviews%2Fviews. \
ajax%2Cviews%2Fviews.ajax%2Cviews%2Fviews.ajax%2Cviews%2Fviews.ajax%2Cviews%2Fviews.ajax%2Cviews%2Fviews. \
ajax%2Cviews%2Fviews.ajax%2Cviews%2Fviews.ajax%2Cviews%2Fviews.ajax%2Cviews%2Fviews.ajax%2Cviews%2Fviews. \
ajax%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module%2Cviews%2Fviews.module%2Cviews%2Fviews.module%2Cviews%2Fviews. \
module%2Cviews%2Fviews.module%2Cviews%2Fviews.module%2Cviews%2Fviews.module%2Cviews%2Fviews. \
module%2Cviews%2Fviews.module%2Cviews%2Fviews.module%2Cviews%2Fviews.module%2Cviews%2Fviews.module'



failed_num = []
successed_num = []

def format_html(html, num):
    global failed_num

    soup = BeautifulSoup(html, 'html.parser')
    final_url = []
    for i in soup.findAll(name='div', attrs={'class': 'product-roscolux'}):
        parag = BeautifulSoup(str(i), 'html.parser')
        if not hasattr(parag.img, 'src'):
            failed_num.append(num)
            continue

        src = (parag.img)['src']
        number = src.split('/')[-1].split('.')[0]
        if number == num:
            final_url.append(src)


    return final_url

def get_url_name_and_number_ext(url):
    t,na = url.split('//')[-1].split('/')
    n, e = na.split('.')
    return t,n,e



def download_url(urls):
    preurl = 'https://cn.rosco.com'
    urls = list(map(lambda x: preurl + x, urls))
    print(f'--got {len(urls)} results')
    print(urls)
    print('--downloading...')

    for idx, u in enumerate(urls):
        filter_type, number, ext = get_url_name_and_number_ext(u)
        if ext.lower() != 'pdf':
            if number not in failed_num:
                failed_num.append(number)
            print('-- ', idx, f'not pdf! FAILED')
            continue

        outdir = os.path.join(out, f'./{number}', f'./{filter_type}_{number}_{ext}')
        if os.path.exists(outdir):
            strange_semaphore.acquire()
            g = input(f'??????? this is strange, the out file {filter_type}_{number}_{ext} already exists, '
                      f'pls check. Still save?(_/n)\n')
            strange_semaphore.release()
            if g == 'n':
                continue
        else:
            os.makedirs(outdir)

        savepath = f'{outdir}/{filter_type}_{number}.{ext}'
        urllib.request.urlretrieve(u, savepath)

        save_pdf_data(*get_pdf_data(savepath), outdir)
        print('-- ', idx, f'done in {savepath}')
        successed_num.append(number)


def get_url(num):
    global postform, failed_num

    print('='*6, f'deal with number {num}', '='*6)
    url = 'https://cn.rosco.com/zh/views/ajax?_wrapper_format=drupal_ajax'

    postform += f'&search={num}'
    res = requests.post(url, data=postform, headers=headers, verify=False)

    res = json.loads(res.text)
    htmldatas = res[2]['data']
    if 'No result found' in htmldatas:
        print(f'{num} no result')
        failed_num.append(num)
    else:
        img_urls = format_html(htmldatas, num)
        download_url(img_urls)


def start_abatch(idxs):
    for idx in idxs:
        get_url(idx)


def start(indexs, outdir):
    global ids, out
    ids = indexs.split('.')
    out = os.path.join('./', outdir)
    if not os.path.exists(out):
        os.makedirs(out)

    n = int(len(ids) / args.max_thread) + 1
    ids_block = [ids[i:i + n] for i in range(0, len(ids), n)]
    ts = []
    for idxs in ids_block:
        thread = threading.Thread(target=start_abatch, args=(idxs, ))
        thread.start()
        ts.append(thread)

    for t in ts:
        t.join()

    print(f'=== failed {len(failed_num)} numbers are', failed_num)
    print(f'=== successed {len(successed_num)} numbers are', successed_num)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('number', type=str)
    parser.add_argument('--output_dir', type=str, default='output')
    parser.add_argument('--max_thread', type=int, default=20)
    args = parser.parse_args()

    start(args.number, args.output_dir)


