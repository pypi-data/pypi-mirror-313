import sqlite3
import tibis.lib.logger as log
import tibis.lib.static as static

def list():
 try:
  db=static.tibis_db_location
  conn=sqlite3.connect(db)
  cursor_obj = conn.cursor()
  sql = static.tibis_database_list_all
  cursor_obj.execute(sql)
  rows = cursor_obj.fetchall()
  for row in rows:
    name=row[0]
    status=row[3]
    mount_point=row[4]
    if(status=='unlocked'):
      log.unlocked(name + " " +mount_point)
    else:
      log.locked(name)
 except Exception as e:
  log.error(e)
 finally:
  conn.close()

if __name__ == '__main__':
  list()