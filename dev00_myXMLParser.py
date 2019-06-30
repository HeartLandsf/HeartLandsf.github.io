#!/usr/bin/python
import re
import cgi
import cgitb
tcounter = 0
cgitb.enable()
class node(object):
	def __init__(self, tag, condition, nextp):
		global tcounter
		self.node = tag
		self.condition = condition
		self.nextp = nextp
		self.branch = []
		self.data = ''
		self.dataHappened = False
		self.id = ''
		self.nid = ''
	def infodisplay(self):
		print("node:%s condition:%s nextp:%d data:%s" % \
		(self.node, self.condition, self.nextp, self.data))
		for i in self.branch:
			i.infodisplay()
	def scan4ID(self ):
		global tcounter
		if self.node != "comment":
			#print "Node-->", self.node
			#print "data-->", self.data
			t = 1
		self.id = str(tcounter)
		tcounter += 1
		if self.node == 'term':
			self.branch[0].id = "definition" + str(self.id)
			self.branch[0].nid = str(self.id)
			self.branch[1].id = "comment" + str(self.id)
			self.branch[1].nid = str(self.id)
			return
		if len(self.branch) != 0:
			nnames = sorted([x.branch[0].data for x in self.branch], key=str.lower )
			for i in nnames:
				for term in self.branch:
					if( term.branch[0].data == i ):
						term.scan4ID()
	def renderHTML(self, op):
		#				<script type="text/javascript" src="dev00_jobindex_presentation.js"></script>\n\
		if self.node == 'xmlfile' :
			op += 'Content-type: text/html\n\n<html><head>\n\
<STYLE type="text/css">\n\
table{\n\
border:1px solid #002000;\n\
color:#003000;\n\
}\n\
tr{\n\
border:1px solid #002000;\n\
color:#003000;\n\
}\n\
th{\n\
border:1px solid #002000;\n\
color:#003000;\n\
}\n\
td{\n\
border:1px solid #002000;\n\
color:#003000;\n\
}\n\
.termdef{cursor:pointer}\n\
</style>\n\
<script type="text/javascript" src="/dev00_jobindex_presentation.js"></script>\n\
<title>' + self.data + '</title>\n\
</head>\n\
<body>\n'
			#<body style="line-height:0">\n'
			#<link rel="stylesheet" type="text/css" href="/jobindex.css" />\n\
#<STYLE type="text/css">\n\
#table{\n\
#border:3px solid #002000;\n\
#color:#003000;\n\
#}\n\
#tr{\n\
#border:1px solid #002000;\n\
#color:#003000;\n\
#}\n\
#th{\n\
#border:1px solid #002000;\n\
#color:#003000;\n\
#}\n\
#td{\n\
#border:1px solid #002000;\n\
#color:#003000;\n\
#}\n\
#.termdef{cursor:pointer}\n\
#</style>\n\
		elif self.node == 'data':
			op += '<table cellspacing=0 cellpadding=0>'
			self.dataHappened = True
			nnames = sorted([x.branch[0].data for x in self.branch], key=str.lower )
			if len(self.branch) != 0:
				for i in nnames:
					for term in self.branch:
						#print "---"+term.branch[0].data
						if( term.branch[0].data == i ):
							op = term.renderHTML(op)
			return op			
		elif self.node == 'term':
			op += '<tr>\n'
		elif self.node == 'definition':
			op += '<th align="left" class="termdef" id="' + self.id + '" onclick=displayComment("' + self.nid + '")>\n' + self.data + '</th>\n'
		elif self.node == 'comment':
			op += '<td id="' + self.id + '" style="display:none">\n' + self.data + '</td>\n</tr>\n'
		if len(self.branch) != 0:
			for i in self.branch:
				op = i.renderHTML(op)
		if self.node == 'xmlfile':
			if self.dataHappened:
				op += '</table>\n'
			op += '</table>\n</body>\n</html>\n'
		return op

def jumpOnSpacings(banner):
	i = 0
	while( i<len(banner) and re.match("\s",banner[i]) ):
		i+=1
		continue
	while( i<len(banner) and re.match("<br>",banner[i:i+4]) ):
		i+=4
		continue
	return i
def foundkey(var, tptr, keylist):
	ptr = tptr
	for i in keylist:
		b = '<' + i + '>'
		j = '</' + i + '>'
		s = var[ptr:ptr+len(j)]
		t = var[ptr:ptr+len(b)]
		#print 'b->'+b+'|j->'+j+'|s->'+s+'|t->'+t,
		if( s == j ):
			#print 'match->' + s+' '+j+' '
			item = node(i,'close', ptr + len(i) + 3 + jumpOnSpacings(var[ptr+len(i)+3:]))
			item.datae = ptr
			#print
			return item
		elif( t == b ):
			#print 'match->' + t+' '+i+' '
			item = node(i,'open',ptr +  len(i) + 2 + jumpOnSpacings(var[ptr+len(i)+2:]))
			ptr = item.nextp
			if( var[ptr] == '<' ):
				#print
				return item
			else:
				#var = var[ptr:]
				#print "shovel->" + var[0:10]
				item.data = var[ptr:ptr+var[ptr:].index(j)]
				item.nextp += len(item.data)
				return item
	item = node('', 'na', 0)
	return item
def parseXmlByKeywords2Tree(banner, i, keywords):
	tstack = []
	tstack.append( node('xmlfile', 'open', 0))
	while(i<len(banner)):
		#	print "this time:"+str(i)
		i += jumpOnSpacings(banner[i:])
		if( i >= len(banner) ):
			break
		kf = foundkey(banner, i, keywords)
		#kf.infodisplay()
		#print '==>' + banner[i:i+20]
		if( kf.condition == 'open'):
			# tree grows deeper
			#print "found->"+kf.node
			i = kf.nextp
			tstack[-1].branch.append(kf)
			tstack.append(kf)
			#print "stack->"+str(len(tstack))+" node:"+kf.node+" "+kf.condition+" nextp:"+str(kf.nextp)
		elif( kf.condition == 'close'):
			#print "node closed<-- "+kf.node
			#print "stack->"+str(len(tstack))+" node:"+kf.node+" "+kf.condition
			latest = tstack.pop()
			latest.condition = 'closed'
			#print "latest node:"+latest.node+" latest nextp:"+str(latest.nextp)+" kf.node:"+kf.node+" kf.datae:"+str(kf.datae)
			if latest.data == '':
				latest.data = banner[latest.nextp:kf.datae ]
			tstack[-1].nextp = kf.nextp
			i = kf.nextp
		else:
			#print 'i->'+str(i)+' banner=' + banner[i:i+20]
			i += 1
	tstack[0].condition = 'closed'
	#return tstack[0]
	return tstack
def myParsexml(path, keywords):
	with open(path, 'r') as fhdl:
		xmlc = fhdl.read();
		formalxmlkeyws = ['?xml version="1.0"?', 'table', 'tr', 'th', 'td', 'br',\
		'ol', 'ul', 'html', 'header', 'title', 'body', 'h1', 'h2', 'h3', 'h4', \
		'h5', 'h6', 'a', 'p', 'li']
	dictlist = parseXmlByKeywords2Tree(xmlc, 0, keywords )
	return dictlist
