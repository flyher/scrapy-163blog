# -*- coding: utf-8 -*-
import scrapy
import os
import re
import json

class Blog163Spider(scrapy.Spider):
    name = 'blog163'
    allowed_domains = ['blog.163.com']
    start_urls = ['http://blog.163.com/blogger.html']
    def __int__(self):
        self.hao=0

    def parse(self, response):
        famouse_urls=response.xpath('//div[@class="g-bd ui-bg2"]//ol/li/a/@href').extract()[:5]
        famouse_name=response.xpath('//div[@class="g-bd ui-bg2"]//ol/li/a/text()').extract()[:5]


        pattern = re.compile(r'http://(.+)\.blog\.163.com')
        only_list=[]
        for i in famouse_urls:
            only = pattern.findall(i)
            #print only,type(only)
            only_list.append(only)
            yield scrapy.Request(url=i,callback=self.list_parse,meta={"meta0":only[0]})
            #print type(only)

        for j in range(0,len(only_list)):
            if only_list[j]:
                try:
                    dirname=famouse_name[j]+only_list[j][0]
                    os.makedirs('./blog/'+dirname)
                except:
                    continue
            else:
                dirname = famouse_name[j]
                os.makedirs('./blog/' + dirname)


    #列表页
    def list_parse(self,response):
        str=response.xpath("//a[@class='m2a fc03 fs1 ztag']/@href").extract()[0]
        pattern=re.compile(r'static/(\d{9})')
        hao=pattern.findall(str)[0].encode('utf-8')
        #提取url编号
        meta3=response.meta['meta0'].encode('utf-8')
        # print meta3,type(meta3)

        url = 'http://api.blog.163.com/'+meta3+'/dwr/call/plaincall/BlogBeanNew.getBlogs.dwr'
        header={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'Content-Type': 'text/plain',
            'Referer': 'http://api.blog.163.com/crossdomain.html?t=20100205',
        }

        yield scrapy.FormRequest(
                url=url,
                formdata={"scriptSessionId":"${scriptSessionId}187",
                        'callCount':'1',
                        'c0-scriptName':'BlogBeanNew',
                        'c0-methodName':'getBlogs',
                        'c0-id':'0',
                        'c0-param0':hao,
                        'c0-param1':'0',
                        'c0-param2':'30',
                        'batchId':'1'},
                headers=header,
                callback=self.content_parse,
                meta={"meta4": meta3}
                    )
    def content_parse(self,response):

        meta5=response.meta["meta4"]
        article_num = re.compile(r's\d+\.permaSerial="(.*?)"')
        res = article_num.findall(response.body)
        #print res
        for i in res:
            url='http://'+meta5+'.blog.163.com/blog/static/'+str(i)
            yield scrapy.Request(url=url,callback=self.final_parse,meta={"meta6":meta5})
    def final_parse(self,response):
        only=response.meta['meta6']
        name=response.xpath('//span[@class="tcnt"]/text()').extract()[0]
       # print name ,type(name)
        text=response.xpath('//div[@class="bct fc05 fc11 nbw-blog ztag"]//text()').extract()
        #print text,type(text)
        dir_list=os.listdir('./blog')
        pattern=re.compile(only)
        for i in dir_list:
            if pattern.search(i):
                with open('./blog/'+i.decode('gbk')+'/'+name+'.json','w')as f:
                    f.write(json.dumps(text,ensure_ascii=False).encode('utf-8'))
            else:
                pass









