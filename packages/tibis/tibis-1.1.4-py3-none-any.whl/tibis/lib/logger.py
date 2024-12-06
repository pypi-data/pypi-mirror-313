import simple_chalk as chalk
from halo import Halo
from log_symbols import LogSymbols


def info(text):
 spinner=Halo()
 spinner.info(text)

def success(text):
 spinner=Halo()
 spinner.succeed(text)

def ask(text):
 spinner=Halo()
 spinner.warn(text)

def warning(text):
 spinner=Halo()
 spinner.warn(text)

def error(text):
 spinner=Halo()
 spinner.fail(text)

def locked(text):
 spinner=Halo()
 toPrint = "[LOCKED] : "+text
 print(chalk.green.bold(toPrint))

def unlocked(text):
 spinner=Halo()
 toPrint="[ OPEN ] : "+text
 print(chalk.red.bold(toPrint))