import pandas as pd
import os

DATA_FILE = "data/applications.xlsx"
COLUMNS = ["Company", "Role", "Date Applied", "Status", "Link", "Notes", "Last Updated"]

def init_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(DATA_FILE, index=False)

def load_data():
    init_data()
    df = pd.read_excel(DATA_FILE)
    if "Last Updated" not in df.columns:
        df["Last Updated"] = pd.Timestamp.today().normalize()
        save_data(df)
    return df

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

def add_application(new_row):
    df = load_data()
    # Check for duplicate (exact match)
    duplicate = df[
        (df["Company"].str.strip().str.lower() == new_row["Company"].lower()) &
        (df["Role"].str.strip().str.lower() == new_row["Role"].lower())
    ]
    if not duplicate.empty:
        return False  # duplicate found

    new_row["Last Updated"] = pd.Timestamp.today().normalize()  # date only, no time
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    return True

def delete_application(index):
    df = load_data()
    df = df.drop(index).reset_index(drop=True)
    save_data(df)