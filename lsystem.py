import importlib

class LVariable: #class to hold Lsystem variables
	def __init__(self, value):
		self.value = value
	rule = ""
	crule = ""

class LConstant: #class to hold Lsystem constants
	def __init__(self, value):
		self.value = value
	crule = ""

class LCRule: #class to hold movement rules, and values of how much to move
	def __init__(self, mtype, amount):
		self.mtype = mtype
		self.amount = amount

class LSystem: #class to hold the entire LSystem
	start = ""
	sourcefile = ""
	scriptfile = ""
	variables = []
	constants = []

	#drawing variables
	drawlength = 5
	nvalue = 3

	def readConstant(self,rline): #reads constant rules for variables and applies them to appropriate objects.
		#takes read line rline, and returns LCRule object
		if "(" in rline:
			rule = rline.split("(")[0]
			amount = rline.split("(")[1][:-1].rstrip()
			return LCRule(rule, amount)
		else:
			rule = rline.split("(")[0]
			return LCRule(rule, "")

	def writeConstant(self,c_str,o,i): #reads template lines and writes constant information into them.
		#takes line to edit, iterator int "i", and objects "o" that constant code are being generated for
		if "*PRE*" in c_str:
			if i == 0:
				c_str = c_str.replace("*PRE*","")
			else:
				c_str = c_str.replace("*PRE*","el")
		if "*CONST*" in c_str:
			c_str = c_str.replace("*CONST*",o.value)
		if "*MTYPE*" in c_str:
			c_str = c_str.replace("*MTYPE*",o.crule.mtype)
		if "*AMOUNT*" in c_str:
			if o.crule.amount != "":
				c_str = c_str.replace("*AMOUNT*",o.crule.amount)
			else:
				c_str = c_str.replace("*AMOUNT*","d")
		return c_str


	def readTemplate(self, filename): #imports a template file and returns it as a list of lines
		template = open(filename, 'r')
		lines = template.readlines()
		template.close()
		return lines

	def importSystem(self, filename): #imports lsystem information from .lsys file
		f = open(filename,'r')
		lines = f.readlines()
		f.close()

		for i in range(len(lines)):
			if "variables:" in lines[i]: #iterate through variables
				variables = lines[i][10:].rstrip().split(',')
				for v in variables:
					self.variables.append(LVariable(v)) #create new LComponent and append it to LSystem object
			if "constants:" in lines[i]:
				constants = lines[i][10:].rstrip().split(',')
				for c in constants:
					self.constants.append(LConstant(c))
			if "start:" in lines[i]:
				self.start = lines[i][6:].rstrip()
			if "vrules:" in lines[i]:
				x = 1
				while 1==1:
					try:
						if lines[i + x][0] == "*":
							for v in self.variables:
								if v.value == lines[i + x][1]:
									v.rule = lines[i + x][3:].rstrip()
							x += 1
						else:
							break
					except IndexError: #stop loop if running on line too near the end of the file
						break
			if "crules:" in lines[i]:
				x = 1
				while 1==1:
					try:
						if lines[i + x][0] == "*":
							for v in self.variables:
								if v.value == lines[i + x][1]:
									v.crule = self.readConstant(lines[i + x][3:].rstrip())
							for c in self.constants:
								if c.value == lines[i + x][1]:
									c.crule = self.readConstant(lines[i + x][3:].rstrip())
							x += 1
						else:
							break
					except IndexError: #stop loop if running on line too near the end of the file
						break
		self.sourcefile = filename

	def writeScript(self,filename):
		new = open(filename, 'w')

		rec_lines = self.readTemplate('templates/recursion_template.py')

		new.write("import turtle\n")

		if len(self.start) > 1: #fix for systems with more than one variable in start, need to rewrite for long starts
			for line in rec_lines:
				new_str = line
				if "*VAR*" in new_str:
					new_str = new_str.replace("*VAR*",self.start)
				if "*RULE*" in new_str:
					new_str = new_str.replace("*RULE*",self.start)
					for svar in self.start:
						for v in self.variables:
							if v.value == svar:
								new_str = new_str.replace(v.value,v.rule)
								for c in self.constants:
									new_str = new_str.replace(c.value,"\"" + c.value + "\"" + " " + "+" + " ")
								for var in self.variables:
									new_str = new_str.replace(var.value, "func_" + var.value + "(n-1)" + " " + "+" + " ")
								new_str = new_str[:-3]
				new.write(new_str)

		for v in self.variables:
			for line in rec_lines:
				new_str = line
				if "*VAR*" in new_str:
					new_str = new_str.replace("*VAR*",v.value)
				if "*RULE*" in new_str:
					new_str = new_str.replace("*RULE*",v.rule)
					for c in self.constants:
						new_str = new_str.replace(c.value,"\"" + c.value + "\"" + " " + "+" + " ")
					for var in self.variables:
						new_str = new_str.replace(var.value, "func_" + var.value + "(n-1)" + " " + "+" + " ")
					new_str = new_str[:-3]
				new.write(new_str)

		draw_lines = self.readTemplate('templates/draw_template.py')
		const_lines = self.readTemplate('templates/const_template.py')

		for line in draw_lines:
			new_str = line
			if "*STARTVAR*" in new_str:
				new_str = new_str.replace("*STARTVAR*",self.start)
			if "*CONSTANTS*" in new_str:
				new_str = ""
				for c in self.constants:
					if c.value != "[" and c.value != "]":
						for i in range(len(const_lines)):
							c_str = self.writeConstant(const_lines[i],c,i)
							new.write(c_str)
				for v in self.variables:
					if v.crule != "":
						for i in range(len(const_lines)):
							c_str = self.writeConstant(const_lines[i],v,i)
							new.write(c_str)
				for c in self.constants:
					if c.value == "[":
						bracket_lines = self.readTemplate('templates/bracket_template.py')
						for line in bracket_lines:
							new.write(line)
			new.write(new_str)

		end_lines = self.readTemplate('templates/end_template.py')

		for line in end_lines:
			new.write(line)

		new.close()
		self.scriptfile = filename

	def drawSystem(self): #draw system using created script file
		script = importlib.import_module(self.scriptfile[:-3].replace("/","."))
		script.draw(self.nvalue,script.turtle,self.drawlength)

	def executeSystem(self,source,out): #import source file, create script file, and draw
		self.importSystem(source)
		self.writeScript(out)
		self.drawSystem()
