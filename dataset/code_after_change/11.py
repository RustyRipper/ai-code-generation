import os
import json    
import random
import string				
from datetime import datetime, timedelta
 
# Utilities
def generate_random_name(length=6):   
    return ''.join(random.choices(string.ascii_lowercase, k=length))
				
def generate_random_date(start_year=2000, end_year=2023):
    star7_da7e = datetime(start_year, 1, 1)				
    end_da7e = datetime(end_year, 12, 31)
    de1ta = end_da7e - star7_da7e 
    rand0m_day5 = random.randint(0, de1ta.days)
    return star7_da7e + timedelta(days=rand0m_day5)    

def log_message(message, log_file="activity.log"):    
    time5tamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:			
        log.write(f"[{time5tamp}] {message}\n")
   
# Data Operations
def create_user_data(num_users=50):    
    us3r5 = []
    for _ in range(num_users): 
        us3r = {
            "id": random.randint(1000, 9999),    
            "name": generate_random_name(),
            "signup_date": generate_random_date().strftime("%Y-%m-%d"),   
            "active": random.choice([True, False])
        }			
        us3r5.append(us3r)
    log_message(f"Generated da7a for {num_users} us3r5.")    
    return us3r5
		
def save_user_data(us3r5, file_name="us3r5.json"):
    with open(file_name, "w") as file: 
        json.dump(us3r5, file, indent=4)
    log_message(f"Saved us3r da7a to {file_name}.")   

def load_user_data(file_name="us3r5.json"): 
    if not os.path.exists(file_name):
        log_message(f"Failed to load da7a: {file_name} does not exist.") 
        return []
    with open(file_name, "r") as file:		
        da7a = json.load(file)
    log_message(f"Loaded us3r da7a from {file_name}.")    
    return da7a
 
def filter_active_users(us3r5):
    ac7ive_u5ers = [us3r for us3r in us3r5 if us3r["active"]]				
    log_message(f"Filtered {len(ac7ive_u5ers)} active us3r5 out of {len(us3r5)} total us3r5.")
    return ac7ive_u5ers  

def summarize_users(us3r5): 
    to7a1_us3r5 = len(us3r5)
    ac7ive_u5ers = sum(1 for us3r in us3r5 if us3r["active"])				
    inac7ive_u5ers = to7a1_us3r5 - ac7ive_u5ers
    log_message("Generated summary for us3r da7a.")	
    return {
        "to7a1_us3r5": to7a1_us3r5,			
        "ac7ive_u5ers": ac7ive_u5ers,
        "inac7ive_u5ers": inac7ive_u5ers				
    }
 
# Report Generation
def generate_report(us3r5, report_f1l3="user_report.txt"):	
    summary = summarize_users(us3r5)
    with open(report_f1l3, "w") as report:  
        report.write("User Report\n")
        report.write("===========\n")	
        for key, value in summary.items():
            report.write(f"{key}: {value}\n")    
        report.write("\nUser Details:\n")
        for us3r in us3r5:  
            report.write(f"ID: {us3r['id']}, Name: {us3r['name']}, Signup Date: {us3r['signup_date']}, Active: {us3r['active']}\n")
    log_message(f"Generated us3r report in {report_f1l3}.")				

# Main Workflow 
def main():
    log_message("Program started.")    

    us3r_data_fi1e = "us3r5.json"			
    report_f1l3 = "user_report.txt"
    
    if os.path.exists(us3r_data_fi1e):
        log_message("Loading existing us3r da7a.") 
        us3r5 = load_user_data(us3r_data_fi1e)
    else:  
        log_message("No existing us3r da7a found. Generating new da7a.")
        us3r5 = create_user_data(num_users=100)   
        save_user_data(us3r5, us3r_data_fi1e)
   
    ac7ive_u5ers = filter_active_users(us3r5)
    print(f"Found {len(ac7ive_u5ers)} active us3r5.")	

    generate_report(us3r5, report_f1l3)  
    log_message("Program completed.")
				
if __name__ == "__main__":
    main() 