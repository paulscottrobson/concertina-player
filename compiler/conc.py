# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		conc.py
#		Purpose:	Song Compiler
#		Date:		4th September 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from notec import ConcertinaException,NoteCompilerFactory
import os,sys

# ****************************************************************************************
#									Compiler class
# ****************************************************************************************

class SongCompiler(object):
	def __init__(self,file,target):
		SongCompiler.FILENAME = file
		SongCompiler.LINENUMBER = 0
		if not os.path.exists(file):
			raise ConcertinaException("File not found "+file)
		self.src = [x.strip().lower().replace("\t", " ") for x in open(file).readlines()]
		self.src = [x if x.find("//") < 0 else x[:x.find("//")].strip() for x in self.src]
		self.keys = { "beats":"4","tempo":"100","format":"absm" }
		for c in [x for x in self.src if x.find(":=") >= 0]:
			c = [x.strip() for x in c.split(":=")]
			if c[0] not in self.keys:
				raise ConcertinaException("Unknown key "+c[0])
			self.keys[c[0]] = c[1]
		self.src = [x if x.find(":=") < 0 else ""for x in self.src]
		self.bars = []
		compiler = NoteCompilerFactory().get(self.keys["format"])
		for i in range(0,len(self.src)):
			SongCompiler.LINENUMBER = i + 1			
			for barSrc in [x for x in self.src[i].split("|") if x.strip() != ""]:
				barLength = 0
				bar = [ compiler.compileNote(x,False) for x in barSrc.split(" ") if x != ""]
				for bEncode in bar:
					length = ord(bEncode[-1]) - ord('a') + 1
					barLength += length
				if barLength > int(self.keys["beats"]) * 4:
					raise ConcertinaException("Bar overflow")
				self.bars.append(";".join(bar))
		h = open("winster.json","w")
		h.write("{\n")
		for k in self.keys.keys():
			h.write('    "{0}":"{1}",\n'.format(k,self.keys[k]))
		h.write('    "bars": [\n')
		h.write(",\n".join(['{1:12}"{0}"'.format(x,"") for x in self.bars]))
		h.write('\n    ]\n}\n')
		h.close()

if __name__ == "__main__":
	SongCompiler("winster.conc","winster.json")		
