import tarfile
import sqlite3
import hashlib
import pgpy
import tibis.lib.logger as log
import tibis.lib.static as static
import tibis.lib.config as config

from pathlib import Path
import os 
import sys
import threading
import time

from halo import Halo

def existsInDB(name):
	rows=True
	try:
		db=static.tibis_db_location
		conn=sqlite3.connect(db)
		cursor_obj = conn.cursor()
		cursor_obj.execute("SELECT name FROM tibis WHERE name=?", [name])

		rows = cursor_obj.fetchall()
	except Exception as e:
		raise e
	finally:
		conn.close()
		if(rows):
			return True
		else:
			return False

def getPrivateKey(name):
	rows=True
	try:
		db=static.tibis_db_location
		conn=sqlite3.connect(db)
		cursor_obj = conn.cursor()
		cursor_obj.execute("SELECT private_key_path as private FROM tibis WHERE name=?", [name])
		rows = cursor_obj.fetchone()	
	except Exception as e:
		raise e
	finally:
		conn.close()
		private_key_path=rows[0]
		if(Path(private_key_path).is_file()):
			return private_key_path
		else:
			return False

def getPublicKey(name):
	rows=True
	try:
		db=static.tibis_db_location
		conn=sqlite3.connect(db)
		cursor_obj = conn.cursor()
		cursor_obj.execute("SELECT public_key_path as public FROM tibis WHERE name=?", [name])
		rows = cursor_obj.fetchone()	
	except Exception as e:
		raise e
	finally:
		conn.close()
		public_key_path=rows[0]
		if(Path(public_key_path).is_file()):
			return public_key_path
		else:
			return False

def getMountPoint(name):
	rows=True
	try:
		db=static.tibis_db_location
		conn=sqlite3.connect(db)
		cursor_obj = conn.cursor()
		cursor_obj.execute("SELECT mount_point as mp FROM tibis WHERE name=?", [name])
		rows = cursor_obj.fetchone()	
	except Exception as e:
		raise e
	finally:
		conn.close()
		mp=rows[0]
		if(Path(mp).is_dir()):
			return mp
		else:
			return False

def updateMountPoint(name,mountPoint):
	allGood=False
	if(existsInDB(name)):
		try:
			db=static.tibis_db_location
			conn=sqlite3.connect(db)
			cursor_obj=conn.cursor()
			cursor_obj.execute("UPDATE tibis SET mount_point=? WHERE name=?",[mountPoint,name])
			conn.commit()
			allGood=True
		except Exception as e:
			raise e 
		finally:
			conn.close()
			return allGood

def isUnlocked(name):
	rows=True
	try:
		db=static.tibis_db_location
		conn=sqlite3.connect(db)
		cursor_obj = conn.cursor()
		cursor_obj.execute("SELECT status as status FROM tibis WHERE name=?", [name])
		rows = cursor_obj.fetchone()	
	except Exception as e:
		raise e
	finally:
		conn.close()
		status=rows[0]
		if(status=='unlocked'):
			return True
		else:
			return False

def updateStatus(name,status):
	allGood=False
	if(existsInDB(name)):
		try:
			db=static.tibis_db_location
			conn=sqlite3.connect(db)
			cursor_obj=conn.cursor()
			cursor_obj.execute("UPDATE tibis SET status=? WHERE name=?",[status,name])
			conn.commit()
			allGood=True
		except Exception as e:
			raise e 
		finally:
			conn.close()
			return allGood

def uncompressArchive(source,dest):
 with tarfile.open(source,"r:"+config.compression_method() ) as tar:
  def is_within_directory(directory, target):
      
      abs_directory = os.path.abspath(directory)
      abs_target = os.path.abspath(target)
  
      prefix = os.path.commonprefix([abs_directory, abs_target])
      
      return prefix == abs_directory
  
  def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
  
      for member in tar.getmembers():
          member_path = os.path.join(path, member.name)
          if not is_within_directory(path, member_path):
              raise Exception("Attempted Path Traversal in Tar File")
  
      tar.extractall(path, members, numeric_owner=numeric_owner) 
      
  
  safe_extract(tar, dest)

def deleteArchive(source):
	remove_dir(source)

def createArchive(dirname,source,dest):
	with tarfile.open(dest+"/"+dirname+"."+config.compression_method(),"w:"+config.compression_method()) as tar:
		for fn in os.listdir(source):
			p = os.path.join(source, fn)
			tar.add(p, arcname=fn)
		#tar.add(source,arcname=dirname)
	return dest+"/"+dirname+"."+config.compression_method()

def cryptArchive(keyPath,source,dest,dirname):
	try:
		pubkey,_ = pgpy.PGPKey.from_file(keyPath)
		# file = open(source, "rb")
		# data = file.read()
		# file.close()
		# message = pgpy.PGPMessage.new(data)
		file_message=pgpy.PGPMessage.new(source,file=True)
		encrypted_message = pubkey.encrypt(file_message)

		#Important remove the clear content
		deleteArchive(source)
		#Save data into storage
		outputfile=dest+"/"+dirname

		#bytes_data=bytes(encrypted_message)

		with open(outputfile,'wb') as destFile:
			destFile.write(bytes(encrypted_message))
		return True
	except Exception as e:
		print(e)
		return False

def remove_dir(directory):
    path=Path(directory)
    if path.is_file() or path.is_symlink():
        path.unlink()
        return
    for p in path.iterdir():
        remove_dir(p)
    path.rmdir()

def deleteSQLEntry(name):
	allGood=False
	if(existsInDB(name)):
		try:
			db=static.tibis_db_location
			conn=sqlite3.connect(db)
			cursor_obj=conn.cursor()
			cursor_obj.execute("DELETE FROM tibis WHERE name=?",[name])
			conn.commit()
			allGood=True
		except Exception as e:
			raise e 
		finally:
			conn.close()
			return allGood

def calculate_hash(file_content, algorithm="sha256"):
    hasher = hashlib.new(algorithm)
    hasher.update(file_content)
    return hasher.hexdigest()

def calculate_tar_hash(archive_path, algorithm="sha256"):
    tar = tarfile.open(archive_path, "r")
    file_hashes = {}

    for member in tar.getmembers():
        if member.isfile():
            file_content = tar.extractfile(member).read()
            file_hash = calculate_hash(file_content, algorithm)
            file_hashes[member.name] = file_hash

    tar.close()
    return file_hashes

def calculate_directory_hash(directory,algorithm="sha256"):
    file_hashes = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                content = f.read()
                #file_hash = hashlib.sha256(content).hexdigest()
                file_hash = calculate_hash(content, algorithm)
                file_hashes[file_path] = file_hash
    return file_hashes 

def checkArchiveIntegrity(archive_path):
	value = calculate_tar_hash(archive_path)
	return value

def checkIntegrityIsOK(archiveIntegrity,directoryIntegrity,mountPoint):
	if(len(archiveIntegrity) != len(directoryIntegrity)):
		log.error("Not the same files")
		log.error("Archive Content : "+str(archiveIntegrity))
		log.error("Directory Content : "+str(directoryIntegrity))
		sys.exit("ERROR")

	_directoryIntegrity=[]
	_archiveIntegrity=[]

	if(mountPoint[::-1][0]!='/'):
		mountPoint+="/"
	#CleanDirectoryIntegrity to remove mountPointValue
	for obj in directoryIntegrity:
		_directoryIntegrity.append({obj.replace(mountPoint,""):directoryIntegrity[obj]})
	for obj in archiveIntegrity:
		_archiveIntegrity.append({obj:archiveIntegrity[obj]})
	
	# Convert data1 and data2 to sets of frozensets
	set1 = {frozenset(item.items()) for item in _archiveIntegrity}
	set2 = {frozenset(item.items()) for item in _directoryIntegrity}

	if(set1!=set2 or set2!=set1):
		log.error("Integrity error")
		log.error("Archive Content : "+archiveIntegrity)
		log.error("Directory Content : "+directoryIntegrity)
		sys.exit(1)
	else:
		log.success("Same integrity between archive and content")