#!/usr/bin/python
import cgi
import cgitb
from dev00_myXMLParser import *
cgitb.enable()
keyws = ['data', 'term', 'definition', 'comment']
dictlist = myParsexml('/var/www/terms.xml', keyws)
for i in dictlist:
	i.scan4ID()
op = ''
for i in dictlist:
	op += i.renderHTML('')
print op
