# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver

from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
import requests
from lxml import html
import urllib
import urllib2

import time
from time import sleep
import random
import csv



class GreenspiderSpider(scrapy.Spider):
    name = 'greenspider'
    #allowed_domains = ['www.green.com']
    #start_urls = ['http://www.green.com/']
    login_url = 'https://support.octanefitness.com/login.cfm?send_back='
    start_urls = [login_url]

    base_url = 'https://support.octanefitness.com/model/model_detail.cfm?'

    fieldnames=['PartID' , 'PartName', 'Price', 'PartListKey', 'Quantity', 'ModelName']
    csvfile = open('result.csv', 'w')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    crome_path = r"C:\cromedriver\chromedriver.exe"
    driver = webdriver.Chrome(crome_path)
    driver.maximize_window()
    driver.get('https://support.octanefitness.com/login.cfm?send_back=')


    def parse(self, response):
    	username = self.driver.find_element_by_name("email")
    	userpwd = self.driver.find_element_by_name("password")

    	username.send_keys('fitnesspartsrepair@gmail.com')
    	userpwd.send_keys('Xtreme80!')

    	submit = self.driver.find_element_by_xpath('//button[@type="submit"]')
    	submit.click()
    		

    	print	'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>You have logined successfully!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

    	pagelist = [
    	 # 'model_id=379',
    	 # 'model_id=344', 
    	 # 'model_id=54', 
    	 # 'model_id=56', 
    	 # 'model_id=499', 
    	 # 'model_id=58', 
    	 # 'model_id=337', 
    	 # 'model_id=68', 
    	 # 'model_id=69', 
    	 # 'model_id=73', 
    	 # 'model_id=75',
    	 # 'model_id=90', 
    	 # 'model_id=79', 
    	 # 'model_id=83', 
    	 # 'model_id=350', 
    	 # 'model_id=99', 
    	 # 'model_id=98', 
    	 # 'model_id=101', 
    	 # 'model_id=325', 
    	 # 'model_id=96', 
    	 # 'model_id=327',
    	 # 'model_id=356', 
    	 # 'model_id=357', 
    	 # 'model_id=330', 
    	 # 'model_id=102', 
    	 # 'model_id=380', 
    	 # 'model_id=334', 
    	 # 'model_id=340', 
    	 # 'model_id=57', 
    	 # 'model_id=59', 
    	 # 'model_id=60',
    	 # 'model_id=65',	 
    	 # 'model_id=61', 
    	 # 'model_id=62', 
    	 # 'model_id=63', 
    	 # 'model_id=64', 
    	 # 'model_id=66', 
    	 # 'model_id=67', 
    	 # 'model_id=70', 
    	 # 'model_id=71', 
    	 # 'model_id=72',
    	 # 'model_id=85', 
    	 # 'model_id=86', 
    	 # 'model_id=87', 
    	 # 'model_id=91', 
    	 # 'model_id=89', 
    	 # 'model_id=88', 
    	 'model_id=77', 
    	 'model_id=78', 
    	 'model_id=80', 
    	 'model_id=81', 
    	 'model_id=84', 
    	 'model_id=82', 
    	 'model_id=94', 
    	 'model_id=95', 
    	 'model_id=97', 
    	 'model_id=92', 
    	 'model_id=93'
    	 ]

    	for page in pagelist:
    		self.process_model(self.driver.get(self.base_url + page) , self.base_url + page)
            #return scrapy.Request(url= self.base_url + page, callback=self.process_model)
            #self.driver.get(self.base_url + page)
            #posts = self.driver.find_elements_by_class_name("title")

    	    #for post in posts:
    	    #	print post.text

    	self.driver.quit()
    	self.csvfile.close()


    
    def process_model(self, response, currentUrl):
    	
    	nIndex = 0
    	print	currentUrl
    	print	'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Scanning Main Page!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

    	main_box_title = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/h2').text
    	print main_box_title
    	MainTable = self.driver.find_element_by_xpath('//*[@class="table table-striped resources"]/tbody')

    	for i in MainTable.find_elements_by_xpath('.//tr'):

    		try:
	    		middle_part_no = i.find_element_by_class_name('number').text
	    		#part_No = '#' + middle_part_no + '-' + box_title
	    		part_No = ""

	    		part_number =  i.find_element_by_class_name('part-number').text
	    		part_Number = part_number.replace('PART NUMBER: ', '')

	    		part_Name = i.find_element_by_class_name('title').text
	    		part_Price = i.find_element_by_class_name('price').text
	    		part_Quantiy = i.find_element_by_xpath('.//td[4]').text

	    		print 'Part_Number:-> ' + part_Number + ', Part_Name:-> ' + part_Name + ', Part_Price:-> ' + part_Price + ', Part_Quantiy:-> ' + part_Quantiy
	    		nIndex = nIndex + 1

	    		json_one = {"PartID":part_Number, "PartName":part_Name, "Price":part_Price, "PartListKey":part_No, "Quantity":part_Quantiy, "ModelName":main_box_title}
	    		self.writer.writerow(json_one)

	    		image_dir = "D://proudctimage/"

	    		# download the image
	    		try:
	    			urllib.urlretrieve('https://support.octanefitness.com/files/image/large/'+part_Number+'.jpg', image_dir + part_Number + ".jpg")
	    			#print 'okay'
	    		except Exception as e:
	    			print '+++++++++++++++++++++++++++++++++++++++++++++<Saving1 exception product image>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

    		except Exception as e:
    			print '++++++++++++++++ <Main Page UnExcepted Exception>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'


    	print	'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Scanning Detailed Page!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

    	viewurlArray = []
    	vblist = self.driver.find_elements_by_xpath('//*[@id="addPart"]/div/a')
    	
    	for vb in vblist:
    		dialog_crumbs = vb.get_attribute('data-diagram-crumbs')
    		diagram_id = vb.get_attribute('data-diagram-id')
    		add_param = '#base-diagram:' + dialog_crumbs + ':' + diagram_id
    		execute_url =  currentUrl + add_param
    		#print execute_url + '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

    	 	viewurlArray.append(execute_url)

    	#Scan View Buttons
    	
    	for vurl in viewurlArray:
    		self.driver.get(vurl)
    		self.driver.refresh()
    		time.sleep(3)
    		
    		try:	
	    		box_title = self.driver.find_element_by_xpath('//*[@id="base"]/div[1]/div[3]/h4').text
	    		DetailTB = self.driver.find_element_by_xpath('//*[@class="table table-striped resources"]/tbody')
	    	except Exception as e:
	    		continue

    		for i in DetailTB.find_elements_by_xpath('.//tr'):
    			try:	
	    			middle_part_no = i.find_element_by_class_name('number').text
	    			part_No = '#' + middle_part_no + '-' + box_title

	    			part_number =  i.find_element_by_class_name('part-number').text
	    			part_Number = part_number.replace('PART NUMBER: ', '')

	    			part_Name = i.find_element_by_class_name('title').text
	    			part_Price = i.find_element_by_class_name('price').text
	    			part_Quantiy = i.find_element_by_xpath('.//td[4]').text

	    			print 'Part_Number:-> ' + part_Number + ', Part_Name:-> ' + part_Name + ', Part_Price:-> ' + part_Price + ', Part_Quantiy:-> ' + part_Quantiy + ', Part_No:-> ' + part_No
	    			nIndex = nIndex + 1

	    			json_one = {"PartID":part_Number, "PartName":part_Name, "Price":part_Price, "PartListKey":part_No, "Quantity":part_Quantiy, "ModelName":main_box_title}
	    			self.writer.writerow(json_one)

	    			# saving image on hard disk.
	    			imageproduct_dir = "D://proudctimage/"
	    			try:
	    				urllib.urlretrieve('https://support.octanefitness.com/files/image/large/'+part_Number+'.jpg', imageproduct_dir + part_Number + ".jpg")
	    				#print 'okay2'
	    			except Exception as e:
	    				print '+++++++++++++++++++++++++++++++++++++++++++++<Saving2 exception product image>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

    			except Exception as e:
    				print '+++++++++++++++++++++++++++++++++++++++++++++<UniCode Exception!!!!!!!!>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'


    		#save images
    		image_dir = "D://productdiagram/"

    		#print '1@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    		try:
    		#	print '2@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    			Frame_Index = 1
    			part_images = self.driver.find_element_by_xpath('//*[@id="base"]/div[1]/div[3]/ul')

    			for part_image in part_images.find_elements_by_xpath('.//li'):
	    			#print "start"
	    			image_url = part_image.find_element_by_xpath('.//a').get_attribute('href')
	    			#print image_url
	    			image_jpgname = box_title + '_Frame' + str(Frame_Index);
	    			#print image_jpgname
   	
	    			# download the image
	    			try:
	    				urllib.urlretrieve(image_url, image_dir + image_jpgname + ".jpg")
	    				#time.sleep(2)
	    				#print 'Scan View Buttons - Exception--------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
	    			except Exception as e:
	    				print 'Scan View Buttons - Exception--------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

	    			Frame_Index = Frame_Index + 1

    		except Exception as e:
    		
    		# download the image
	    		try:
	    			single_image_url = self.driver.find_element_by_xpath('//*[@id="base"]/div[1]/div[3]/div/img').get_attribute('src')
    				single_image_jpgname = box_title + '_Frame1';

	    			urllib.urlretrieve(single_image_url, image_dir + single_image_jpgname + ".jpg")
	    			#time.sleep(2)
	    			#print 'Scan View Buttons - Exception--------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
	    		except Exception as e:
	    			print 'Diagram Saving Exception <<<>>>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    		else:
    			pass
    		finally:
    			pass


    	print nIndex

    	
    	#Capture view urls

    	#a_selectors = self.driver.find_elements_by_xpath('//div[@class="title"]')
    	#print	'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>**********************************>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    	#for partname in partnames:
    	#	print partname.text
    	#print	'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>---------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

    	#view = self.driver.find_element_by_xpath('//a[@data-diagram-id="1847"]')
    	#print view.text
    	
    	#button = driver.wait.until(EC.element_to_be_clickable((By.NAME, "btnK")))
    	#vblist = self.driver.find_elements_by_xpath('//*[@id="addPart"]/div/a')
    	# print len(vblist)
    	# print '-------------------------------------------------------------------'

    	# for vb in vblist:
    	#for i in [0,1,2]:
    	# 	print len(vblist)
    	# 	print '-------------------------------------------------------------------'
    	# 	dialog_crumbs = vb.get_attribute('data-diagram-crumbs')
    	# 	diagram_id = vb.get_attribute('data-diagram-id')
    	# 	add_param = '#base-diagram:' + dialog_crumbs + ':' + diagram_id
    	# 	execute_url =  currentUrl + add_param
    	# 	print execute_url + '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
    	# 	self.driver.get(execute_url)
    	# 	self.driver.refresh()
    	# 	time.sleep(1)

    		#print "STEP0------------------------------------------------------------------------------------------------------------------>"
    		#print dialog_number
    		# print len(vblist)
    		# print vb.text
    		#print "STEP1------------------------------------------------------------------------------------------------------------------>"
    		# prev_vb = vb
    		#vb.click()
    		#print i
    		#if i == 0:
    		#	self.driver.get('https://support.octanefitness.com/model/model_detail.cfm?model_id=54#base-diagram:3367:1847')
    		#elif i == 1:
    		#	self.driver.get('https://support.octanefitness.com/model/model_detail.cfm?model_id=54#base-diagram:3367:1502')
    		#else:
    		#	break
    		#print "STEP2------------------------------------------------------------------------------------------------------------------>"
    		#time.sleep(1)
    		#self.driver.refresh()
    		#time.sleep(2)

    		#print "STEP3------------------------------------------------------------------------------------------------------------------>"

    		#DetailTB = self.driver.find_element_by_xpath('//*[@class="table table-striped resources"]/tbody')
    		#print "STEP2------------------------------------------------------------------------------------------------------------------>"
    		#box_title = self.driver.find_element_by_xpath('//*[@id="base"]/div[1]/div[3]/h4').text
    		#//*[@id="base"]/div[1]/div[3]/h4
    		#print "STEP3------------------------------------------------------------------------------------------------------------------>" + box_title

    		#for i in DetailTB.find_elements_by_xpath('.//tr'):
    		#	part_number =  i.find_element_by_class_name('part-number').text
    		#	part_number = part_number.replace('PART NUMBER: ', '')
    		#	part_No =  i.find_element_by_class_name('number').text

    		#	print '#' + part_No + ' - ' + box_title + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

    			

    		
    		#resp = self.driver.get('https://support.octanefitness.com/model/model_detail.cfm?model_id=54')
    		#self.driver.back()
    		#self.driver.refresh()
    		# self.driver.get('https://support.octanefitness.com/model/model_detail.cfm?model_id=54')
    		#time.sleep(3)
    		# vb = prev_vb
    		#print "FINSIH ONE------------------------------------------------------------------------------------------------------------------>"
    		
    		#self.driver.back()
    		#self.driver.refresh()
    		#self.driver.get('https://support.octanefitness.com/model/model_detail.cfm?model_id=54')
    		#break

    	#return 0	
    	#print	'*****************************************************   vb2   *************************************************'
    	#vb2.click()
    	#self.driver.find_element_by_partial_link_text("View").click()

    	#return 0

    	#driver.findElement(By.xpath("//a/u[contains(text(),'Re-Submit')]")).click();

    	#SMRtable = self.driver.find_element_by_xpath('//*[@class="table table-striped resources"]/tbody')
    	#index = 0
    	#for i in SMRtable.find_elements_by_xpath('.//tr'):
    		#print i.get_attribute('innerHTML')
    		#for j in i.find_elements_by_xpath('.//td'):
    		#print i.find_element_by_class_name('title').text
    		# part_number =  i.find_element_by_class_name('part-number').text
    		# part_number = part_number.replace('PART NUMBER: ', '')
    		# #print	part_number
    		# #print i.find_element_by_class_name('price').text
    		# #print i.find_element_by_xpath('.//td[3]').text
    		# #print i.find_element_by_xpath('.//td[4]').text

    		# #btn btn-default btn-sm dropdown tooltip-view
    		
    		# try:
    		# 	#viewbutton = i.find_element_by_xpath('//*[@id="addPart"]/div/a')
    		# 	#viewbutton.click()
    		# 	#print data_diagram + '******************************************************************************************************'
    		# 	#print viewbutton.text
    		# 	#viewbutton.click()
    		# 	#index = index + 1
    		# 	print	'*****************************************************   okay   *************************************************'

    		# except Exception as e:
    		# 	print	'++++++++++++++++++++++++++++++++++++++++++++++++++Exception++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    		 


    	#for selector in a_selectors:

    	#	part_name = selector.text
    		#print part_name

    	#	middle_partnam = selector.find_element_by_xpath('./following-sibling::div[1]')
        	#partnumber = ''.join(middle_partnam).replace('Part Number: ', '').strip().split("\n")
        #	print	middle_partnam.text

        #	middleprice = selector.xpath('../following-sibling::td[1]/text()').extract()
    	#	price = ''.join(middleprice).strip().split("\n")

    	#	quantity = selector.xpath('../following-sibling::td[2]//text()').extract()

    	#	print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    	#	print 'Part Number:' + partnumber + ', Part Name:' + partname + ', Price:' + price + ', Quantity:' + quantity

