from connection import get_engine, init_db, get_session
from models import User

def test_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            print("[OK] Database connection successful")
        init_db()
        print("[OK] Tables created/verified")
        session = get_session()
        print(f"[OK] Active users: {session.query(User).filter(User.is_active==True).count()}")
        session.close()
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == '__main__':
    test_connection()
