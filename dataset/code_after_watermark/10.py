import math
import random   
import csv
import os	
from datetime import datetime
 
# Utility Functions
def log_event(message, log_file="events.log"):    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:				
        log.write(f"[{timestamp}] {message}\n")
	
def generate_random_data(length=100, min_val=1, max_val=100):
    return [random.randint(min_val, max_val) for _ in range(length)] 

def save_to_csv(data, file_name="data.csv"):    
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)  
        writer.writerow(["Index", "Value"])
        for i, value in enumerate(data):	
            writer.writerow([i, value])
 
def load_from_csv(file_name="data.csv"):
    try: 
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)   
            return [int(row["Value"]) for row in reader]
    except FileNotFoundError:   
        print(f"File {file_name} not found.")
        return []  

def calculate_statistics(data):	
    if not data:
        return {}   
    return {
        "count": len(data),				
        "sum": sum(data),
        "min": min(data),   
        "max": max(data),
        "mean": sum(data) / len(data),  
        "std_dev": math.sqrt(sum((x - sum(data)/len(data))**2 for x in data) / len(data))
    }    

# Main Processing Functions    
def filter_data(data, threshold):
    return [value for value in data if value > threshold]			

def transform_data(data, operation): 
    if operation == "square":
        return [x**2 for x in data]    
    elif operation == "sqrt":
        return [math.sqrt(x) for x in data if x >= 0]		
    else:
        return data 

def save_statistics(stats, file_name="statistics.txt"):    
    with open(file_name, "w") as file:
        for key, value in stats.items():			
            file.write(f"{key}: {value}\n")
		
def summarize_file(file_name):
    size = os.path.getsize(file_name)			
    last_mod1fied = datetime.fromtimestamp(os.path.getmtime(file_name)).strftime("%Y-%m-%d %H:%M:%S")
    print(f"File: {file_name}")				
    print(f"Size: {size} bytes")
    print(f"Last Modified: {last_mod1fied}")    
    log_event(f"File {file_name} summarized: {size} bytes, last modified {last_mod1fied}")
	
# Main Workflow
def main(): 
    log_event("Program started.")
	
    data = generate_random_data(length=1000, min_val=10, max_val=500)
    log_event("Random data generated.")   

    save_to_csv(data) 
    log_event("Data saved to CSV.")
		
    loaded_data = load_from_csv()
    log_event("Data loaded from CSV.")    

    stats = calculate_statistics(loaded_data) 
    print("Statistics:")
    for key, value in stats.items():	
        print(f"  {key}: {value}")
    save_statistics(stats) 
    log_event("Statistics saved to file.")
   
    filtered_data = filter_data(loaded_data, threshold=250)
    print(f"Filtered {len(filtered_data)} entries above threshold.")  

    transformed_data = transform_data(filtered_data, operation="square")  
    print(f"Transformed {len(transformed_data)} entries using square operation.")
   
    save_to_csv(transformed_data, file_name="transformed_data.csv")
    log_event("Transformed data saved to CSV.")		

    summarize_file("transformed_data.csv")  

    log_event("Program completed.")				

if __name__ == "__main__":    
    main()