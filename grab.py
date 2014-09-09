# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 18:38:07 2014

@author: Prosnav
"""

import urllib3
import csv
from bs4 import BeautifulSoup

table = []
LINK_PREFIX = 'http://snap.windin.com/ns'
http = urllib3.PoolManager()

with open("list.csv", newline='', encoding='utf8') as csvfile:
    #dialect=csv.Sniffer.sniff(csvfile.read(10240))
    #csvfile.seek(0)
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        table.append(row)

#table[0][-1]='文件名'
#table[0].append('PDF链接')

def getDownloadInfo(row):
    r = http.request("GET", row[3])
    soup = BeautifulSoup(r.data)

    time_stamp = '{2}{1}{0}'.format(*row[0].split(sep='/'))
    sec_code = row[1]
    try:
        file_name = '--'.join([time_stamp, sec_code, soup.find(target="downloadAttach").get('title')])
        href = soup.find(target="downloadAttach").get('href')
        pdf_link = LINK_PREFIX + href[1:]
    except AttributeError as err:
        print(err)
        print("No Attachments!")
        from time import localtime,strftime
        err_time=strftime('%H:%M:%S %d-%m-%Y',localtime())
        with open('errlog.log','a') as ferr:
            ferr.write(','.join([err_time,sec_code,time_stamp,row[2],row[3]])+'\n')
        pass

    return (pdf_link,file_name)

# for index, row in enumerate(table[1:]):
for index, row in enumerate(table[1957:]):
    try:
        pdf_link=getDownloadInfo(row)[0]
        file_name=getDownloadInfo(row)[1]
        # table[i+1][-1]=file_name
        # table[i+1].append(pdf_link)

        with http.request("GET", pdf_link) as response, open('/'.join(['dl_prospectus', file_name]), 'wb') as pdf:
            pdf.write(response.data)

        print(' '.join([str(index) + '.', file_name, 'is downloaded!']))
    except Exception:
        pass
