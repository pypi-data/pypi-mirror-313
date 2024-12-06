from pathlib import Path

version  = '1.1.4'
codename = "Ibis is born"

tibis_config_file="config.yml"
tibis_config_location=str(Path.home())+"/.config/tibis/"
tibis_full_config_location=tibis_config_location+tibis_config_file

tibis_keys_location=tibis_config_location+"keys"


tibis_dbfile="database.db"
tibis_db_location=tibis_config_location+"/"+tibis_dbfile
tibis_database_init=""" CREATE TABLE IF NOT EXISTS tibis (
            name VARCHAR(255) NOT NULL,
            private_key_path VARCHAR(255) NOT NULL,
            public_key_path VARCHAR(255) NOT NULL,
            status VARCHAR(10) NOT NULL,
            mount_point VARCHAR(255) NOT NULL
        ); """

tibis_database_insert=""" INSERT INTO tibis(name,private_key_path,public_key_path,status,mount_point) VALUES(?,?,?,?,?) """
tibis_database_list_all="""SELECT name,private_key_path,public_key_path,status,mount_point FROM tibis"""

tibis_empty_dir="/tmp/tempate_tibis_empty_dir"
tibis_storage_path="/tmp/storage"
tibis_tmp_dir="/tmp/tibis_tmp"

default_config={'storage_path':tibis_storage_path,'keys_location':tibis_keys_location,'pgp_infos':{'email':'tibis@localhost.org','comment':'Tibis Key','name':'Tibis'},'check_integrity':True,'encrypting':False}

