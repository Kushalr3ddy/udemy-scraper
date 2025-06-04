import pandas as pd
import os
from glob import glob
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv


RAW_FOLDER = "raw_layer"
CLEANED_FOLDER = "bronze_layer"



dbname=os.environ["DB_NAME"]
user=os.environ["DB_USER"]
password=os.environ["DB_PASSWORD"]
host=os.environ["DB_HOST"]
port=5432


TABLE_NAME = "BRONZE_LAYER"

uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
conn = create_engine(uri).connect()

columns={
    "source_link":"TEXT",
    "course_titles":"TEXT",
    "coupon_links":"TEXT",
    "coupon_url":"TEXT",
    "scraped_at":"TIMESTAMP"
    }



def create_table(cursor):
    col_list = [f"{col_name} {dtype}" for col_name,dtype in columns.items()]

    create_query  = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({','.join(col_list)});

    """
    cursor.execute(create_query)
    return f"executed {create_query}"


def clean_bronze_csv(csv_path):
    df = pd.read_csv(csv_path,index_col=0)

    # 
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

    #  Drop empty rows
    df.dropna(how="all", inplace=True)

    # Remove exact duplicate rows
    df.drop_duplicates(inplace=True)
    
    #drop the first column
    df = df.iloc[:, 1:]
    
    # Save cleaned file
    filename = os.path.basename(csv_path)
    output_path = os.path.join(CLEANED_FOLDER, filename)
    
    
    df.to_sql(TABLE_NAME, conn, if_exists='append',index=False)
    
    df.to_csv(output_path, index=False)
    print(f"Cleaned and saved: {output_path}")

def clean_all_raw_files():
    csv_files = glob(os.path.join(RAW_FOLDER, "*.csv"))
    for csv_file in csv_files:
        clean_bronze_csv(csv_file)

if __name__ == "__main__":
    os.makedirs(CLEANED_FOLDER, exist_ok=True)
    clean_all_raw_files()
    conn.close()
