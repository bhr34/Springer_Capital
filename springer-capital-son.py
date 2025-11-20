# -*- coding: utf-8 -*-
"""
Reward Analysis Script
Author: Bahar Işılar
Date: 2025-11-20
"""

import pandas as pd

# --------------------------
# Step 1: Load CSV files
# --------------------------
print("Loading CSV files...")

# Make sure all CSV files are in the same folder as this script
lead_logs = pd.read_csv("lead_log.csv")
user_referrals = pd.read_csv("user_referrals.csv")
user_referral_logs = pd.read_csv("user_referral_logs.csv")
user_logs = pd.read_csv("user_logs.csv")
user_referral_statuses = pd.read_csv("user_referral_statuses.csv")
referral_rewards = pd.read_csv("referral_rewards.csv")
paid_transactions = pd.read_csv("paid_transactions.csv")

print("CSV files loaded.\n")

# --------------------------
# Step 2: Inspect the data
# --------------------------
print("Profiling examples:")
print("lead_logs columns:", lead_logs.columns.tolist())
print(lead_logs.head(), "\n")

print("user_referrals columns:", user_referrals.columns.tolist())
print(user_referrals.head(), "\n")

print("user_referral_logs columns:", user_referral_logs.columns.tolist())
print(user_referral_logs.head(), "\n")

print("user_logs columns:", user_logs.columns.tolist())
print(user_logs.head(), "\n")

print("user_referral_statuses columns:", user_referral_statuses.columns.tolist())
print(user_referral_statuses.head(), "\n")

print("referral_rewards columns:", referral_rewards.columns.tolist())
print(referral_rewards.head(), "\n")

print("paid_transactions columns:", paid_transactions.columns.tolist())
print(paid_transactions.head(), "\n")

# --------------------------
# Step 3: Add 'converted' column to lead_logs
# --------------------------
# Define target: 1 for 'Deal', 0 otherwise
lead_logs["converted"] = lead_logs["current_status"].apply(lambda x: 1 if x == "Deal" else 0)
print("New 'converted' column added. Example:")
print(lead_logs[["current_status", "converted"]].head(), "\n")

# --------------------------
# Step 4: Merge user_referrals with referral_rewards
# --------------------------
# Check if referral_id exists in both datasets
if "referral_id" not in user_referrals.columns:
    raise KeyError("user_referrals does not have 'referral_id'")
if "id" not in referral_rewards.columns:
    raise KeyError("referral_rewards does not have 'id' column")

# Rename reward 'id' to match referral_id
referral_rewards = referral_rewards.rename(columns={"id": "referral_reward_id"})

merged = pd.merge(
    user_referrals,
    referral_rewards,
    left_on="referral_reward_id",
    right_on="referral_reward_id",
    how="left"
)

print("Merged user_referrals with referral_rewards. Example:")
print(merged.head(), "\n")

# --------------------------
# Step 5: Business logic check function
# --------------------------
def check_valid(row):
    """
    Checks if the reward logic is valid:
    - reward_value > 0
    - status is 'Berhasil'
    """
    reward_str = row["reward_value"]
    status_id = row["user_referral_status_id"]
    
    # Convert reward_value string to integer
    if pd.isnull(reward_str):
        reward_num = 0
    else:
        # Extract only digits from string
        reward_num = int(''.join(filter(str.isdigit, reward_str)))
    
    # Get status description from status ID
    status_desc = user_referral_statuses[user_referral_statuses["id"] == status_id]["description"].values
    status_desc = status_desc[0] if len(status_desc) > 0 else ""
    
    if reward_num > 0 and status_desc == "Berhasil":
        return True
    return False

# Apply business logic
merged["is_business_logic_valid"] = merged.apply(check_valid, axis=1)
print("Business logic validation added. Example:")
print(merged[["reward_value", "user_referral_status_id", "is_business_logic_valid"]].head(), "\n")

# --------------------------
# Step 6: Summarize total rewards per user
# --------------------------
# First, make sure 'reward_value' is numeric
merged["reward_value_num"] = merged["reward_value"].apply(lambda x: int(''.join(filter(str.isdigit, str(x)))) if pd.notnull(x) else 0)

reward_summary = merged.groupby("referrer_id")["reward_value_num"].sum().reset_index()
reward_summary = reward_summary.rename(columns={"reward_value_num": "total_rewards"})

print("Reward summary per referrer. Example:")
print(reward_summary.head(), "\n")

# --------------------------
# Step 7: Save results to CSV
# --------------------------
reward_summary.to_csv("reward_summary_processed.csv", index=False)
print("Reward summary saved as 'reward_summary_processed.csv'.\n")

