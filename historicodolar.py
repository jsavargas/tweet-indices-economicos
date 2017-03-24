#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Twitter Credenciales


import twitter
from datetime import datetime
import commands

from bs4 import BeautifulSoup
import requests
import urllib
import httplib
import json
import sys
import sys, traceback
from datetime import datetime, timedelta


var_consumer_key=''
var_consumer_secret=''
var_access_token_key=''
var_access_token_secret=''


api = twitter.Api(consumer_key=var_consumer_key,
	consumer_secret=var_consumer_secret,
	access_token_key=var_access_token_key,
	access_token_secret=var_access_token_secret)




# Pagina
link       = "http://www.sii.cl/pagina/valores/dolar/dolar2017.htm"
host       = "www.sii.cl"
parametros = "" 
headers    = {
"Cache-Control":"max-age=300, proxy-revalidate, private",
"Connection":"Keep-Alive",
"Date":"Fri, 24 Mar 2017 13:23:06 GMT",
"Expires":"Fri, 24 Mar 2017 13:28:06 GMT",
"Keep-Alive":"timeout=30",
"Server":"Apache",
"Vary":"Accept-Encoding,User-Agent",
"X-Pad":"avoid browser bug"
}


conexion   = httplib.HTTPConnection(host)
conexion.request("POST", link, parametros, headers)
respuesta  = conexion.getresponse()
ver_source = respuesta.read()
#print "\nSOURCE =====> \n"
#print ver_source
#print "\nSOURCE <===== \n"

#sys.exit(0)


if respuesta.status == 200:
	#Pagina web ver_source
	soup = BeautifulSoup(ver_source, 'html5lib')
	#print soup
	entradas = soup.find_all('tr')
	a=[['0','0']]
	for i in xrange(1,len(entradas)): #		
		columnas = entradas[i].find_all('td')
		columnasth = entradas[i].find_all('th')
		if len(columnas)>0:
			dia=columnasth[0].text.strip(" ").replace("&nbsp", "").strip()
			#print "DIA: ",columnasth[0].text.strip(" ").replace("&nbsp", "").strip()
			enero=columnas[0].text.strip(" ").replace("&nbsp", "").strip()
			#print "ENERO: ",columnas[0].text.strip(" ").replace("&nbsp", "").strip()
			febrero=columnas[1].text.strip(" ").replace("&nbsp", "").strip()
			#print "FEBRERO: ",columnas[1].text.strip(" ").replace("&nbsp", "").strip()
			marzo=columnas[2].text.strip(" ").replace("&nbsp", "").strip()
			#print "MARZO: ",columnas[2].text.strip(" ").replace("&nbsp", "").strip()
			#print "ABRIL: ",columnas[3].text.strip(" ").replace("&nbsp", "").strip()
			#print "Fecha: %s Estado: %s Oficina: %s" % (columnas[1].text.strip(" ").replace("&nbsp", "").strip(),columnas[0].text.strip(" ").replace("&nbsp", "").strip(),columnas[2].text.strip(" ").replace("&nbsp", "").strip())
			#print ""
			a.append([dia,enero,febrero,marzo])
			
			
	#print a
	array_dia=["Dom","Lun","Mar","Mie","Jue","Vie","Sab"]
	array_mes=["","Enero","Febrero","Marzo","Abril"]

	var_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	dia=datetime.now().strftime('%d')
	mes=datetime.now().strftime('%m')
	dianombre=array_dia[int(datetime.now().strftime('%w'))]
	
	myvstring=''
	for num in range(5, 0, -1):  #to iterate between 10 to 20
		num = int(num) - 1
		#print "[",num,"]"
		vardianombre7=array_dia[int((datetime.now() - timedelta(days=num)).strftime('%w'))]
		vardiafecha7=str((datetime.now() - timedelta(days=num)).strftime('%d/%m/%y'))
		dia=int((datetime.now() - timedelta(days=num)).strftime('%-d'))
		mes=int((datetime.now() - timedelta(days=num)).strftime('%-m'))
		#print "d[",dia,"]"
		#print "m[",mes,"]"
		#print "usd[",a[dia][mes],"]"
		dolar=a[dia][mes]	
		if len(dolar)==0: dolar = '--'
		myvstring=myvstring + "\n" + str(vardianombre7) + " " + str(vardiafecha7) + " Dolar: " + str(dolar)
		#print (myvstring)
		#print len(myvstring)
	
	#print (myvstring)
	print "largo del mensaje: ",len(myvstring)

var_date=datetime.now().strftime('%I %p')

print var_date,"",myvstring
status = api.PostUpdate(var_date+myvstring)
