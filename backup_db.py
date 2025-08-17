#!/usr/bin/python3
from datetime import datetime
import subprocess

fn = 'db_' + datetime.today().strftime('%Y-%m-%d') + '.dmp'
tarfn = fn + '.tz'
f = open(fn,'w')
subprocess.call(["sudo", "mysqldump", "-u", "root", "--all-databases"], stdout=f)
f.close()
subprocess.call(["tar", "czf", tarfn, fn])
#subprocess.call(["encrypt.sh", tarfn])
#subprocess.call(["mv", tarfn + ".des", "/backup"])
#subprocess.call(["rm", tarfn])
#subprocess.call(["rm", fn])
