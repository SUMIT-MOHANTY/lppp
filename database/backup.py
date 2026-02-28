import json
from datetime import datetime
from connection import get_engine
from sqlalchemy import text

def backup_tables(tables=None):
    engine = get_engine()
    backup = {'timestamp': datetime.now().isoformat(), 'data': {}}
    tables = tables or ['users', 'structured_data', 'api_logs']
    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f'SELECT * FROM {table}'))
            backup['data'][table] = [dict(row._mapping) for row in result]
    filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(backup, f, default=str)
    print(f"[OK] Backup saved to {filename}")
    return filename

def restore_backup(filename):
    with open(filename) as f:
        backup = json.load(f)
    engine = get_engine()
    with engine.connect() as conn:
        for table, records in backup['data'].items():
            if records:
                cols = list(records[0].keys())
                for rec in records:
                    placeholders = ', '.join([f':{c}' for c in cols])
                    conn.execute(text(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})"), rec)
                conn.commit()
    print(f"[OK] Restored from {filename}")
