import re
#opening file for reading
with open('the-hound-of-the-baskervilles.txt',"r") as f:
	contents = f.read()
fout = open('assign1c.txt', 'w')
#splitting into words at special characters and spaces
words = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>? \n]', contents)
#creating dictionary
d={}

for w in words:
	
	#if word in dict, incrementing freq count
	if w in d:
		d[w]+=1
	#else add word to dict, with freq count 1
	elif w != "" and w != "s" and w != "re" and w != "ll": #eliminating some invalid words like '', 's'(from that's etc) and 're' from 'they're'
		d[w]=1
for w in sorted(d):
	print w, d[w] #printing to console
	#writing to file
	fout.write(w)
	fout.write(' ')
	fout.write(str(d[w]))
	fout.write('\n')
print "Please open assign1c.txt to read complete list."
fout.close()
