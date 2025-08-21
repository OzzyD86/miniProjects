from PIL import Image, ImageDraw

import sqlite3
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class xori():
	def __init__(self):
		self.loaded = None
		self.src = None
		self.ret = None
		self.pos = (0,0,0)
	pass

	def list_results(self):
		out = []
		for i in cur.execute("select id from encro where `pos` is not null"):
			#print(dict(i))
			out.append(i['id'])
		return out
	
	def load_source(self, src):
		self.src = Image.open(src)
		if (self.ret is None ) or (self.src.dize == self.ret.size):
			return True
		else:
			return False
			
	def load_result_from_db(self,pos):
		e = cur.execute("select * from encro where id =?", (pos,))
		f = e.fetchone()
		self.loaded = pos
		self.ret= Image.open(io.BytesIO(f["img"]))
		self.pos = (tuple(map(int, f["pos"].split(","))))
		
		if (self.ret.size == self.src.size):
			print (True)
		else:
			print(False)
		return self.ret, self.pos
			
	def en(self, tex, img, st = (0,0,0)):
		if (self.ret is None):
			i = Image.new("RGB", self.src.size, (0,0,0))
		else:
			i = self.ret
		
		l=st[2]
		x,y=st[0:2]
		tex = list(tex)
		c = img.load()
		jj = i.load()
		while len(tex) > 0:
			d = tex.pop(0)
	
			b = c[x,y]
			n1 = format(b[l], "#010b")[2:]
			n2 = format(ord(d), "#010b")[2:]
		#print(n1,n2)
		#print(type(n1))
			ob = "0b"
			for j in range(len(str(n1))):
				if (n1[j] == n2[j]):
					ob += "0"
				else:
					ob += "1"
		#print(int(ob[2:],2))
			e = list(jj[x,y])
			e[l] = int(ob[2:],2)
			jj[x,y] = tuple(e)
			l += 1
			if (l >= 3):
				#print(jj[x,y])
				l=0
				x+=1
				if (x >= i.size[0]):
					y+=1
					x=0
					print(y)
					if (y >= i.size[1]):
						#self.ret = Image.new("RGB", self.src.size, (0,0,0))
						self.pos = None
						return False, i, "".join(tex)
			#print(j)
		self.ret = i
		self.pos = (x,y,l)
		return True, i,(x,y,l)
		
	def ret_save(self):
		
		stream = io.BytesIO()
		self.ret.save(stream, format="PNG")
		if (self.loaded is not None):
			if (self.pos is not None):
				ppos = ",".join(map(str,self.pos))
			else:
				ppos = None
			cur.execute("update encro set img = ?, pos = ? where id = ?", (stream.getvalue(), ppos, self.loaded))
		else:
			cur.execute("insert into encro (img, pos) values (?,?)", (stream.getvalue(), ",".join(map(str,self.pos))))
			self.loaded = None
		db.commit()

	def de(self, start=(0,0,0),end=None):
		src = self.src
		im = self.ret
		x,y,z = list(start)
		out =""
		a = im.load()
		b = src.load()
		
		while (x <= end[0] or y <= end[1] or z <= end[2]):
			#print(x,y,z)
		
			n1 = format(a[x,y][z], "#010b")[2:]
			n2 = format(b[x,y][z], "#010b")[2:]
			
			ob = "0b"
			for j in range(len(str(n1))):
				#print(type(n1[j]))
				if (n1[j] == "0"):
					ob += n2[j]
				else: 
					if (n2[j] == "0"):
						ob += "1"
					else:
						ob += "0"
			
			c = chr(int(ob[2:],2))
			#print(n1,n2,ob,c)
			out += c
		
			z += 1
			if (z >= 3):
				z=0
				x+=1
				if (x >= im.size[0]):
					y+=1
					x=0
					#print(y)
		return out
		
enc = xori()

#p = enc.load_source("Image_fx-419.jpg")
#p = enc.load_source("Image_fx-614.jpg")
p = enc.load_source("Copy-1.jpg")
db = sqlite3.connect("imgenc.db")
db.row_factory = sqlite3.Row
cur = db.cursor()

#cur.execute("drop table encro")
#cur.execute("create table encro (`id` integer not null primary key autoincrement, `pos` text null, `img` blob)")

x = enc.src
print(x.size)
print(p)

cap = "\n"
cap += '''I need to keep adding data because I need to get close to the end! '''

cap += "This is a further test. Also, that should be enough to see the system make NEW stuff at the end of this!\n Can I make this process faster please? Mermaid nipples! " * 99
cap += "\n"
cap2 = "Nipples! "
cap *=1
cap += cap2 * 100
cap *= 5
import io

inputs = enc.list_results()
print(inputs)
if (len(inputs) > 0):
	r,ret = enc.load_result_from_db(inputs[0])
	print(r,ret)
	
print(enc.src.size, enc.ret.size)
print(len(cap))

buf_spa = 2500
while (len(cap) > buf_spa):
	co, cap = cap[:buf_spa], cap[buf_spa:]
	#print(len(co), len(cap), len(cap+co))
	
	suc,r,ret = enc.en(co, x, ret)
	while (suc is False):
		enc.ret_save()
		r.save("last.png")
		# Make a new output image
		enc.loaded = None
		ret = (0,0,0)
		enc.ret = None
		suc,r,ret = enc.en(cap, x, ret)

# Whatever's left
suc,r,ret = enc.en(co, x, ret)
while (suc is False):
	enc.ret_save()
	r.save("last.png")
	# Make a new output image
	enc.loaded = None
	enc.ret = None
	ret = (0,0,0)
	suc,r,ret = enc.en(cap, x, ret)

print(r,ret)
enc.ret_save()

import math as maths
nn = 150#maths.floor((x.size[1] * x.size[0] * 3) / len(cap))
#print(nn)

#for i in range(nn-1):
#	r,ret = en(cap, x, ret,r)
r.save("t.png")

#cur.execute("insert into encro (`img`,`pos`) values (?,?)", (stream.getvalue() , ",".join(map(str,ret))))
#db.commit()
#o =enc.de(start=(0,50,0), end=(0,51,0))
#print(o)