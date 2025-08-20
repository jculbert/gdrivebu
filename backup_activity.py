#!/usr/bin/python3
import os, subprocess

current_dir = os.getcwd()
cur_dir_name = os.path.basename(current_dir)

tarfn = "activity_" + str(cur_dir_name) + ".tz"
enc_tarfn = tarfn + ".aes"
cmd = "tar cvzf " + tarfn +  " *"
subprocess.run(cmd, shell=True)
subprocess.call(["encrypt_aes.sh", tarfn])
subprocess.call(["gdrivebu_upload_file.py", enc_tarfn, "activity"])
subprocess.call(["rm", tarfn])

cmd = 'find . -maxdepth 1 -type f -not -name "*.aes" -delete'
subprocess.run(cmd, shell=True)
