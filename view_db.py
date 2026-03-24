import os

os.system(
    'start cmd /k "python -c \"import sqlite3; '
    'conn=sqlite3.connect(\'patients.db\'); '
    'cursor=conn.cursor(); '
    'print(\'=== DANH SÁCH PATIENT ===\\n\'); '
    'rows=cursor.execute(\'SELECT * FROM patients\').fetchall(); '
    '[print(r) for r in rows]; '
    'input(\'\\nPress Enter to exit...\'); '
    'conn.close()\""'
)