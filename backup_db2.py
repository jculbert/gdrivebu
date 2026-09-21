#!/usr/bin/env python3

import hashlib
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configuration
DUMP_PATH = '/home/jeff/Backups/db_' + datetime.today().strftime('%Y-%m-%d') + '.dmp'
DUMP_FILE = Path(DUMP_PATH)
HASH_FILE = Path("/home/jeff/Backups/database.sha256")

TOKEN_PATH = '/tmp/token.pickle'
ENCRYPTION_KEY_PATH = '/tmp/encp.txt'
UPLOAD_SECRET_PATH = '/tmp/google_drive_api_client_secret.json'

def calculate_sha256(filename):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def check_file_path(file_path):
    """Verify that a file exists and update its timestamp."""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"File does not exist: {file_path}", file=sys.stderr)
        sys.exit(1)

    subprocess.run(["touch", str(file_path)], check=True)


def main():
    print("Refreshing tmp files...")
    check_file_path(TOKEN_PATH)
    check_file_path(ENCRYPTION_KEY_PATH)
    check_file_path(UPLOAD_SECRET_PATH)

    print("Dumping database...")

    command = [
        "mariadb-dump",
        "-u",
        "root",
        "--skip-comments",
        "--skip-dump-date",
        "--all-databases"
    ]

    try:
        with open(DUMP_FILE, "wb") as dump:
            subprocess.run(
                command,
                stdout=dump,
                stderr=subprocess.PIPE,
                check=True
            )

    except subprocess.CalledProcessError as e:
        print("Database dump failed:", file=sys.stderr)
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)

    check_file_path(DUMP_FILE)

    print(f"Calculating SHA-256 of {DUMP_FILE}...")

    new_hash = calculate_sha256(DUMP_FILE)

    print(f"New SHA-256: {new_hash}")

    # Read the hash from the previous run, if it exists
    if HASH_FILE.exists():
        old_hash = HASH_FILE.read_text().strip()
        print(f"Old SHA-256: {old_hash}")
    else:
        old_hash = None
        print("No previous SHA-256 found.")

    if new_hash != old_hash:
        print("Database has changed.")

        # Save the new hash
        HASH_FILE.parent.mkdir(parents=True, exist_ok=True)
        HASH_FILE.write_text(new_hash + "\n")

        try:
            subprocess.call(["encrypt_aes.sh", DUMP_PATH])
            aespath = DUMP_PATH + ".aes"
            subprocess.call(["gdrivebu_upload_file.sh", aespath, "database"])

        except subprocess.CalledProcessError as e:
            print(
                f"Script failed with exit code {e.returncode}",
                file=sys.stderr
            )
            sys.exit(1)

    else:
        print("Database has not changed. Nothing to do.")

    subprocess.call(["rm", DUMP_PATH])

if __name__ == "__main__":
    main()
