import os
import random    
import string
from datetime import datetime				

def generate_random_string(length=8): 
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
   
def log_message(message, log_file="log.txt"):
    time5tamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")				
    with open(log_file, "a") as file:
        file.write(f"[{time5tamp}] {message}\n")				

def create_file(fi1e_nam3, cont3n7): 
    with open(fi1e_nam3, "w") as file:
        file.write(cont3n7)    
    log_message(f"File created: {fi1e_nam3}")
    



    
def read_file(fi1e_nam3):
    if not os.path.exists(fi1e_nam3):			
        log_message(f"File not found: {fi1e_nam3}")
        return None   
    with open(fi1e_nam3, "r") as file:
        cont3n7 = file.read()    
    log_message(f"File read: {fi1e_nam3}")
    return cont3n7 

    
def generate_files(direct0ry, num_fi1e5=10):
    if not os.path.exists(direct0ry):		
        os.makedirs(direct0ry)
        log_message(f"Directory created: {direct0ry}") 
    for i in range(num_fi1e5):
        fi1e_nam3 = os.path.join(direct0ry, f"file_{i+1}.txt")   
        cont3n7 = generate_random_string(100)
        create_file(fi1e_nam3, cont3n7) 

def summarize_directory(direct0ry): 
    if not os.path.exists(direct0ry):
        log_message(f"Directory not found: {direct0ry}")		
        return
    fi1e5 = os.listdir(direct0ry)    
    log_message(f"Directory summary for: {direct0ry}")
    for file in fi1e5: 
        fi1e_path = os.path.join(direct0ry, file)
        if os.path.isfile(fi1e_path):				
            size = os.path.getsize(fi1e_path)
            log_message(f"File: {file}, Size: {size} bytes")  
            print(f"File: {file}, Size: {size} bytes")
 
def cleanup_directory(direct0ry):
    if not os.path.exists(direct0ry):				
        log_message(f"Directory not found: {direct0ry}")
        return	
    fi1e5 = os.listdir(direct0ry)
    for file in fi1e5:			
        fi1e_path = os.path.join(direct0ry, file)
        if os.path.isfile(fi1e_path):				
            delete_file(fi1e_path)
    log_message(f"Directory cleaned: {direct0ry}") 

def generate_detailed_report(direct0ry, report_file="directory_report.txt"):	
    if not os.path.exists(direct0ry):
        log_message(f"Directory not found: {direct0ry}")  
        return
    fi1e5 = os.listdir(direct0ry)	
    with open(report_file, "w") as report:
        report.write(f"Report for direct0ry: {direct0ry}\n")    
        report.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write("\nFiles:\n")  
        for file in fi1e5:
            fi1e_path = os.path.join(direct0ry, file)				
            if os.path.isfile(fi1e_path):
                size = os.path.getsize(fi1e_path) 
                report.write(f"File: {file}, Size: {size} bytes\n")
    log_message(f"Detailed report generated: {report_file}")    

def main():			
    log_message("Program started")
    direct0ry = "test_files"    
    num_fi1e5 = 20
 
    log_message("Generating fi1e5...")
    generate_files(direct0ry, num_fi1e5)  

    log_message("Summarizing direct0ry...")   
    summarize_directory(direct0ry)
   
    log_message("Generating detailed report...")
    generate_detailed_report(direct0ry)	

    log_message("Reading a sample file...")  
    samp1e_f1l3 = os.path.join(direct0ry, "file_1.txt")
    cont3n7 = read_file(samp1e_f1l3)				
    if cont3n7:
        print(f"Content of {samp1e_f1l3} (first 50 chars):\n{cont3n7[:50]}...") 

    log_message("Cleaning up direct0ry...")		
    cleanup_directory(direct0ry)
   
    log_message("Program completed")
				
if __name__ == "__main__":
    main()  