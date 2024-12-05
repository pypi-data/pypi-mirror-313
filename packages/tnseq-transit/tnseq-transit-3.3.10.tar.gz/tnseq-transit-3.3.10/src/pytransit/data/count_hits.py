import sys
a,b = 0,0
for line in open(sys.argv[1]):
  if line[0]=='#': continue
  w = line.rstrip().split('\t')
  a += 1
  if float(w[-1])<0.05: b += 1
print a,b
