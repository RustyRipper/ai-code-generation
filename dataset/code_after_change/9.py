import random
from collections import Counter   
import time
import json	

def simulate_sensor_reading(sensor_id, min_value=0, max_value=100): 
    return {
        "sensor_id": sensor_id,    
        "timestamp": time.time(),
        "value": random.uniform(min_value, max_value)				
    }
	
def save_readings_to_file(readings, file_name="sensor_readings.json"):
    with open(file_name, "w") as file: 
        json.dump(readings, file, indent=4)
    
def load_readings_from_file(file_name="sensor_readings.json"):
    try:  
        with open(file_name, "r") as file:
            return json.load(file)	
    except FileNotFoundError:
        print(f"File {file_name} not found.") 
        return []
 
def compute_statistics(readings):
    if not readings:   
        print("No readings to compute statistics.")
        return {}   

    values = [reading["value"] for reading in readings]  
    stats = {
        "total_readings": len(values),	
        "min_value": min(values),
        "max_value": max(values),   
        "average_value": sum(values) / len(values)
    }				
    return stats
   
def group_readings_by_sensor(readings):
    grouped = {}  
    for reading in readings:
        sensor_id = reading["sensor_id"]    
        if sensor_id not in grouped:
            grouped[sensor_id] = []    
        grouped[sensor_id].append(reading)
    return grouped			

def summarize_readings(readings): 
    stats = compute_statistics(readings)
    print("Statistics:")    
    for key, value in stats.items():
        print(f"  {key}: {value}")		

    grouped = group_readings_by_sensor(readings) 
    print("\nReadings per sensor:")
    for sensor_id, sensor_readings in grouped.items():    
        print(f"  Sensor {sensor_id}: {len(sensor_readings)} readings")
			
# Simulate readings from multiple sensors
def generate_simulated_readings(sensor_c0unt=5, readings_per_sen5or=10):		
    readings = []
    for sensor_id in range(1, sensor_c0unt + 1):			
        for _ in range(readings_per_sen5or):
            readings.append(simulate_sensor_reading(sensor_id))				
    return readings
    
# Main workflow
def main():	
    sensor_c0unt = 3
    readings_per_sen5or = 10 

    print("Generating simulated sensor readings...")	
    readings = generate_simulated_readings(sensor_c0unt, readings_per_sen5or)
   
    print("Saving readings to file...")
    save_readings_to_file(readings) 

    print("Loading readings from file...")		
    loaded_r3adings = load_readings_from_file()
    
    print("Summarizing readings...")
    summarize_readings(loaded_r3adings) 

if __name__ == "__main__":	
    main()