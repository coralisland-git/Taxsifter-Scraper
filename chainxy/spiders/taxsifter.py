# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from lxml import etree

from lxml import html

import string

import time

import pdb


class taxsifter(scrapy.Spider):

	name = 'taxsifter'

	domain = 'http://graysharborwa.taxsifter.com'

	history = []

	output = []

	header = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
		"Accept-Encoding": "gzip, deflate",
		"Proxy-Authorization": "Basic Y2Fyb25kMDA2QGdtYWlsLmNvbTpJbW9iaWxlMQ==",
		"Cookie": "ASP.NET_SessionId=knzxh245zxu1na55sd25nibi; FormsAuthentication=33874677C1D796561BB666938840F546D3D711E428DE5782FA5D08ADB94CB2F010B3F244BA81BCEFB0114E897D0526D6994FDE2924F955FF08761D05848AFF1901B406564C3BA2F2EF011352FB3F5D001A42156EDC36F54DF86FEADC095DC97D23163847A06D3EFEABEC644C607E038CD583F3A2F150CB563DAFEF90C21FC120A250579BFDA22F00199ACE54889043882C5E1E45",
		"Proxy-Connection": "keep-alive",
		"Referer": "None",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
	}

	def __init__(self):

		pass
	
	def start_requests(self):

		url = "http://graysharborwa.taxsifter.com/Disclaimer.aspx"

		formdata = {
			"__VIEWSTATE": "/wEPDwUINTA1ODUyOTQPZBYCZg9kFgICAw9kFgQCAQ9kFgQCAQ8WAh4LXyFJdGVtQ291bnQCBRYKZg9kFgICAQ8PFgYeB1Rvb2xUaXAFJlBlcmZvcm0gYSBzZWFyY2ggdXNpbmcgc2ltcGxlIGNyaXRlcmlhHgtOYXZpZ2F0ZVVybAUVfi9TZWFyY2gvUmVzdWx0cy5hc3B4HgZUYXJnZXQFBV9zZWxmZBYCZg8VAQ1TaW1wbGUgU2VhcmNoZAIBD2QWAgIBDw8WBh8BBShQZXJmb3JtIGEgc2VhcmNoIGJhc2VkIG9uIHByb3BlcnR5IHNhbGVzHwIFHn4vU2FsZXNTZWFyY2gvU2FsZXNTZWFyY2guYXNweB8DBQVfc2VsZmQWAmYPFQEMU2FsZXMgU2VhcmNoZAICD2QWAgIBDw8WBh8BBSZPcGVuIHRoZSBDb3VudHkgSG9tZSBQYWdlIChOZXcgd2luZG93KR8CBSFodHRwOi8vd3d3LmNvLmdyYXlzLWhhcmJvci53YS51cy8fAwUGX2JsYW5rZBYCZg8VARBDb3VudHkgSG9tZSBQYWdlZAIDD2QWAgIBDw8WBh8BBRhWaWV3IGNvbnRhY3QgaW5mb3JtYXRpb24fAgUOfi9Db250YWN0LmFzcHgfAwUFX3NlbGZkFgJmDxUBB0NvbnRhY3RkAgQPZBYCAgEPDxYGHwEFGVZpZXcgdGhlIGxlZ2FsIGRpc2NsYWltZXIfAgURfi9EaXNjbGFpbWVyLmFzcHgfAwUFX3NlbGZkFgJmDxUBCkRpc2NsYWltZXJkAgMPFgIeBWNsYXNzBQduYXZMaW5rZAICD2QWBAIBDw8WAh4EVGV4dAX0Eg0KPGhlYWQ+DQo8c3R5bGU+DQo8IS0tDQpkaXYuU2VjdGlvbjENCgl7cGFnZTpTZWN0aW9uMTt9DQotLT4NCjwvc3R5bGU+DQo8L2hlYWQ+DQo8ZGl2IHN0eWxlPSJtYXJnaW4tbGVmdDoxNXB4O2ZvbnQtd2VpZ2h0Om5vcm1hbDsiPg0KVGhlIGluZm9ybWF0aW9uIHByb3ZpZGVkIGJ5ICBHcmF5cyBIYXJib3IgQ291bnR5IGlzIHByb3ZpZGVkICdhcyBpcycgYW5kIGZvciByZWZlcmVuY2Ugb25seS4gVGhlIHVzZXIgZXhwcmVzc2x5IGFncmVlcyB0aGF0IHRoZSB1c2Ugb2YgIEdyYXlzIEhhcmJvciBDb3VudHkncyB3ZWIgc2l0ZSBpcyBhdCB0aGUgdXNlcidzIHNvbGUgcmlzay4gIEdyYXlzIEhhcmJvciBDb3VudHkgZG9lcyBub3Qgd2FycmFudCB0aGF0IHRoZSBzZXJ2aWNlIHdpbGwgYmUgdW5pbnRlcnJ1cHRlZCBvciBlcnJvciBmcmVlLiBBbnkgaW5mb3JtYXRpb24gcHVibGlzaGVkIG9uIHRoaXMgc2VydmVyIGNvdWxkIGNvbnRhaW4gdGVjaG5pY2FsIGluYWNjdXJhY2llcyBvciB0eXBvZ3JhcGhpY2FsIGVycm9ycy4gQ2hhbmdlcyBtYXkgYmUgbWFkZSBwZXJpb2RpY2FsbHkgdG8gdGhlIHRheCBsYXdzLCBhZG1pbmlzdHJhdGl2ZSBydWxlcywgdGF4IHJlbGVhc2VzIGFuZCBzaW1pbGFyIG1hdGVyaWFsczsgdGhlc2UgY2hhbmdlcyBtYXkgb3IgbWF5IG5vdCBiZSBpbmNvcnBvcmF0ZWQgaW4gYW55IG5ldyBtYXRlcmlhbHMgb24gdGhlIHdlYiBzaXRlLg0KPC9kaXY+PGJyPg0KDQo8ZGl2IHN0eWxlPSJtYXJnaW4tbGVmdDoxNXB4O2ZvbnQtd2VpZ2h0Om5vcm1hbDsiPg0KIEdyYXlzIEhhcmJvciBDb3VudHkgbWFrZXMgZXZlcnkgZWZmb3J0IHRvIHByb2R1Y2UgYW5kIHB1Ymxpc2ggdGhlIG1vc3QgY3VycmVudCBhbmQgYWNjdXJhdGUgaW5mb3JtYXRpb24gcG9zc2libGUuIE5vIHdhcnJhbnRpZXMsIGV4cHJlc3Mgb3IgaW1wbGllZCwgYXJlIHByb3ZpZGVkIGZvciB0aGUgZGF0YSBwcm92aWRlZCwgaXRzIHVzZSwgb3IgaXRzIGludGVycHJldGF0aW9uLiAgR3JheXMgSGFyYm9yIENvdW50eSBkb2VzIG5vdCBndWFyYW50ZWUgdGhlIGFjY3VyYWN5IG9mIHRoZSBtYXRlcmlhbCBjb250YWluZWQgaGVyZWluIGFuZCBpcyBub3QgcmVzcG9uc2libGUgZm9yIGFueSBtaXN1c2Ugb3IgbWlzcmVwcmVzZW50YXRpb24gb2YgdGhpcyBpbmZvcm1hdGlvbiBvciBpdHMgZGVyaXZhdGl2ZXMuDQo8L2Rpdj48YnI+DQoNCjxkaXYgc3R5bGU9Im1hcmdpbi1sZWZ0OjE1cHg7Zm9udC13ZWlnaHQ6bm9ybWFsOyI+DQpJZiB5b3UgaGF2ZSBvYnRhaW5lZCBpbmZvcm1hdGlvbiBmcm9tIGEgc291cmNlIG90aGVyIHRoYW4gIEdyYXlzIEhhcmJvciBDb3VudHksIGJlIGF3YXJlIHRoYXQgZWxlY3Ryb25pYyBkYXRhIGNhbiBiZSBhbHRlcmVkIHN1YnNlcXVlbnQgdG8gb3JpZ2luYWwgZGlzdHJpYnV0aW9uLiBEYXRhIGNhbiBhbHNvIHF1aWNrbHkgYmVjb21lIG91dC1vZi1kYXRlLiBJdCBpcyByZWNvbW1lbmRlZCB0aGF0IGNhcmVmdWwgYXR0ZW50aW9uIGJlIHBhaWQgdG8gdGhlIGNvbnRlbnRzIG9mIGFueSBkYXRhIGFzc29jaWF0ZWQgd2l0aCBhIGZpbGUsIGFuZCB0aGF0IHRoZSBvcmlnaW5hdG9yIG9mIHRoZSBkYXRhIG9yIGluZm9ybWF0aW9uIGJlIGNvbnRhY3RlZCB3aXRoIGFueSBxdWVzdGlvbnMgcmVnYXJkaW5nIGFwcHJvcHJpYXRlIHVzZS4gWW91IHNob3VsZCBhbHdheXMgdXNlIHRoZSBvcmlnaW5hbCByZWNvcmRlZCBkb2N1bWVudHMgZm9yIGxlZ2FsIHRyYW5zYWN0aW9ucy4NCjwvZGl2Pjxicj4NCg0KPGRpdiBzdHlsZT0ibWFyZ2luLWxlZnQ6MTVweDtmb250LXdlaWdodDpub3JtYWw7Ij4NCkluIG5vIGV2ZW50IHNoYWxsICBHcmF5cyBIYXJib3IgQ291bnR5IGJlY29tZSBsaWFibGUgdG8gdXNlcnMgb2YgdGhpcyBkYXRhLCBvciBhbnkgb3RoZXIgcGFydHksIGZvciBhbnkgbG9zcyBvciBkYW1hZ2VzLCBjb25zZXF1ZW50aWFsIG9yIG90aGVyd2lzZSwgaW5jbHVkaW5nIGJ1dCBub3QgbGltaXRlZCB0byB0aW1lLCBtb25leSwgb3IgZ29vZHdpbGwsIGFyaXNpbmcgZnJvbSB0aGUgdXNlLCBtaXN1c2UsIG9wZXJhdGlvbiBvciBtb2RpZmljYXRpb24gb2YgdGhlIGRhdGEuIEluIGFkZGl0aW9uLCB0aGUgaW5mb3JtYXRpb24gb24gdGhpcyBzZXJ2ZXIsIG9yIHNpdGUsIGlzIHN1YmplY3QgdG8gY2hhbmdlIHdpdGhvdXQgbm90aWNlIGFuZCBkb2VzIG5vdCByZXByZXNlbnQgYSBjb21taXRtZW50IG9uIHRoZSBwYXJ0IG9mICBHcmF5cyBIYXJib3IgQ291bnR5IGluIHRoZSBmdXR1cmUuDQo8L2Rpdj4NCjxicj4NCjxkaXYgc3R5bGU9Im1hcmdpbi1sZWZ0OjE1cHg7Zm9udC13ZWlnaHQ6bm9ybWFsOyI+DQpJIGhhdmUgcmVhZCwgdW5kZXJzdGFuZCBhbmQgZnVsbHkgYWdyZWUgd2l0aCB0aGlzICJEaXNjbGFpbWVyIGFuZCBUZXJtcyBvZiBTZXJ2aWNlIg0KPC9kaXY+ZGQCBQ8PFgIeDU9uQ2xpZW50Q2xpY2sFRndpbmRvdy5sb2NhdGlvbi5ocmVmPSdodHRwOi8vd3d3LmNvLmdyYXlzLWhhcmJvci53YS51cy8nOyByZXR1cm4gZmFsc2VkZGSZvOKx18uiX8ZJg/NL4prRtnI5OQ==",
			"__EVENTVALIDATION": "/wEWAwK73Yj9CQLL9vioDQKU7KHJAUUHMSTii/vTFWriXw52qN0dOpJA",
			"ctl00$cphContent$btnAgree": "I Agree"
		}

		yield scrapy.FormRequest(url, formdata=formdata, headers=self.header, method="POST", callback=self.parse_search)


	def parse_search(self, response):

		alpha_list = list(string.ascii_lowercase)

		for alpha in alpha_list[10:]:
		
			url = 'http://graysharborwa.taxsifter.com/Search/results.aspx?q='+alpha

			yield scrapy.Request(url, headers=self.header, callback=self.parse_result, dont_filter=True) 

		# for ind in range(0, 10):
		
		# 	url = 'http://graysharborwa.taxsifter.com/Search/results.aspx?q='+str(ind)

		# 	yield scrapy.Request(url, headers=self.header, callback=self.parse_result, dont_filter=True) 


	def parse_result(self, response):
 
		page_count = 0

		try:

			page_count = int(response.xpath('//div[@class="pager"][1]//div//a/@href').extract()[-1].split('page=')[1].split('&')[0].strip())

		except:

			pass

		if page_count != 0:

			for count in range(1, page_count+1):

				url = response.url+'&page='+str(count)+'&1=1#rslts'

				yield scrapy.Request(url, headers=self.header, callback=self.parse_page, dont_filter=True)


	def parse_page(self, response):

		store_list = response.xpath('//div[@id="result-area"]//div[@class="result"]//div[@class="nav"]//li//a[contains(@href, "Treasurer")]/@href').extract()

		for store in store_list:

			url = self.domain + store

			if url not in self.history:

				self.history.append(url)

				yield scrapy.Request(url, headers=self.header, callback=self.parse_detail, dont_filter=True)


	def parse_detail(self, response):

		item = ChainItem()

		item['Parcel'] = self.validate(' '.join(response.xpath('//span[@id="ctl00_cphContent_ParcelOwnerInfo1_lbParcelNumber"]//text()').extract()))

		item['Name'] = self.validate(' '.join(response.xpath('//span[@id="ctl00_cphContent_ParcelOwnerInfo1_lbOwnerName"]//text()').extract()))

		item['Address1'] = self.validate(' '.join(response.xpath('//span[@id="ctl00_cphContent_ParcelOwnerInfo1_lbAddress"]//text()').extract()))

		item['Address2'] = self.validate(' '.join(response.xpath('//span[@id="ctl00_cphContent_ParcelOwnerInfo1_lbAddress2"]//text()').extract()))

		item['City'] = self.validate(' '.join(response.xpath('//span[@id="ctl00_cphContent_ParcelOwnerInfo1_lbCity"]//text()').extract()))

		item['State'] = self.validate(' '.join(response.xpath('//span[@id="ctl00_cphContent_ParcelOwnerInfo1_lbState"]//text()').extract()))

		item['Zip'] = self.validate(' '.join(response.xpath('//span[@id="ctl00_cphContent_ParcelOwnerInfo1_lbZip"]//text()').extract()))

		balance_list = response.xpath('//table[@id="ctl00_cphContent_CurrentTaxYearInterest1_GridView1"]//a/text()').extract()

		item['Foreclosure'] = "No"	

		for balance in balance_list:

			if '2016-' in balance:

				item['Foreclosure'] = "Yes"

		item['Link'] = response.url

  		yield item
		

	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp