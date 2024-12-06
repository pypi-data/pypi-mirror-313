from pathlib import Path
from halo import Halo
from os import rmdir
import tibis.lib.logger as log
import tibis.lib.common as common
import tibis.lib.config as config
import tibis.lib.static as static

def lock(dirname):
	if(config.isEncrypting()):
		log.error("Wait for previous operation to end")
	else:
		if(not common.existsInDB(dirname)):
			log.error("Directory not in database")
			return False
		if(not common.isUnlocked(dirname)):
			log.error("Directory is already locked")
			return False
		else:
			#Get Keys
			publicKeyLocation=common.getPublicKey(dirname)
			mountPoint=common.getMountPoint(dirname)
			if(not Path(static.tibis_tmp_dir).exists()):
				path = Path(static.tibis_tmp_dir)
				path.mkdir(parents=True,exist_ok=True)
			if(publicKeyLocation):
				#Create archive
				config.defineEncryptingStatus(True)
				#Empty the tmpdir
				[f.unlink() for f in Path(static.tibis_tmp_dir).glob("*") if f.is_file()]
				#Create the archive
				spinner = Halo(text='Creating archive ',spinner='moon')
				spinner.start()
				archivePath=common.createArchive(dirname,mountPoint,static.tibis_tmp_dir)
				spinner.succeed('Archive created')
				if(config.check_integrity_status()):
					spinner = Halo(text='Checking directory integrity ',spinner='moon')
					spinner.start()
					directoryIntegrity=common.calculate_directory_hash(mountPoint)
					spinner.succeed('Directory integrity obtained')
					spinner = Halo(text='Checking archive integrity ',spinner='moon')
					spinner.start()
					archiveIntegrity=common.checkArchiveIntegrity(str(archivePath))
					spinner.succeed('Archive integrity obtained')
					common.checkIntegrityIsOK(archiveIntegrity,directoryIntegrity,mountPoint)

				spinner = Halo(text='Encrypting and moving',spinner='moon')
				spinner.start()
				isCrypted=common.cryptArchive(publicKeyLocation,archivePath,config.storage_path(),dirname)
				spinner.succeed('Archive encrypted')
				#Need To check the previous return status
				if(isCrypted):
					spinner = Halo(text='Removing files ',spinner='moon')
					spinner.start()
					[f.unlink() for f in Path(static.tibis_tmp_dir).glob("*") if f.is_file()]
					common.remove_dir(mountPoint)
					common.updateStatus(dirname,'locked')
					common.updateMountPoint(dirname,'')
					spinner.succeed('Files removed')
					log.success(dirname+" is locked")
					config.defineEncryptingStatus(False)
				else:
					log.error("Something went wrong ...")
 
if __name__ == '__main__':
    lock(dirname)
