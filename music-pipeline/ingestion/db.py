import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
DB_URL = os.getenv("DB_URL")

def get_engine():
    return create_engine(DB_URL)

def save_to_db(df: pd.DataFrame):
    engine = get_engine()
    df.to_sql('top_tracks', con=engine, if_exists='append', index=False)
