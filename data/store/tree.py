
class tree():
	def __init__(self):
		self.counter = 0
		self.x = {}
	
	def find(self, name = "", pos = 0):
		out = []
		for i,j in self.x.items():
			if j["name"] == name:
				out.append(i)
			pass
		if (len(out) > pos):
			return out[pos]
		else:
			return None
			
	def reserve(self, id):
		if (id in self.x):
			p = self.counter
			self.x[p] = self.x[id].copy()
			
			for j,i in self.x.items():
				print(i)
				if ("rel" in i and id in i["rel"]):
					x = i["rel"]
					#print(x)
					x.remove(id)
					x.append(p)
					self.x[j]["rel"] = x.copy()
					#print(x)
			del self.x[id]
		self.counter += 1
		
	def erase(self, id):
		self.x[id]["ignore"] = True
		#del self.x[id]
		
	def add(self, name, rel = None,colour=None):
		if (rel is not None):
			self.x[self.counter] = {"name":name,"rel":[rel]}
		else:
			self.x[self.counter] = {"name":name}
		
		if (colour is None):
			if rel is not None and "colour" in self.x[rel]:
				colour = self.x[rel]["colour"]
		
		self.x[self.counter]["colour"] = colour
		c = self.counter
		self.counter+= 1
		return c
		
	def getList(self):
		return self.x