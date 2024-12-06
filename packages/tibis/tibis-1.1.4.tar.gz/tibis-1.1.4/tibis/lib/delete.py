import sqlite3
import tibis.lib.logger as log
import tibis.lib.static as static
import tibis.lib.common as common 

import simple_chalk as chalk

def delete(dirname):
 if(not common.existsInDB(dirname)):
  log.error("Entry does not exist")
 else:
   answer = ""
   while answer not in ["y", "n"]:
    answer = input(chalk.red.bold("OK to push to continue [Y/N]? ")).lower()
   if(answer=="y"):
    #On vire la data  du storage
    if(common.isUnlocked(dirname)):
      mp=common.getMountPoint(dirname)
      log.warning("Your content was previously unlocked at "+ str(mp) +" you have to delete it by yourself")
    try:
      common.remove_dir(static.tibis_keys_location+"/"+dirname)
      common.deleteSQLEntry(dirname)
    except:
     log.warning("Keys are already gone")
     log.warning("Entry and keys removed")
   else:
    log.success("Leaves the things as it ...")     

if __name__ == '__main__':
  deleteSQLEntry(dirname)