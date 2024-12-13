from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os


def test_connection():
    try:
        # Load environment variables from .env
        load_dotenv()

        # Fetch variables
        USER = os.getenv("user")
        PASSWORD = os.getenv("password")
        HOST = "aws-0-us-west-1.pooler.supabase.com"  # Using pooler host
        PORT = "6543"  # Using pooler port
        DBNAME = os.getenv("dbname")

        # Construct the SQLAlchemy connection string
        DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

        # Create the SQLAlchemy engine
        # Using NullPool since we're connecting to a connection pooler
        engine = create_engine(
            DATABASE_URL, poolclass=NullPool, echo=True  # Set to False in production
        )

        # Test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT NOW();")).fetchone()
            print("Connection successful!")
            print("Current Time:", result[0])
            return True

    except Exception as e:
        print(f"Failed to connect: {e}")
        return False


if __name__ == "__main__":
    test_connection()
