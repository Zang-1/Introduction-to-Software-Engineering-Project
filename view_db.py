import os

os.system(
    'start cmd /k "python -c \"import sqlite3; '
    'conn=sqlite3.connect(\'patients.db\'); '
    'cursor=conn.cursor(); '
    'print(\'=== PATIENT LIST ===\\n\'); '
    'rows=cursor.execute(\'SELECT * FROM patients\').fetchall(); '
    '[print(r) for r in rows]; '
    'input(\'\\nPress Enter to exit...\'); '
    'conn.close()\""'
)
