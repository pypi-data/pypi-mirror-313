import sys
import pgpy
import yaml
import getpass
import sqlite3
import tibis.lib.logger as log
import tibis.lib.static as static
import tibis.lib.config as config
import tibis.lib.common as common
from pathlib import Path
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

def create(dirname):
 if(not common.existsInDB(dirname)):
  log.ask("Enter passphrase :")
  p = getpass.getpass("")
  log.ask("Do it again :")
  c = getpass.getpass("")
  if(not p==c):
   log.error("Passphrases are not the same")
   sys.exit(2)
  privateKeyLocation,publicKeyLocation=keys_operations(dirname,p)
  updateDb(dirname,privateKeyLocation,publicKeyLocation)

  #Create empty dir for convenance
  path=Path(static.tibis_empty_dir)
  path.mkdir(parents=True,exist_ok=True)
  path=Path(static.tibis_tmp_dir)
  path.mkdir(parents=True,exist_ok=True)
  
  archive=common.createArchive(dirname,static.tibis_empty_dir,static.tibis_tmp_dir)
  common.cryptArchive(publicKeyLocation,archive,config.storage_path(),dirname)

 else:
   log.error("Name already Exists")
   log.error("Maybe consider removing it : tibis delete "+str(dirname))

def keys_operations(dirname,passphrase):
 key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
 uid = pgpy.PGPUID.new(config.pgp_infos()['name'], comment=config.pgp_infos()['comment'], email=config.pgp_infos()['email'])
 key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
            ciphers=[SymmetricKeyAlgorithm.AES256],
            compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed])
 key.protect(passphrase, SymmetricKeyAlgorithm.AES256, HashAlgorithm.SHA256)
 privateKey = str(key)
 publicKey = str(key.pubkey)

 path=Path(static.tibis_keys_location+"/"+dirname)
 path.mkdir(exist_ok=True)

 privateKeyLocation=static.tibis_keys_location+"/"+dirname+"/private"
 publicKeyLocation=static.tibis_keys_location+"/"+dirname+"/public"

 if(path.is_dir()):
  with open(privateKeyLocation,'w') as private:
    private.write(privateKey)
  with open(publicKeyLocation,'w') as public:
    public.write(publicKey)
 log.success("Keys created")

 dataLocation=config.storage_path()
 return privateKeyLocation,publicKeyLocation
 

def updateDb(dirName,privateKeyLocation,publicKeyLocation):
 try:
  db=static.tibis_db_location
  conn=sqlite3.connect(db)
  cursor_obj = conn.cursor()
  sql = static.tibis_database_insert
  cursor_obj.execute(sql,(dirName,privateKeyLocation,publicKeyLocation,"locked",""))
  conn.commit()
  log.success("Database updated")
 except Exception as e:
 	log.error(e)
 finally:
 	conn.close()

if __name__ == '__main__':
    create(dirname)
