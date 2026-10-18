"""Offline demo backup. Stop the server before running. Copies SQLite and uploaded files."""
from pathlib import Path
import sqlite3, shutil, datetime
root=Path(__file__).parent
data=root/'data'
dest=root/'backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
dest.mkdir(parents=True,exist_ok=True)
with sqlite3.connect(data/'legalchain.sqlite') as source,sqlite3.connect(dest/'legalchain.sqlite') as target:
 source.backup(target)
if (data/'files').exists():shutil.copytree(data/'files',dest/'files')
print('Backup saved:',dest)
