import pandas as pd
import os

# === CONFIG ===
FOLDER = r"C:\Users\ASUS\Downloads\Yeni Klasör"
OUTPUT_FILE = os.path.join(FOLDER, "data_dictionary.xlsx")

print("📘 Data Dictionary oluşturuluyor...\n")

# Tablolar
csv_files = {
    "lead_log": "lead_log.csv",
    "user_referrals": "user_referrals.csv",
    "user_referral_logs": "user_referral_logs.csv",
    "user_logs": "user_logs.csv",
    "user_referral_statuses": "user_referral_statuses.csv",
    "referral_rewards": "referral_rewards.csv",
    "paid_transactions": "paid_transactions.csv"
}

# Otomatik açıklama üretici
def generate_description(col):
    col_lower = col.lower()
    if "id" in col_lower:
        return "Unique identifier"
    if "date" in col_lower or "at" in col_lower:
        return "Timestamp value"
    if "phone" in col_lower:
        return "Phone number"
    if "name" in col_lower:
        return "User or referral name"
    if "status" in col_lower:
        return "Status information"
    if "reward" in col_lower:
        return "Reward-related value"
    if "location" in col_lower or "timezone" in col_lower:
        return "Geographical or timezone info"
    return "General field"

# Excel writer
writer = pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl")

# Her CSV için Data Dictionary sheet oluştur
for table_name, filename in csv_files.items():
    file_path = os.path.join(FOLDER, filename)

    if not os.path.exists(file_path):
        print(f"⚠️ Bulunamadı: {filename}")
        continue

    print(f"✔ Okunuyor: {filename}")

    df = pd.read_csv(file_path)

    rows = []
    for col in df.columns:
        rows.append({
            "Table Name": table_name,
            "Column Name": col,
            "Data Type": str(df[col].dtype),
            "Description": generate_description(col)
        })

    out_df = pd.DataFrame(rows)
    out_df.to_excel(writer, sheet_name=table_name, index=False)

writer.close()

print(f"\n🎉 Data Dictionary başarıyla oluşturuldu:\n{OUTPUT_FILE}")
