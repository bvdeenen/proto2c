#!/usr/bin/python
import sys,re



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
		data=f.read()
		f.close()


		print """
typedef long int32;
typedef long long int64;
typedef unsigned long uint32;
typedef unsigned long long uint64;
typedef char * string;
typedef char * bytes;
typedef int bool;
"""
		p=re.compile(r'\bmessage\W+(\w+)\W*{')
		structs=p.findall(data)
		p=re.compile(r'\benum\W+(\w+)\W*{')
		enums=p.findall(data)

		pat_message = re.compile(r'(?<!message)\W+(' + r'|'.join(structs) + r')\b' )
		enum_message = re.compile(r'(?<!enum)\W+(' + r'|'.join(enums) + r')\b' )

		in_enum=False
		f=open(fn,"r")
		org_lines = f.readlines()
		
		outlines=[]
		for line in org_lines:
			line=line.strip()

			if message_pattern.match(line):
				line=message_pattern.sub("struct", line)
			else:	
				line=pat_message.sub(r' struct \1 *', line)


			if enum_pattern.match(line) :
				in_enum = True
			else:	
				if enums:
					line=enum_message.subn(r' enum \1 ', line, 1)[0]
				
				
			if in_enum:
				line=semicolon_pattern.sub(r',', line)

			if bracketclose_pattern.match(line):
				in_enum = False
				line = bracketclose_pattern.sub(r'};', line)
			
			line = default_pattern.sub(r'/* \1 */',line)	
			line=id_pattern.sub("", line)
			m= label_pattern.match(line)
			if m :
				line=label_pattern.sub('', line) + "//!< " + m.groups(1)[0]
			line=package_pattern.sub("", line)
			line=include_pattern.sub("//"+line, line)

			outlines.append(line)

		for line in structs: print "struct "+line+";"
		for line in enums: print "enum "+line+";"
		for line in outlines: print line
		print """int main() { return 0 ;} """


			

if __name__ == '__main__':
	run_p2c()
	

