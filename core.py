from time import sleep
import json,base64
from random import randint
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from pillowdemo import findDiffStart

'''

'''

# 将base64转换为Image
def getImage(browser, classes):
    js = "return document.getElementsByClassName(\"%s\")[0].toDataURL(\"image/png\");" % classes
    # 执行 JS 代码并拿到图片 base64 数据
    im_info = browser.execute_script(js)  # 执行js文件得到带图片信息的图片数据
    im_base64 = im_info.split(',')[1]  # 拿到base64编码的图片信息
    im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    return Image.open(BytesIO(im_bytes))


def crackCaptcha(browser, fullbg, bg):
    # 得到不带缺口的背景
    img1 = getImage(browser, 'geetest_canvas_fullbg geetest_fade geetest_absolute')
    # 带缺口的背景图
    img2 = getImage(browser, 'geetest_canvas_bg geetest_absolute')
    # img1.save('fullbg.png')
    # img2.save('bg.png')
    # 得到差异位置，-8是因为滑块到背景左边缘默认有8px偏移
    left = findDiffStart(img1, img2)-8
    # 计算轨迹
    tracks = generateTracks(left)
    sleep(0.5)
    # 找到滑块
    slide = browser.find_element_by_xpath(
        '/html/body/div[4]/div[2]/div[6]/div/div[1]/div[2]/div[2]')
    # 模拟滑动
    action = ActionChains(browser)
    action.move_to_element(slide).click_and_hold()
    x = y = 0
    # 添加滑动Action
    for xoffset, yoffset in tracks:
        print("xoffset=%d,yoffset=%d,x=%d,y=%d" % (xoffset, yoffset, x, y))
        action.move_by_offset(xoffset, yoffset)
    #不需要sleep的原因是actionchain本身执行有间隔(可能是相同的)
    #就算间隔相同也不会造成滑块匀速运动(因为轨迹是随机的)
    action.release().perform()
    # 执行滑动


def generateTracks(left):
  x=0
  y=0
  tracks=[]
  while x<left:
    #添加if判断防止y跑的太偏
    if y>5:
      yoffset=-5
    elif y<-5:
      yoffset=5
    else:
      yoffset=randint(-3,3)
    #x在left的中间8/10的时候加速
    if x>(left/10) and x<(left*9/10):#如果要将6|12调大，建议将这里的9/10调小
      xoffset=randint(8,16)
    else:#在开始的时候和快到终点的时候减速，防止xoffset过大导致无法准确拼合
      xoffset=randint(3,6)
    x+=xoffset
    y+=yoffset
    tracks.append((xoffset,yoffset))
  return tracks
