import requests,re,time,os
import threading
from bs4 import BeautifulSoup


def main():
    reponse = requests.get("https://www.agefans.net/play/20130111?playid=4_1")
    print(reponse.text)

if __name__ == "__main__":
    main()