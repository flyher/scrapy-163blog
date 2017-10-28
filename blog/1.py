import urllib2,urllib
import re
from lxml import etree
data={
'scriptSessionId':'${scriptSessionId}187',
'callCount':'1',
'c0-scriptName':'BlogBeanNew',
'c0-methodName':'getBlogs',
'c0-id':'0',
'c0-param0':'128975216',
'c0-param1':'0',
'c0-param2':'10',
'batchId':'1'
}
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    'Content-Type': 'text/plain',
     'Referer' : 'http://api.blog.163.com/crossdomain.html?t=20100205',

}
data=urllib.urlencode(data)
request=urllib2.Request(url='http://api.blog.163.com/dwmahonggang/dwr/call/plaincall/BlogBeanNew.getBlogs.dwr',data=data,headers=headers)

response=urllib2.urlopen(request)

html=response.read().decode('unicode-escape')
print html

# a=re.compile(r's\d+\.permaSerial="(.*?)"')
# b=a.findall(html)
# for i in b:
#     print i



