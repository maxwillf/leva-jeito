import sys,os
import hashlib 
import hmac
import json
import argparse

def resetHasher():
  global hasher
  if key is not None:
    hasher = hmac.HMAC(key)
  else:
    hasher = hashlib.sha256()


def writeToFile(hashDict,directory):
  dirNameHash = hashlib.sha256(directory.encode('utf-8')).hexdigest()
  folderPath = os.path.join('.vigia',intermediatePath)
  filePath = os.path.join(folderPath,dirNameHash)
  if not os.path.exists(folderPath):
    os.makedirs(folderPath)
    json.dump(hashDict,open(filePath,'w'))
  else:
    json.dump(hashDict,open(filePath,'w'))

def generateDirHashes(directory,key):
  
  root = os.getcwd()
  targetDir = os.path.join(root,directory)

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
            resetHasher()
            print('[W]',filename)
            print(hashDict[os.path.join(path,name)])
            break
          else:
            hasher.update(data)
  writeToFile(hashDict,directory)

def trackDirectory(directory,key):

  root = os.getcwd()
  targetDir = os.path.join(root,directory)
  dirNameHash = hashlib.sha256(directory.encode('utf-8')).hexdigest()
  if not os.path.exists(os.path.join('.vigia',intermediatePath,dirNameHash)):
    return generateDirHashes(directory,key)

  with open(os.path.join(".vigia",intermediatePath,dirNameHash)) as f:

    oldHashDict = json.load(f)
    root = os.getcwd()
    targetDir = os.path.join(root,directory)
    hashDict = dict()

    for path,subdirs,files in os.walk(targetDir):
      for name in files:
        filename = os.path.join(path,name)
        #print(filename)
        if not os.path.isdir(filename):
          f = open(filename,'rb')
          while True:
            data = f.read(1024)
            if not data:
              pathName = os.path.join(path,name)
              hashDict[pathName] = hasher.hexdigest()
              resetHasher()
              if pathName in oldHashDict:
                if hashDict[pathName] != oldHashDict[pathName]:
                  print('[M]', pathName)
                  print(hashDict[pathName])
              else:
                print('[W]', pathName)
                print(hashDict[pathName])
              break
            else:
              hasher.update(data)
    for filename in oldHashDict.keys():
      if filename not in hashDict.keys():
        print("[D]", filename)

  writeToFile(hashDict,directory)

def deleteRecords(directory):

  dirNameHash = hashlib.sha256(directory.encode('utf-8')).hexdigest()
  deleteDir = os.path.join('.vigia',intermediatePath,dirNameHash)
  if os.path.exists(deleteDir):
    os.remove(deleteDir)
    print("Deleted directory tracking info")
  else:
    print("Diretório à ser removido não estava sendo monitorado anteriormente")

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
  parser.add_argument('-o',dest="saida",action="store") 
  args = parser.parse_args()

  if(args.saida is not None):
    sys.stdout = open(args.saida,'w')
  
  if args.hmac is not None:
    intermediatePath = 'hmac'
    key = args.hmac.encode('utf-8')
  else:
    intermediatePath = 'hash'
    key = args.hmac
  
  if key is not None:
    hasher = hmac.HMAC(key)
  else:
    hasher = hashlib.sha256()

  if (args.i == True):
    generateDirHashes(args.pasta,key)
  if (args.t == True):
    trackDirectory(args.pasta,key)
  if (args.x == True):
    deleteRecords(args.pasta)

