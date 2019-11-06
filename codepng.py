import requests
from PIL import Image
import pytesseract

# 验证码地址
url = "http://cloud.epsolarpv.com/checkCode?0.7337270680854053"
response = requests.get(url).content
#将图片写入文件
with open('test.png','wb') as f:
    f.write(response)
#识别验证码
#第一步：通过内置模块PIL打开文件
#image = Image.open('E:\\test\\2019pytest\\微信截图_20191105151020.png')
image = Image.open('test.png')
image = image.resize((60, 30),Image.ANTIALIAS)  #对图片进行放大，容易识别
image = image.convert('L')  #转化为灰度图
threshold = 166             #设定的二值化阈值
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