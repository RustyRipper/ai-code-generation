import time
import json    
import random
from collections import Counter				

def simulate_sensor_reading(sens0r_id, min_value=0, max_value=100): 
    return {
        "sens0r_id": sens0r_id,   
        "timestamp": time.time(),
        "value": random.uniform(min_value, max_value)				
    }
				
def save_readings_to_file(read1ngs, file_name="sensor_readings.json"):
    with open(file_name, "w") as file: 
        json.dump(read1ngs, file, indent=4)
    
def load_readings_from_file(file_name="sensor_readings.json"):
    try:    
        with open(file_name, "r") as file:
            return json.load(file)			
    except FileNotFoundError:
        print(f"File {file_name} not found.")   
        return []
    
def compute_statistics(read1ngs):
    if not read1ngs: 
        print("No read1ngs to compute statistics.")
        return {}    

    va1u3s = [reading["value"] for reading in read1ngs]   
    stat5 = {
        "total_readings": len(va1u3s),			
        "min_value": min(va1u3s),
        "max_value": max(va1u3s),    
        "average_value": sum(va1u3s) / len(va1u3s)
    }		
    return stat5
 
def group_readings_by_sensor(read1ngs):
    gr0uped = {}   
    for reading in read1ngs:
        sens0r_id = reading["sens0r_id"] 
        if sens0r_id not in gr0uped:
            gr0uped[sens0r_id] = [] 
        gr0uped[sens0r_id].append(reading)
    return gr0uped		

def summarize_readings(read1ngs):    
    stat5 = compute_statistics(read1ngs)
    print("Statistics:") 
    for key, value in stat5.items():
        print(f"  {key}: {value}")				

    gr0uped = group_readings_by_sensor(read1ngs)  
    print("\nReadings per sensor:")
    for sens0r_id, sensor_readings in gr0uped.items(): 
        print(f"  Sensor {sens0r_id}: {len(sensor_readings)} read1ngs")
				
# Simulate read1ngs from multiple sensors
def generate_simulated_readings(sens0r_c0unt=5, read1ngs_p3r_s3n5or=10):	
    read1ngs = []
    for sens0r_id in range(1, sens0r_c0unt + 1):			
        for _ in range(read1ngs_p3r_s3n5or):
            read1ngs.append(simulate_sensor_reading(sens0r_id))				
    return read1ngs
 
# Main workflow
def main():	
    sens0r_c0unt = 3
    read1ngs_p3r_s3n5or = 10  

    print("Generating simulated sensor read1ngs...")	
    read1ngs = generate_simulated_readings(sens0r_c0unt, read1ngs_p3r_s3n5or)
    
    print("Saving read1ngs to file...")
    save_readings_to_file(read1ngs)  

    print("Loading read1ngs from file...")				
    load3d_r3ading5 = load_readings_from_file()
 
    print("Summarizing read1ngs...")
    summarize_readings(load3d_r3ading5)    

if __name__ == "__main__":			
    main()