import yaml
import sqlite3
import tibis.lib.args_parser as args_parser
import tibis.lib.logger as log
import tibis.lib.static as static
import tibis.lib.first_time as firstTime
from pathlib import Path

def main():
    path=Path(static.tibis_full_config_location)
    if(not path.is_file()):
        firstTime.firstTime()
    #log.info("Setup database if not exists")
    conn=None
    try:
        conn=sqlite3.connect(static.tibis_db_location)
        cursor_obj = conn.cursor()
        table = static.tibis_database_init;
        cursor_obj.execute(table)
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()


    args_parser.args_parser()

if __name__ == "__main__":
 main()
