from colorsys import hsv_to_rgb

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h,s,v))

from PIL import Image, ImageFont, ImageDraw
import math as maths
import os

def rotate(point, by, around = (0,0)):
	by = (maths.radians(by))
	x = point[0] - around[0]
	y = point[1] - around[1]
	ox = ((x * maths.cos(by) )+ (y * maths.sin(by)))
	oy = ((y * maths.cos(by)) + (x * maths.sin(by)))
	
	return (ox + around[0], oy + around[1])
	
def select(ov, num = None):
	out = {}
	for i,j in ov.items():
		if ("rel" in j and num in j["rel"]):
			out[i] = j
		elif ("rel" not in j and num is None):
			out[i] = j
	ls = []
	for i,j in out.items():
		ls.append([i,j])
	return ls
	return out
	
def faob(i, band=0):
	out = {}
	for j,k in i.items():
		
		if "band" in k and k["band"] == band:
			out[j] = k
	return out

class circle():
	def __init__(self, i):
		self.i = i
		self.pics = []
		self.hl = []
	
	def xOverlay(self, origin, mn, mx, sz = 1000, sh=(1080,1080)):
		x = Image.new("L", sh)
		d = ImageDraw.Draw(x)
		d.pieslice((origin[0]-sz,origin[1]-sz,origin[0]+sz,origin[1]+sz),start=mn,end=mx,fill=255)
		return x.transpose(Image.FLIP_LEFT_RIGHT)
		pass
		
	def setc(self):
		self.a = select(self.i)
		c = 0
		for j in self.a:
			self.i[j[0]]["band"] = 0
			c+= 1
		return c
		pass
		
	def doBands(self):
		bds= 0
		a = self.a
		y = True
		while( y):
			y = False
			o = []
			for j in a:
				z = select(self.i, j[0])
				c = 0
				for k in z:
					if ("ignore" not in self.i[k[0]] or self.i[k[0]]["ignore"] is not True):
						if ("band" in self.i[j[0]]):
							self.i[k[0]]["band"] = self.i[j[0]]["band"] +1
							c+= 1
				o += z
			if (len(o) > 0):
				a = o
				y = True
				bds+= 1

		for n in range(bds,0,-1):
			#print(n)
			for a,b in faob(self.i,n).items():
				#print(a, b["rel"][0])
				if ("children" in self.i[b["rel"][0]]):
					if ("children" in b):
						self.i[b["rel"][0]]["children"] += b["children"]
					else:
						self.i[b["rel"][0]]["children"] += 1
				else:
					if ("children" in b):
						self.i[b["rel"][0]]["children"] = b["children"]
					else:
						self.i[b["rel"][0]]["children"] = 1
						
		self.bds = bds
		
	def predraw(self):
		c = 0
		a = select(self.i)
		print(a)
		tot = a[0][1]["children"]

		for j in a:
			self.i[j[0]]["scope"] = { "min": c/len(a)*360, "max": (c+1)/len(a)*360 }

		y = True
		while( y):
			y = False
			o = []
			for j in a:
				z = select(self.i, j[0])
				mn = self.i[j[0]]["scope"]
				if ("children" in self.i[j[0]]):
					ch = self.i[j[0]]["children"]
				else:
					ch = 1
				c = 0
				for k in z:
					if ("children" not in self. i[k[0]]):
						d = 1
					else:
						d = self.i[k[0]]["children"]
					
					#print(k[0], d)
					self.i[k[0]]["scope"] = {"min":mn["min"] + ((c) / ch * (mn["max"]  - mn["min"])),"max":mn["min"] + ((c + d) / ch * (mn["max"]  - mn["min"]))}
					#i[k[0]]["band"] = i[j[0]]["band"] +1
					c+= d
				o += z
				
			#print(o)
			if (len(o) > 0):
				a = o
				y = True
				
	def addHighlight(self, pic, ls = []):
		self.pics.append(pic)
		self.hl.append(ls)
		
	def draw(self, name = "nump2.png", pt = 100):

		d = (1080, 1080)
		fnt = ImageFont.truetype( "assets/arial.ttf", 12)
		#pt = 85
		ox = Image.new("RGB", d, (0,0,0))
		id = ImageDraw.Draw(ox)
		#ox.paste(Image.open("001.png").resize((1080,1080)), (0,0), self.xOverlay((540,540), 0,90))

		for op in self.hl:
			fl = self.pics.pop(0)
			if (os.path.exists(fl)):
				for oop in op:
				#print(self.i[oop])
					ox.paste(Image.open(fl).resize((1080,1080)), (0,0), self.xOverlay((540,540), self.i[oop]["scope"]["min"]+90, self.i[oop]["scope"]["max"]+90))
			else:
				print(fl + " not found")
		for qq in range(self.bds):
			#print(qq)
			x = pt * (qq+1)
			id.ellipse(((d[0]/2) - x, (d[1]/2)-x, (d[0]/2) + x, (d[1]/2) +x), outline=(192,63,63))
	
		for j,p in self. i.items():
			if ("band" in p and ("ignore" not in p or p["ignore"] is not True)):
				bdr = maths.radians((p["scope"]["max"] + p["scope"]["min"]) / 2)
				x = (d[0] / 2) +((p["band"] * pt) * maths.sin(bdr))
				y = (d[1] / 2) +((p["band"] * pt) * maths.cos(bdr))
				self.i[j]["pos"] = {"x":x,"y":y}
	
				if ("colour" in self.i[j] and self.i[j]["colour"] is not None):
					c = self.i[j]["colour"]
				else:
					c = hsv2rgb((p["scope"]["min"]+ p["scope"]["max"])/2/360, 1, 1.0)# (255,255,255)
		#print(c)
				id.ellipse((self.i[j]["pos"]["x"] -5, self.i[j]["pos"]["y"]-5,self.i[j]["pos"]["x"]+5,self.i[j]["pos"]["y"]+5), outline=c)
				
				t = fnt.getbbox(self.i[j]["name"])
				o = Image.new("RGBA", (t[2], t[3]), (0,0,0,0))
				to = ImageDraw.Draw(o)
				mp = (t[0]/2, t[1]/2)
				to.text((0, 0), self.i[j]["name"], font=fnt, fill=c)
				rto = maths.degrees(bdr)+90
				if (rto < 270):
					rto += 180
				o = o.rotate(rto, expand=True)
				pot = rotate((x + 7 + mp[0], y + mp[1]), maths.degrees(bdr)+90, (x+7, y))
				nib = rotate(mp, maths.degrees(bdr)-90)
				#nib = (o.size[0]/2, o.size[1]/2)
				#print(t)
				if (maths.cos(bdr) >= 0):
					yy = 0
				else:
					yy = -o.size[1]
					
				if (maths.sin(bdr) >0):
					xx = 7
				else:
					xx = -o.size[0]
				
				#id.line((x,y, x+xx,y+yy), fill=(255,255,255))
				ox.paste(o, (int(x + xx), int(y + yy)), o)
				#id.text((x+7, y), str(j), font=fnt, fill=c)

		for j,p in self.i.items():
			if ("band" in p) and ("ignore" not in p or p["ignore"] is not True):
				if ("colour" in p and p["colour"] is not None):
					c = p["colour"]
				else:
					c = hsv2rgb((p["scope"]["min"]+ p["scope"]["max"])/2/360, 1, 1.0)# (255,255,255)
				if ("rel" in p):
					for k in p["rel"]:
						#print(i[j], i[k])
						if ("ignore" not in self.i[k] or self.i[k]["ignore"] is not True):
							id.line((self.i[j]["pos"]["x"],self.i[j]["pos"]["y"],self.i[k]["pos"]["x"], self.i[k]["pos"]["y"]), fill=c)
	#print(p)
		ox.save(name)
		pass
