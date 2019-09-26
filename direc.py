import sys,os
import hashlib 

hasher = hashlib.sha256()

root = os.getcwd()
print(root)
targetDir = os.path.join(root,sys.argv[1])
print(targetDir)

for path,subdirs,files in os.walk(targetDir):
	for name in files:
		filename = os.path.join(path,name)
		print(filename)
		if not os.path.isdir(os.path.join(path,name)):
			f = open(filename,'rb')
			while True:
				data = f.read(1024)
				if not data:
					print(hasher.hexdigest())
					break
				hasher.update(data)

