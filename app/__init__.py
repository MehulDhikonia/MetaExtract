from flask import Flask

app = Flask(__name__)
#app.config.from_object('config')

#import views
import re, lxml.html, MySQLdb
from lxml import etree
from urllib import urlopen
from urlparse import urlparse
from flask import render_template, flash, redirect, request
#from app import app

##Redirect to homepage
def get_home(url):
	parsed_uri = urlparse(url)
	domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	return domain

##Parse Title from html home page
def get_title(url):
	t = lxml.html.parse(url)
	Title = t.find(".//title").text
	return Title

##Parse Keywords if available
##Meta keywords are generally specified with name="Keywords" or name="keywords". Checking both possibilities.
def get_keywords(url):
	tmp = urlopen(url).read()
	tree = etree.HTML(tmp)
	if len(tree.xpath("//meta[@name='Keywords']"))>0:
		KeyWords = tree.xpath("//meta[@name='Keywords']")[0].get("content")
		return KeyWords
	elif len(tree.xpath("//meta[@name='keywords']"))>0:
		KeyWords = tree.xpath("//meta[@name='keywords']")[0].get("content")
		return KeyWords
	else:
		KeyWords = ""
		return KeyWords

##Parse Description if available
##Meta Description is specified with name="Description" or name="description". Checking both possibilities.
def get_desc(url):
	tmp = urlopen(url).read()
	tree = etree.HTML(tmp)
	if len(tree.xpath("//meta[@name='Description']"))>0:
		Desc = tree.xpath("//meta[@name='Description']")[0].get("content")
		return Desc
	elif len(tree.xpath("//meta[@name='description']"))>0:
		Desc = tree.xpath("//meta[@name='description']")[0].get("content")
		return Desc
	else:
		Desc = ""
		return Desc



global URL
URL = ""

@app.route('/')
@app.route('/index', methods=['POST'])
def index():
	global URL
	#form = enterURL()
	#if form.validate_on_submit():
	#	print form.url.data
	#	return redirect('/insert')

	#return render_template('index.html',form=form)
	return render_template('index.html')

@app.route('/insert', methods=['GET','POST'])
def insert():
	global URL
	if request.method == 'POST':
		print request.form['url']
		URL = request.form['url']
		domain = get_home(URL)
		title = get_title(domain)
		keywords = get_keywords(domain)
		description = get_desc(domain)
		#print domain
		#print title
		#print keywords
		#print description
	return render_template('insert.html', home = domain, title = title, keywords = keywords, description = description)

@app.route('/save', methods=['GET','POST'])
def save():
	global URL
	home = request.form['HomePage']
	title = request.form['Title']
	keywords = request.form['Keywords']
	description = request.form['Description']
	db = MySQLdb.connect("localhost","root","","MetaExtract")
	cursor = db.cursor()
	sql = "INSERT INTO meta (URL, HomePage, Title, KeyWords, Description) VALUES (%s, %s, %s, %s, %s)"
	try:
		cursor.execute(sql, (URL, home, title, keywords, description))
		db.commit()
	except:
		db.rollback()
	db.close()
	print URL
	return render_template('save.html')


if __name__ == "__main__":
    app.run()
