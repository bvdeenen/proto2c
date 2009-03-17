#!/usr/bin/python
import sys,re


def find_messages( lines ) :
	messages=[]
	message_pattern = re.compile("\\bmessage\\W+(\\w+)\\W*{")
	for line in lines:
		if message_pattern.match(line):
			messages.append( message_pattern.sub(r'\1', line.strip()))
	return messages		

def find_enums( lines ) :
	enums=[]
	enum_pattern = re.compile("\\benum\\W+(\\w+)\\W*{")
	for line in lines:
		if enum_pattern.match(line):
			enums.append( enum_pattern.sub(r'\1', line.strip()))
	return enums		
		
		

def run_p2c():
	message_pattern = re.compile("\\bmessage\\b")
	id_pattern = re.compile("=\\W*\\d+")
	label_pattern = re.compile("\\b(repeated|optional|required)\\b")
	struct_pattern = re.compile("struct\\W+(\\w+)\W*{")
	enum_pattern = re.compile("enum\\W+(\\w+)\W*{")
	semicolon_pattern = re.compile(";")
	bracketclose_pattern = re.compile(r'}')
	package_pattern = re.compile(r'^package.*')
	include_pattern = re.compile(r'^import.*')
	default_pattern = re.compile(r'(\[default.*\])')

	for fn in sys.argv[1:] :
		f=open(fn,"r")


		print """
typedef long int32;
typedef long long int64;
typedef unsigned long uint32;
typedef unsigned long long uint64;
typedef char * string;
typedef char * bytes;
typedef int bool;
"""
		structlines=[]
		enumlines=[]
		outlines=[]

		in_enum=False
		org_lines = f.readlines()
		messages = find_messages(org_lines)
		messageptr_pattern=re.compile("\\b("+ "|".join(messages) + ")\\b")

		enums = find_enums(org_lines)
		enumptr_pattern=re.compile("\\b("+ "|".join(enums) + ")\\b")
		
		for line in org_lines:
			line=line.strip()

			if message_pattern.match(line):
				line=message_pattern.sub("struct", line)
			else:	
				line=messageptr_pattern.sub(r'\1 *', line)

			line = default_pattern.sub(r'/* \1 */',line)	
			line=id_pattern.sub("", line)
			line=label_pattern.sub(r'/*! \1 */', line)
			line=package_pattern.sub("", line)
			line=include_pattern.sub("//"+line, line)
			if struct_pattern.match(line) :
				structlines.append(struct_pattern.sub(r'typedef struct \1 \1;', line) )

			if enum_pattern.match(line) :
				# enumlines.append(enum_pattern.sub(r'typedef enum \1 * \1;', line) )
				in_enum = True
			else:	
				line=enumptr_pattern.sub(r'enum \1 *', line)
				
			if in_enum:
				line=semicolon_pattern.sub(r',', line)

			if bracketclose_pattern.match(line):
				in_enum = False
				line = bracketclose_pattern.sub(r'};', line)
			

			outlines.append(line)

		for line in structlines: print line
		for line in enumlines: print line
		for line in outlines: print line

			

if __name__ == '__main__':
	run_p2c()
	

