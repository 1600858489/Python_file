import requests
from bs4 import  BeautifulSoup
import re,time

def main():
    url = "https://www.bqkan8.com/50_50096/18520412.html"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44"}
    reponse = requests.get(url,headers = headers)
    res = BeautifulSoup(reponse.text,features="html.parser")
    aTage = res.select("a")
    lis1 = [i.get("href") for i in aTage]
    print(lis1)

if __name__ == "__main__":
    main()
