import sys,os
import hashlib 
import json
import argparse

#def dumpsToFile(hashDict,directory):
#  if not os.path.exists('.vigia'):
#    os.mkdir('.vigia')
#    os.mkdir(directory)
#  else:
#    if not os.path.exists(directory)

def writeToFile(hashDict):
  json.dump(hashDict,open('.vigia.json','w'))


def generateDirHashes(directory):

  hasher = hashlib.sha256()
  root = os.getcwd()
  print(root)
  #targetDir = os.path.join(root,sys.argv[1])
  targetDir = os.path.join(root,directory)
  print(targetDir)

  hashDict = dict()

  for path,subdirs,files in os.walk(targetDir):
    for name in files:
      filename = os.path.join(path,name)
      #print('[W]',filename)
      if not os.path.isdir(os.path.join(path,name)):
        f = open(filename,'rb')
        while True:
          data = f.read(1024)
          if not data:
            hashDict[os.path.join(path,name)] = hasher.hexdigest()
            print('[W]',filename)
            print(hashDict[os.path.join(path,name)])
            break
          hasher.update(data)
  writeToFile(hashDict)

def trackDirectory(directory):

  root = os.getcwd()
  targetDir = os.path.join(root,directory)
  
  if not os.path.exists(targetDir):
    generateDirHashes(directory)

  with open(".vigia.json") as f:
    oldHashDict = json.load(f)

    hasher = hashlib.sha256()

    root = os.getcwd()
    #print(root)
    targetDir = os.path.join(root,directory)
    #print(targetDir)

    hashDict = dict()

    for path,subdirs,files in os.walk(targetDir):
      for name in files:
        filename = os.path.join(path,name)
        #print(filename)
        if not os.path.isdir(os.path.join(path,name)):
          f = open(filename,'rb')
          while True:
            data = f.read(1024)
            if not data:
              pathName = os.path.join(path,name)
              hashDict[pathName] = hasher.hexdigest()

              if pathName in oldHashDict:
                if hashDict[pathName] != oldHashDict[pathName]:
                  print('[M]', hashDict[pathName])
              else:
                print('[W]', hashDict[pathName])

              break
            hasher.update(data)
    for filename in oldHashDict.keys():
      if filename not in hashDict.keys():
        print("[D]", filename)

  writeToFile(hashDict)

def deleteRecords(directory):

  root = os.getcwd()
  targetDir = os.path.join(root,directory)
  os.remove(".vigia.json")
  print("Deleted directory tracking info")

if  __name__ == "__main__":
  parser = argparse.ArgumentParser()
  metodo = parser.add_mutually_exclusive_group(required= True)
  metodo.add_argument("--hash",action="store_true")
  metodo.add_argument("--hmac",dest="hmac")
  opcao = parser.add_mutually_exclusive_group(required= True)
  opcao.add_argument('-i',action="store_true", help = "running mode") 
  opcao.add_argument('-t',action="store_true", help = "running mode") 
  opcao.add_argument('-x',action="store_true", help = "running mode") 
  parser.add_argument('pasta')
  parser.add_argument('saida')
  args = parser.parse_args()

  if(args.i == True):
    generateDirHashes(args.directory)
  if (args.t == True):
    trackDirectory(args.directory)
  if (args.x == True):
    deleteRecords(args.directory)

