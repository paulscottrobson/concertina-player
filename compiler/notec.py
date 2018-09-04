# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		notec.py
#		Purpose:	Note Compiler
#		Date:		4th September 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

# ****************************************************************************************
#		Compiler exceptions
# ****************************************************************************************

class ConcertinaException(Exception):
	pass

# ****************************************************************************************
#									Base Compiler
# ****************************************************************************************

class BaseNoteCompiler(object):
	#
	def __init__(self):
		self.currentDirection = None							# Push or draw direction
		self.currentRow = None 									# Current Row identifier
	#
	def compileNote(self,note,details):
		note = note.lower().strip()								# everything LC strip spaces
		#
		while note != "" and "+-pd".find(note[0]) >= 0:			# Process + - P D
			self.currentDirection = BaseNoteCompiler.PUSH 		# - and P push
			if note[0] == "d" or note[0] == "+":				# + and D draw
				self.currentDirection = BaseNoteCompiler.DRAW
			note = note[1:]										# and chuck it.
		#
		qbLength = 4 											# establish note length.
		pos = len(note)											# find the length stuff.
		while pos > 0 and "-=o.".find(note[pos-1]) >= 0:
			pos = pos - 1
		for modifier in note[pos:]:								# process the modifiers
			if modifier == ".":
				qbLength = int(qbLength * 3 / 2)
			elif modifier == "-":
				qbLength -= 2
			elif modifier == "=":
				qbLength -= 3
			elif modifier == "o":
				qbLength += 4

		note = note[:pos].strip()
		buttons = [ self.decodeButtons(note) ] if note != "&" else []

		if self.currentDirection is None:
			raise ConcertinaException("Direction of play is not set")

		if details:
			return [ self.currentDirection, buttons, qbLength ]

BaseNoteCompiler.PUSH = -1
BaseNoteCompiler.DRAW = 1


# ****************************************************************************************
#						 "Absolute Beginners" format compiler
# ****************************************************************************************

class ABSMNoteCompiler(BaseNoteCompiler):
	#
	def getCompilerType(self):
		return "ABSM"
	#
	def decodeButtons(self,descr):
		#
		#	We use B and W for PUSH and DRAW because of the colour scheme
		#
		# 	print(">>>",descr)
		if descr != "":
			if descr[0] == "b" or descr[0] == "w":
				self.currentDirection = BaseNoteCompiler.PUSH if descr[0] == "b" else BaseNoteCompiler.DRAW		
				descr = descr[1:]
		#
		#	G C # then sets the row
		#
		if descr != "":
			if "cg#".find(descr[0]) >= 0:
				self.currentRow = "gc#".find(descr[0]) * 10
				descr = descr[1:]
		if self.currentRow is None:
			raise ConcertinaException("No row specified")
		#
		#	Then 0-9 for the button
		#
		#print("["+descr+"]")
		if descr == "" or descr[0] < "0" or descr[0] > "9":
			raise ConcertinaException("Bad button number")
		buttonID = [ 0,4,3,2,1,5,6,7,8,9 ][int(descr[0])] + self.currentRow
		descr = descr[1:]
		if descr != "":
			raise ConcertinaException("Superfluous text")
		return buttonID

# ****************************************************************************************
#									Factory Class
# ****************************************************************************************

class DecoderFactory(object):
	def get(self,type):
		type = type.lower().strip()
		if type == "absm":
				return ABSMNoteCompiler()
		assert False, "Unknown factory class ID "+type


#
#	Test program
#
if __name__ == "__main__":

	bars = """
		BC5 1 1 W1- 5- 
		B2o 3o. 
		W2 1 1 B1- W2- 
 		W3 B2 W2 B1
		& 		
	""".replace("\t"," ").replace("\n"," ").split(" ")
	nc = ABSMNoteCompiler()
	for b in [x for x in bars if x.strip() != ""]:
		print(b.strip(""),nc.compileNote(b,True))

# Rests
# Chords
