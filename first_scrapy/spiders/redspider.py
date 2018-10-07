# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
import requests
from lxml import html
import urllib
import urllib2

class RedspiderSpider(scrapy.Spider):
    name = 'redspider'

    login_url = 'https://support.octanefitness.com/login.cfm?send_back='
    start_urls = [login_url]
    
    def parse(self, response):

    	payload = {
			"email": "fitnesspartsrepair@gmail.com", 
			"password": "Xtreme80!" 			
		}
    	session_requests = requests.session()
    	login_url2 = "https://support.octanefitness.com/login.cfm?send_back="	
    	result = session_requests.get(login_url2)    
    	#tree = html.fromstring(result.text)			
    	print result.text

    	result = session_requests.post(login_url2, data = payload, headers = dict(referer=login_url2))    
    	print result.text
    	
    	url = 'https://support.octanefitness.com/model/model_detail.cfm?model_id=54'
    	result = session_requests.get(url, headers = dict(referer = url))
    	print result.text
    	#token = response.css('body[class="login"]').extract_first()
    	#print	token

    	data = {
    		'email' : 'fitnesspartsrepair@gmail.com',
    		'password' : 'Xtreme80!',
    	}

    	print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Logging to From>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'	
    	#resp = scrapy.FormRequest.from_response(response, method='POST', formdata = data , callback=self.after_login)
    	print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>End Logging to From>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'	
    	#print resp.url
    	#print resp
    	print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>End Logging to From>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    	

    def after_login(self, response):
    	#open_in_browser(response)
    	#content = response.text
    	print response.url
    	print response.text
    	print	'login Successed!!!++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    	base_url = 'https://support.octanefitness.com/model/model_detail.cfm?'
    	#print	content
    	#pagelist = ['model_id=54', 'model_id=56', 'model_id=499', 'model_id=58', 'model_id=337', 'model_id=68', 'model_id=69', 'model_id=73', 'model_id=75',    	'model_id=90', 'model_id=79', 'model_id=350', 'model_id=99', 'model_id=98', 'model_id=101', 'model_id=325', 'model_id=96', 'model_id=327', 'model_id=356', 'model_id=357', 'model_id=330', 'model_id=102', 'model_id=380', 'model_id=334', 'model_id=340']
    	pagelist = ['model_id=54']
    	for page in pagelist:
            return scrapy.Request(url= base_url + page, callback=self.process_oneurl)
        #return scrapy.Request(url= 'https://support.octanefitness.com/model/model_detail.cfm?model_id=58%23base-diagram:4199:982', callback=self.process_oneurl,dont_filter = True)

        #session=requests.Session()

        #r = requests.get(url= 'https://support.octanefitness.com/model/model_detail.cfm?model_id=58%23base-diagram:4199:982')
        #print r.url
		#print r.text
		
    def process_oneurl(self, response):
    	print 'process_oneurl page find successfully!'
    	#open_in_browser(response)
    	print(response.url+ "--------------------------------------------------------process_oneurl----------------------------------------------------------------")

    	#tree = html.fromstring(response.content)
    	#print tree
        # Get all the <a> tags

        #titlenames = response.css('div.title::text').extract_first()
        #print titlenames
        a_selectors = response.xpath('//div[@class="title"]')

        print(len(a_selectors))
        #print(a_selectors)
        # Loop on each tag
        aa = 0
        for selector in a_selectors:
            # Extract the link text
            #partname = selector.xpath('text()').extract()

            #middle_partnam = selector.xpath('following-sibling::div[1]/text()').extract()
            #partnumber = ''.join(middle_partnam).replace('Part Number: ', '').strip().split("\n")

            #middleprice = selector.xpath('../following-sibling::td[1]/text()').extract()
            #price = ''.join(middleprice).strip().split("\n")

            #quantity = selector.xpath('../following-sibling::td[2]//text()').extract()

            #print quantity
            #print partnumber

            #if it have a view button or not
            #getting data-diagram-id
            part_id = selector.xpath('../following-sibling::td[4]//input[@name="part_id"]/@value').extract_first()
            model_id = selector.xpath('../following-sibling::td[4]//input[@name="model_id"]/@value').extract_first()
            print ('PartID:->'+part_id + ', ModelID:->'+model_id+'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            data = {
    			'part_id' : part_id,
    			'model_id' : model_id,
    		}

            return scrapy.FormRequest.from_response(response, method='POST' , formdata={'qty': '','model_id': '54','part_id': '1565'} , callback=self.process_detail)
            #print resp.url
            data_diagram_crumbs = selector.xpath('../following-sibling::td[4]//a/@data-diagram-crumbs').extract()

            #detailview = '#base-diagram:' + data_diagram_crumbs +':'+data_diagram_id
            if(len(data_diagram_crumbs)>0):
            	data_diagram_id = selector.xpath('../following-sibling::td[4]//a/@data-diagram-id').extract()
            	detailview = '#base-diagram:' + data_diagram_crumbs[0] +':'+data_diagram_id[0]

            	detail_url = response.url + detailview#'https://support.octanefitness.com/model/model_detail.cfm?model_id=353'
            	print detail_url + ':detail_url>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'



            	#req = urllib2.Request(url='https://support.octanefitness.com/model/model_detail.cfm?model_id=73#base-diagram:1837:1014')
            	#f = urllib2.urlopen(req)
            	#print f.url +"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            	#return response.follow(url = detail_url, callback=self.process_detail)
            	#return scrapy.Request(url= 'https://support.octanefitness.com/model/model_detail.cfm?model_id=73#base-diagram:1837:1014', method='POST', callback=self.process_detail, dont_filter = True)
            	#print resp.url + '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
            	#print resp.content
            	#self.process_detail(resp)
            	if aa==1:
            		break
            	#resp = requests.post(detail_url)
            	#print resp.content
            	aa = 1
            	#print resp.content
            	#self.process_detail(resp)

    def process_detail(self, response):
    	#open_in_browser(response)

    	print 'process_detail page find successfully!*****************************************************************************'
    	#print response.text
    	#return scrapy.Request(url= 'https://support.octanefitness.com/model/model_detail.cfm?model_id=73#base-diagram:1837:3367', callback=self.abc)
    	
    	#print(response.url)

    	#main_title = response.xpath('//h4[@class="box dark"]/text()').extract_first()
    	#a_selectors = response.xpath('//div[@class="title"]')

    	#print(len(a_selectors))

    	#for selector in a_selectors:
    		#partname = selector.xpath('text()').extract()

            #middle_partnam = selector.xpath('following-sibling::div[1]/text()').extract()
            #partnumber = ''.join(middle_partnam).replace('Part Number: ', '').strip().split("\n")

            #middleprice = selector.xpath('../following-sibling::td[1]/text()').extract()
            #price = ''.join(middleprice).strip().split("\n")

            #quantity = selector.xpath('../following-sibling::td[2]//text()').extract()

        #    listno = selector.xpath('preceding-sibling::span[1]/text()').extract()
        #    print listno

    def abc(self, response):
    	print response.url + '.............................'

            


    	
    	
        
