#!/usr/bin/env python3

import hashlib
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configuration
DUMP_PATH = '/tmp/db_' + datetime.today().strftime('%Y-%m-%d') + '.dmp'
DUMP_FILE = Path(DUMP_PATH)
HASH_FILE = Path("/var/lib/investman/database.sha256")
SCRIPT_TO_RUN = Path("/usr/local/bin/do_something.py")


def calculate_sha256(filename):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def main():
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

        print(f"Running {SCRIPT_TO_RUN}...")

        try:
            tarfn = DUMP_PATH + '.tz'
            subprocess.call(["tar", "czf", tarfn, DUMP_PATH])
            subprocess.call(["encrypt_aes.sh", tarfn])
            subprocess.call(["rm", tarfn])
            subprocess.call(["rm", DUMP_PATH])

            pass

        except subprocess.CalledProcessError as e:
            print(
                f"Script failed with exit code {e.returncode}",
                file=sys.stderr
            )
            sys.exit(1)

    else:
        print("Database has not changed. Nothing to do.")


if __name__ == "__main__":
    main()
