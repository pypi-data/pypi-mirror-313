import yaml 
import simple_chalk as chalk
import tibis.lib.logger as log
import tibis.lib.static as static

from pathlib import Path


def firstTime():
 log.info("Create config file")
 path=Path(static.tibis_config_location)
 path.mkdir(parents=True,exist_ok=True)
 log.success("Done")

 log.info("Create key directory")
 path=Path(static.tibis_keys_location)
 path.mkdir(parents=True,exist_ok=True)
 log.success("Done")

 log.ask("Storage directory :")
 storage_path=input("Full path : ")
 path=Path(storage_path)
 path.mkdir(parents=True,exist_ok=True)
 log.success("Done")

 log.info("Required informations for PGP Keys")
 name = input(chalk.yellow.bold("Name :"))
 comment = input(chalk.yellow.bold("Comment :"))
 email =  input(chalk.yellow.bold("Email :"))

 if name == "":
  name="Tibis"
 if comment =="":
  comment="Tibis Key"
 if email == "":
  email="tibis@localhost.org"

 default_config=static.default_config
 default_config['pgp_infos']['name']=name
 default_config['pgp_infos']['email']=email
 default_config['pgp_infos']['comment']=comment
 default_config['storage_path']=storage_path
 default_config['compression_method']='gz'
 default_config['encrypting']=False

 with open(static.tibis_full_config_location,'w') as file:
  yaml.dump(default_config,file)
  log.success("Ready to go !")

if __name__ == '__main__':
    firstTime()