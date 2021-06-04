import pandas as pd
import requests,re,json,math,os,sys,random,time
from bs4 import BeautifulSoup


class Map(object):

    def poi_detect(self,host):
        '''
            获取该坐标是否存在poi点
        '''
        pass

    def download_map_img(self,host):
        '''
            下载地图瓦片图
        '''
        try:
            reponse = requests.get(host).content()

        except:
            print(host,"下载失败")
            




def deg2num(lon_deg, lat_deg, zoom):
    '''
    根据经纬度计算坐标轴
    lon_deg = 经度
    lat_deg = 纬度
    zoom = 地图层级

    返回元组(xtile, ytile)
    xtile = 经度对应坐标
    ytile = 纬度对应坐标
    '''
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def size(wide:int ,lon_deg:int ,lat_deg:int):

    print("size start~")
    """
    提供中心坐标，螺旋预生成坐标位置
    lon_deg =   中心经度
    lat_deg =   中心纬度
    wide    =   范围
    """
    res = []
    x = y = 0
    #img_coord = []
    #poi_location = []
    for i in range(wide):
        if i == 0:
            #print([str(lon_deg).ljust(6,"0"),str(lat_deg).ljust(6,"0"),i])
            res.append([str(lon_deg).ljust(10,"0"),str(lat_deg).ljust(9,"0"),i])
            lon_deg += 0.000001
            x += 1
            continue

        for z in range(i*2*4):
            time.sleep(0.0000000000001)
            lon_deg = round(lon_deg,6)
            lat_deg = round(lat_deg,6)
            res.append([str(lon_deg).ljust(10,"0"),str(lat_deg).ljust(9,"0"),i])
            #print([lon_deg,lat_deg,i])
            # 边角判断变向方向
            if abs(x) == abs(y):
                if x == y:
                    # 左下角与右上角
                    if x == i:
                        # 一圈结束，增加圈数
                        lon_deg += 0.000001
                        x += 1
                    elif x *-1 == i:
                        # 半圈结束，向上拐弯
                        lat_deg += 0.000001
                        y += 1
                
                elif x == y *-1:
                    # 左上角与右下角
                    if x == i:
                        lon_deg -= 0.000001
                        x -= 1
                    elif x *-1 == i:
                        lon_deg += 0.000001
                        x += 1
            

            else:
                if abs(y) == i:               
                # 横向判断

                    if y == i and x != i:
                        # 左路
                        lon_deg += 0.000001
                        x += 1
                    elif y *-1 == i:
                        lon_deg -= 0.000001
                        x -= 1
                else:
                ## 纵向判断
                    if x == i and y != i:
                        # 上路
                        lat_deg -= 0.000001
                        y -= 1
                    elif x * -1 == i:
                        lat_deg += 0.000001
                        y += 1
            


    return res


def main():
    '''
    centre = 中心点（经度,纬度）
    zoom = 地图层级
    radiation = 辐射范围
    agents = userAgent
    '''

    centre = (119.382915,35.177934)
    zoom = 19

    #radiation = int(0.005 * 100000)
    radiation = 10
    #获取图片坐标矩阵,及poi经纬度
    start = time.time() 
    text = size(radiation,centre[0],centre[1])
    print(len(text))
    end = time.time() 
    print(end-start,"s")







    #coordinate = deg2num(lon,lat,zoom)
    #print(coordinate)



if __name__ == "__main__":
    # 读取请求头池文件
    with open(r"useragents.txt") as  f:
        agents = f.read().split("\n")
    main()





    




    #lon=119.382915
    #lat=35.177934
    #zoom = 19
    #num = 10 ** 3
    #x_y = []
    #for x in range(num):
    #    lat = 35.16181639
    #    for y in range(num):
       
    #        print("lat=",lat,"lon=",lon)
    #        text = deg2num(lat,lon,zoom)
    #        if text not in x_y:
    #            x_y.append(text)
    #        lat += 0.000001

    #    lon += 0.000001
        
    #print(x_y)





    


