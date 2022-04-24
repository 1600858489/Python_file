import requests
from bs4 import  BeautifulSoup
import re,time

def main():
    url = "https://www.bqkan8.com/50_50096/"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44"}
    reponse = requests.get(url,headers = headers)
    reponse.encoding = "gbk"
    res = BeautifulSoup(reponse.text,features="html.parser")
    res = res.select_one("body > div.listmain > dl > dd:nth-child(15) > a")
    url_one = res.get("href")
    one = requests.get("https://www.bqkan8.com" + str(url_one),headers = headers)
    one.encoding = "gbk"
    res = BeautifulSoup(one.text,features="html.parser")
    title = res.select_one("#wrapper > div.book.reader > div.content > h1").text
    text = "".join([i.text for i in res.select("#content")]).replace("&1t;/p>","")
    text = "\n".join(text.split())
    return  title,text

if __name__ == "__main__":
    print(main())

