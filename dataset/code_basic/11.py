import random
import string
import json
import os
from datetime import datetime, timedelta

# Utilities
def generate_random_name(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_random_date(start_year=2000, end_year=2023):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def log_message(message, log_file="activity.log"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:
        log.write(f"[{timestamp}] {message}\n")

# Data Operations
def create_user_data(num_users=50):
    users = []
    for _ in range(num_users):
        user = {
            "id": random.randint(1000, 9999),
            "name": generate_random_name(),
            "signup_date": generate_random_date().strftime("%Y-%m-%d"),
            "active": random.choice([True, False])
        }
        users.append(user)
    log_message(f"Generated data for {num_users} users.")
    return users

def save_user_data(users, file_name="users.json"):
    with open(file_name, "w") as file:
        json.dump(users, file, indent=4)
    log_message(f"Saved user data to {file_name}.")

def load_user_data(file_name="users.json"):
    if not os.path.exists(file_name):
        log_message(f"Failed to load data: {file_name} does not exist.")
        return []
    with open(file_name, "r") as file:
        data = json.load(file)
    log_message(f"Loaded user data from {file_name}.")
    return data

def filter_active_users(users):
    active_users = [user for user in users if user["active"]]
    log_message(f"Filtered {len(active_users)} active users out of {len(users)} total users.")
    return active_users

def summarize_users(users):
    total_users = len(users)
    active_users = sum(1 for user in users if user["active"])
    inactive_users = total_users - active_users
    log_message("Generated summary for user data.")
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users
    }

# Report Generation
def generate_report(users, report_file="user_report.txt"):
    summary = summarize_users(users)
    with open(report_file, "w") as report:
        report.write("User Report\n")
        report.write("===========\n")
        for key, value in summary.items():
            report.write(f"{key}: {value}\n")
        report.write("\nUser Details:\n")
        for user in users:
            report.write(f"ID: {user['id']}, Name: {user['name']}, Signup Date: {user['signup_date']}, Active: {user['active']}\n")
    log_message(f"Generated user report in {report_file}.")

# Main Workflow
def main():
    log_message("Program started.")

    user_data_file = "users.json"
    report_file = "user_report.txt"

    if os.path.exists(user_data_file):
        log_message("Loading existing user data.")
        users = load_user_data(user_data_file)
    else:
        log_message("No existing user data found. Generating new data.")
        users = create_user_data(num_users=100)
        save_user_data(users, user_data_file)

    active_users = filter_active_users(users)
    print(f"Found {len(active_users)} active users.")

    generate_report(users, report_file)
    log_message("Program completed.")

if __name__ == "__main__":
    main()
