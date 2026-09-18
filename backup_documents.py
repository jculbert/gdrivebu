#!/usr/bin/env python3
import subprocess
from datetime import datetime

DOCUMENTS_DIR = "/home/jeff/Documents"
TIMESTAMP_FILE = "/home/jeff/Documents/.last_backup"
BACKUP_DIR = "/home/jeff/Backups/"

result = subprocess.run(
    ["find", DOCUMENTS_DIR, "-type", "f", "-newer", TIMESTAMP_FILE, "-print", "-quit"],
    capture_output=True,
    text=True
)

if result.stdout:
    #subprocess.run(args.command)
    print("Backing up documents...")
    subprocess.call(["touch", TIMESTAMP_FILE])
    tarfn = BACKUP_DIR + 'documents_' + datetime.today().strftime('%Y-%m-%d') + '.tz'
    subprocess.call(["tar", "czf", tarfn, DOCUMENTS_DIR])
    subprocess.call(["encrypt_aes.sh", tarfn])
    subprocess.call(["rm", tarfn])

    aesfn = tarfn + ".aes"
    subprocess.call(["gdrivebu_upload_file.sh", aesfn, "documents"])

else:
    print("No new documents to back up.")
