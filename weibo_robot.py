# -*- coding: utf-8 -*-
from weibo import APIClient
import urllib
import urllib2
import requests 
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#开发进度

#个人信息
__author__  = 'jas0ndyq'
__email__   = 'jasondyq@foxmail.com'
__version__ = 'v0'

#开启调试输出(0 or 1)
debug = 0

#构造headers信息
user_agent = (
  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
  'Chrome/20.0.1132.57 Safari/536.11'
)
session = requests.session()
session.headers['User-Agent'] = user_agent
session.headers['Host'] = 'api.weibo.com'

#设置全局变量
global api_key, api_secret, callback_url, userid, password
api_key = '**********' # 请在微博开放平台获取
api_secret = '**********' #请在微博开放平台获取
callback_url = 'http://jas0n.me'
userid = 'xxx@xx.com' #微博登陆邮箱
password = '**********' #微博登陆密码

#初始化API client
global client, referer_url
client =  APIClient(app_key=api_key, app_secret=api_secret, redirect_uri=callback_url)
referer_url = client.get_authorize_url()
if debug: print 'referer_url: %s' % referer_url

#获取回调地址的code
def get_code():
  #构造post数据
  data = {
    'client_id': api_key,
    'redirect_uri': callback_url,
    'userId': userid,
    'passwd': password,
    'isLoginSina': '0',
    'action': 'submit',
    'response_type': 'code'
  }

  session.headers['Referer'] = referer_url

  #post数据到服务器
  resp = session.post(
    url = 'https://api.weibo.com/oauth2/authorize',
    data = data
  )
  
  if debug: print 'get url: %s' % resp.url
  if debug: print 'code is: %s' % resp.url[-32:]
  
  #截取回调url中的code
  code = resp.url[-32:]
  return code

###以上内容为配置阶段，相关配置服务均可参照此进行

#发文字微博
def weibo_text(text):
  #post构造的数据获取code
  code = get_code()

  #获取授权令牌和期限
  token = client.request_access_token(code)
  client.set_access_token(token.access_token, token.expires_in)

  #发微博
  client.statuses.update.post(status=text)

#发图片微博
def weibo_pic(text, picture):
  #post构造的数据获取code
  code = get_code()

  #获取授权令牌和期限
  token = client.request_access_token(code)
  client.set_access_token(token.access_token, token.expires_in)

  #发图片微博
  Pic = open(picture, 'url')
  client.statuses.upload.post(status=text, pic=Pic)
  Pic.close()


#调用查询用户API
def check_user(userid):
  code = get_code()
  token = client.request_access_token(code)
  client.set_access_token(token.access_token, token.expires_in)
  #r = client.users.show.get(screen_name="爱薇薇")
  #print r
  global r #设置全局变量以备调用
  global her_screen_name
  r = client.users.show.get(uid=userid) #自行获取用户唯一uid
  her_screen_name = r['screen_name'] #通过uid获取用户昵称
  #print her_screen_name

#天气情况
#城市代码也可以从city.py调用
city_num = {
	"chengdu":"101270101",
	"chongqing":"101040100",
	"haerbing":"101050101"
}
	#哈尔滨：101050101
	#重庆：101040100
	#成都：101270101

def checkweather(num):
	site = ("http://weather.51wnl.com/weatherinfo/GetMoreWeather?cityCode=%s&weatherType=0") % num #引入天气信息API
	#print site
	web = urllib2.urlopen(site)

	content = web.read()
	data = json.loads(content)

	result = data["weatherinfo"]



	city = result["city"]
	#print city
	date_y = result["date_y"]
	weather = result["weather1"]
	temp = result["temp1"]
	suggest = result["index_d"]

	global final_temp
	final_temp = city + "，" + date_y + "。天气：" + weather + "，气温：" + temp + "。" + suggest

	#print final_temp + "\n"



#调用城市代码和微博名并发送微博
checkweather(city_num["haerbing"])

if __name__ == '__main__':
  #checkweather(city_num["chengdu"])
  check_user(1372451215) 
  weibo_text(final_temp + " @" + her_screen_name)
  # weibo_text("test")
  # weibo_pic('发布图片微博', '/home/jasondyq/test/test.png')


checkweather(city_num["chengdu"])

if __name__ == '__main__':
  #checkweather(city_num["chengdu"])
  check_user(2693448851)
  weibo_text(final_temp + " @" + her_screen_name)
  # weibo_text("test")
  # weibo_pic('发布图片微博', '/home/jasondyq/test/test.png')
