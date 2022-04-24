import requests,re,time,os
import threading
from bs4 import BeautifulSoup

class M3u8Dowload(object):
    '''
        m3u8格式下载
    '''
    def __init__(self,m3u8url,name,dirName):
        self.m3u8url = m3u8url
        self.name = name
        self.dirName = dirName
        self.fileLine=None


    def readfile(self):
        print("开始下载，文件格式为m3u8")
        print(self.m3u8url)
        reponse = requests.get(self.m3u8url,headers =header).text
        ## 获取每行文件
        self.fileLine = reponse.split()
        print(self.fileLine)
        # 创建多线程进行并发
        self.fileLine = [i for i in self.fileLine if "http" in i]
        # 单片文件
        tsFile = {}
        count_num = 0
        for index,i in enumerate(self.fileLine):
            count_num += 1
            print(i)
            # 进行多线程请求
            ts = threading.Thread(target = self.dowload,args = (i,))
            tsFile[index]=[index,ts.start()]
            while count_num > 10:
                pass
            count_num -=1

        print(tsFile)
        sorted(tsFile,key = lambda x:x[0])
        tsFile = "".join([tsFile[i] for i in tsFile])
        print(len(tsFile) /1048576 ,"MB")
        with open(fr"dowload\{self.dirName}\{self.dirName}_{self.name}.mp4","wb") as f:
            f.write(tsFile)

        if tsFile >10240:
            print("下载成功")
            return True
        else:
            print("下载失败")
            os.remove(fr"dowload\{self.filename}\{self.filename}_{self.movname}.mp4")
            return False

    def dowload(self,url):
        '''
        获取单片请求，并返回结果
        '''
        return requests.get(url,headers = header).text

class Mp4Dowload(object):
    '''
    MP4格式下载
    '''
    def __init__(self,mov_url,movname,filename):
        '''
        mov_url：影片解析地址
        movname：影片名字
        filename：创建的文件夹路径

        '''
  
        self.mov_url = mov_url
        self.movname = movname
        self.filename =  filename


    def download(self):
        '''
        根据网页上抓取的title下载文件
        '''

        downsize = 0
        print('开始下载,该文件为mp4格式')
        startTime = time.time()
        reponse = requests.get(self.mov_url,headers =header)
        with open(fr"dowload\{self.filename}\{self.filename}_{self.movname}.mp4","wb") as f:
              for chunk in reponse.iter_content(chunk_size=10000):  
                  if chunk:
                      f.write(chunk)
                      downsize += len(chunk)
        line = 'downloading %d KB/s - %.2f MB， 共 %.2f MB'
        line = line % (
        downsize / 1024 / (time.time() - startTime), downsize / 1024 / 1024, downsize / 1024 / 1024)
        print(line)
        # 根据下载大小判断是否下载完成
        if downsize >10240:
            print("下载成功")
            return True
        else:
            print("下载失败")
            os.remove(fr"dowload\{self.filename}\{self.filename}_{self.movname}.mp4")
            return False

def max_page(soup_file):
    '''
    根据网站爬取最大页数并下载
    '''

    maxEpisode_txt = soup_file.select("div.movurls ul li a")
    # 如果上述方式没有找到标签，说明是首页的url，将res状态替换为false，后续就会以首页方式获取标题
    if not maxEpisode_txt:
        global res
        res = False
        maxEpisode_txt = soup_file.select("div.movurl ul li a")
    ## 获取最大页数

    # 获取每页相对地址及级数
    # pege_url为每页目标地址，page_name为每集名字
    pege_url = [i.get("href") for i in maxEpisode_txt]
    page_name = [i.text for i in maxEpisode_txt]


    return pege_url,page_name


#class Add(object):
#    def __init__(self):
#        pass
def mkdir(name):
    '''
    使用默认路径进行创建
    检测文件夹是否存在，若不存在则创建
    '''
    filename = fr"dowload\{name}"
    #if address:
    #    if os.path.isdir(f"{address}\{name}"):
    #        print("已经存在该文件夹")
    #    else:
    #        os.makedirs(f"{address}\{name}")
    #        print("创建文件夹成功,文件名为",name)
    #else:
    if os.path.isdir(filename):
        print("已经存在该文件夹")
    else:
        os.makedirs(filename)
        print("创建文件夹成功,文件名为",filename)



if __name__ == "__main__":
    #print("请输入保存地址，若不需要直接回车使用默认地址")

    #address = input("请输入地址")
    res = True
    #url = input("url:")
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    '''
    视频界面 http://www.yhdm.so/v/4789-5.html
    主页 http://www.yhdm.so/show/4789.html
    '''
    # url = "http://www.yhdm.so/v/3629-3.html"
    while True:
        url = input("url:")
        if url == "exit":
            break
        reponse = requests.get(url,headers =header)
        reponse.encoding = "utf-8"
        soup = BeautifulSoup(reponse.text,features="lxml")

        # 获取起始地址，并检测是那种类型的url
        pege_url,mov_name = max_page(soup)
        #print(pege_url,"\n",mov_name)
        pege_url = zip(pege_url,mov_name)

        # 获取影片名字，并创建同名文件夹
        if res: 
            filename = " ".join(soup.select_one("title").text.split("—")[0].split()[:-1])
        else:
            filename = soup.select_one("h1").text
        mkdir(filename)

    
        failed_list = []
        success_list = []
        download_list = []
        for movurl,movname in pege_url:
            #print(movurl,movname)
            start_url = "http://www.yhdm.so" + movurl
            print(filename,movname,start_url)
            reponse = requests.get(start_url,headers =header)
            reponse.encoding = "utf-8"
            soup = BeautifulSoup(reponse.text,features="lxml")
            #print(soup)

            # 提取文件url
            mov_url = soup.select_one("div.bofang div")["data-vid"]
            # 使用提取元素方法 ，而不是用正则，提取元素后再使用正则进行匹配，成功后进入下一步

            mov_url = mov_url[:-4]
            print("文件解析地址为：",mov_url)
        
            ## 根据下载地址及文件类型进行下载进行下载
            if "m3u8" not in mov_url:
                # 以mp4文件格式下载
                mp4Dowload = Mp4Dowload(mov_url,movname,filename)
                status = mp4Dowload.download()
            else:
                # 以m3u8文件格式下载
                m3u8Dowload = M3u8Dowload(mov_url,movname,filename)
                status = m3u8Dowload.readfile()

            download_list.append(movurl)
            if status:
                success_list.append(movurl)
            else:
                failed_list.append(movurl)
            print()
            time.sleep(1)
        print("\n\n\n\n全部下载完成")
    print("退出程序")