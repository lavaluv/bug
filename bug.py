#coding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import sys
import re
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')

def get_content(raw):
	content_list = re.findall(ur"[\u4e00-\u9fa5]+",raw)
	return "".join(content_list)

def get_seg_list(content):
	return jieba.cut(content,cut_all=False, HMM=True)

def count_words(word_list):
	return len(set(word_list))

def get_word_frequency(word_list):
    frequency_dict = dict()
    for w in word_list:
        if frequency_dict.has_key(w):
            frequency_dict[w] = frequency_dict[w] + 1
        else:
            frequency_dict[w] = 1
    return frequency_dict

fileName = "url1.txt"
with open (fileName,'r') as file_to_read:
	while True:
		url = file_to_read.readline()
		# url = ''.join(url).strip("\n")
		print(url)
		if not url:
			break
		#driver = webdriver.PhantomJS(executable_path = "/Users/lava/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
		driver = webdriver.Firefox()
		try:
			driver.get(url)
		except Exception as e:
			print('error page')
		page = driver.page_source
		fileStr = url
		dirname = os.path.dirname(fileStr)
		if not os.path.exists(dirname):
			os.makedirs(dirname)
		f = open(fileStr,"w")
		f.write(page)
		f.close()
		html = BeautifulSoup(page,'html.parser')
		# print repr(html.title.get_text).decode('unicode-escape')
		reg = re.compile("<[^>]*>")
		#title
		#print(reg.sub('',html.title.prettify()))
		tF = open(fileStr + '.title','w')
		if html.title:
			tF.write(reg.sub('',html.title.prettify()))
		tF.close()
		#form
		form = html.select('form')
		fF = open(fileStr + '.form','a')
		for i in form:
			s = reg.sub('',i.prettify()).strip()
			print("%s: %s" % (form.index(i) + 1,re.sub('[\r\n\t]','',s)))
			fF.write(re.sub('[\r\n\t]','',s))
		fF.close()
		#img
		img_list = html.findAll('img',attrs={'src',True})
		imgF = open(fileStr + '.img','a')
		for img in img_list:
			try:
				print img.attrs['src']
				imgF.write(img.attrs['src'])
			except Exception as e:
				print e.message
		imgF.close()
		#script
		scriptF = open(fileStr + '.script','a')
		s_list = html.findAll('script')
		for s in s_list:
			if s.attrs:
				print s.attrs
				scriptF.write(str(s.attrs))
		scriptF.close()
		#source
		inF = open(fileStr + '.source','a')
		in_list = html.findAll('source')
		for In in in_list:
			if In.attrs:
				print In.attrs
				inF.write(str(In.attrs))
		inF.close()
		#iframe
		ifF = open(fileStr + '.iframe','a')
		if_list = html.findAll('iframe')
		for If in in_list:
			if If.attrs:
				print If.attrs
				ifF.write(str(If.attrs))
		ifF.close()
		#frame
		frameF = open(fileStr + '.frame','a')
		f_list = html.findAll('frame')
		for f in in_list:
			if f.attrs:
				print f.attrs
				frameF.write(str(f.attrs))
		frameF.close()
		#link	
		lF = open(fileStr + '.link','a')
		for l in html.select('link'):
			print l
			lF.write(str(l))
		lF.close()
		#a
		aF = open(fileStr + '.a','a')
		for a in html.select('a'):
			print a
			aF.write(str(a))
		aF.close()
		#footer
		footerF = open(fileStr + '.footer','w')
		print(html.footer)
		footerF.write(str(html.footer))
		footerF.close()
		#full_text
		[script.extract() for script in html.findAll('script')]
		[style.extract() for style in html.findAll('style')]
		html.prettify()
		content = reg.sub('',html.prettify())
		print(content)
		fullF = open(fileStr + '.full','w')
		fullF.write(str(content))
		fullF.close()
		#get seg
		segF = open('seg.txt','a')
		seg_list = get_seg_list(get_content(content))
		for nextObj in seg_list:
			segF.write(str(nextObj)+'|')
		print count_words(get_seg_list(get_content(content)))
		print (repr(get_word_frequency(get_seg_list(get_content(content)))).decode('unicode-escape'))
		assert "No results found." not in driver.page_source
		driver.close()
	pass
	file_to_read.close()
	segF.close()
