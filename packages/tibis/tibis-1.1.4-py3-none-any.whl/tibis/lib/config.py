import yaml 
import tibis.lib.static as static
import sys

def storage_path():
    with open(static.tibis_full_config_location) as file:
        p = yaml.load(file,Loader=yaml.FullLoader)
        return p['storage_path']

def pgp_infos():
    with open(static.tibis_full_config_location) as file:
        p = yaml.load(file,Loader=yaml.FullLoader)
        return p['pgp_infos']

def check_integrity_status():
    with open(static.tibis_full_config_location) as file:
        p = yaml.load(file,Loader=yaml.FullLoader)
        if('check_integrity' in p ):
            return p['check_integrity']
        else:
            return True
def compression_method():
    with open(static.tibis_full_config_location) as file:
        p = yaml.load(file,Loader=yaml.FullLoader)
        if('compression_method' in p):
            return p['compression_method']
        else:
            return 'gz'

def isEncrypting():
    with open(static.tibis_full_config_location) as file:
        p = yaml.load(file,Loader=yaml.FullLoader)
        if('encrypting' in p):
            return p['encrypting']
        else:
            return False

def defineEncryptingStatus(status):
    with open(static.tibis_full_config_location,'r+') as file:
        p = yaml.load(file,Loader=yaml.FullLoader)
        p['encrypting']=status
        yaml.dump(p,file)