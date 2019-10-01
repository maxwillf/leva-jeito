import sys,os
import hashlib 
import json

hasher = hashlib.sha256()

root = os.getcwd()
print(root)
targetDir = os.path.join(root,sys.argv[1])
print(targetDir)

hashDict = dict()

for path,subdirs,files in os.walk(targetDir):
	for name in files:
		filename = os.path.join(path,name)
		print(filename)
		if not os.path.isdir(os.path.join(path,name)):
			f = open(filename,'rb')
			while True:
				data = f.read(1024)
				if not data:
					hashDict[os.path.join(path,name)] = hasher.hexdigest()
					print(hashDict[os.path.join(path,name)])
					break
				hasher.update(data)

json.dump(hashDict,open('JSONZAODAMASSA.JSON','w'))
