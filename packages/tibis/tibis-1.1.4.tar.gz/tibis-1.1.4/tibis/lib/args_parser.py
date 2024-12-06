import sys
import argparse
from tibis.lib.create import create
from tibis.lib.lock import lock
from tibis.lib.unlock import unlock
from tibis.lib.list import list
from tibis.lib.delete import delete
from tibis.lib.static import version,codename
import tibis.lib.logger as log

def args_parser():

	parser = argparse.ArgumentParser(description=f"""
		   _   _   _   _   _  
		  / \ / \ / \ / \ / \ 
		 ( t | i | b | i | s )
		  \_/ \_/ \_/ \_/ \_/	

	A cool tool to manage encrypted directory
    Version : {version} Codename : {codename}""",
    formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument('action',nargs=1,choices=['create','list' ,'lock', 'unlock','delete'],help="Main action to choose")
	parser.add_argument('name',nargs='?',help="directory name or path required by create, lock, unlock and delete")
	parser.add_argument('destination',nargs='?',help="directory destination required by unlock")

	try:
		args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
	except SystemExit:
		#Maybe do something here ?
		exit(-1)

	action=args.action[0]
	if(action=='list'):
		list()
		sys.exit(0)
	#Dirname is required here
	if(not args.name):
		log.error("name is required")
		sys.exit(0)
	
	dirname=args.name

	if(action=='create'):
		create(dirname)
		sys.exit(1)

	if(action=='lock'):
		lock(dirname)
		sys.exit(1)

	if(action=='delete'):
		delete(dirname)
		sys.exit(1)

	if(not args.destination):
		log.error("destination is required")
		sys.exit(0)
	destination=args.destination
	if(action=='unlock'):
		unlock(dirname,destination)
		sys.exit(1)