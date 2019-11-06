import time
import requests
from pytesseract import pytesseract
from selenium import webdriver
from PIL import Image


#创建一个浏览器对象
browser = webdriver.Chrome()
browser.maximize_window()
#打开登录界面
browser.get('http://cloud.epsolarpv.com/login')

# 识别验证码
browser.save_screenshot('login.png')
#获取验证码位置
codepng = browser.find_element_by_xpath('//*[@id="imgCheckCode"]')
location = codepng.location
size = codepng.size
#获取验证码位置
left = location['x']
top = location['y']
bottom = top + size['height']
right = left + size['width']

#打开页面截图
login_png = Image.open('login.png')
code_png = login_png.crop((left,top,right,bottom))   #这里需要传入一个元组
code_png.save('code.png')
#识别验证码
#第一步：通过内置模块PIL打开文件
image = Image.open('code.png')
#第二步：识别图片中的内容
image = image.convert('L')  #转化为灰度图
threshold = 168             #设定的二值化阈值
table = []                  #table是设定的一个表，下面的for循环可以理解为一个规则，小于阈值的，就设定为0，大于阈值的，就设定为1
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table,'1')  #对灰度图进行二值化处理，按照table的规则（也就是上面的for循环）
image.show()
result = pytesseract.image_to_string(image) #对去噪后的图片进行识别
print('图片内容为:',result)

#定位账号密码验证码输入框
acc_input = browser.find_element_by_xpath('//*[@id="username"]')
time.sleep(2)
acc_input.send_keys('EPEVER001')
pwd_input = browser.find_element_by_xpath('//*[@id="password"]')
time.sleep(2)
pwd_input.send_keys('123456')
code_input = browser.find_element_by_xpath('//*[@id="checkCode"]')
time.sleep(2)
code_input.send_keys(result)
time.sleep(5)

#点击登录按钮
try:
    browser.find_element_by_xpath('//*[@id="login"]/div[5]/button').click()
    #判断系统状态
    url = browser.current_url
    resp = requests.get(url, timeout=5)
    code = resp.status_code
    print('登录返回码为：',code)
    assert code == 200
except Exception as e:
    time.sleep(5)
    #关闭
    browser.close()
    print('发生错误，登录失败！')
else:
    if url == 'http://cloud.epsolarpv.com/lamp/analysis/data':
        print('登录成功!')
    else:
        print('登录失败!')
    time.sleep(3)
    # 关闭
    browser.close()
