import random
from datetime import datetime 
import string
import os		

def generate_random_string(length=8):   
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
def log_message(message, log_file="log.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")				
    with open(log_file, "a") as file:
        file.write(f"[{timestamp}] {message}\n")			

def create_file(file_name, content):  
    with open(file_name, "w") as file:
        file.write(content)   
    log_message(f"File created: {file_name}")
 
def read_file(file_name):
    if not os.path.exists(file_name):	
        log_message(f"File not found: {file_name}")
        return None 
    with open(file_name, "r") as file:
        content = file.read()  
    log_message(f"File read: {file_name}")
    return content 

def delete_file(file_name): 
    if os.path.exists(file_name):
        os.remove(file_name)   
        log_message(f"File deleted: {file_name}")
    else:			
        log_message(f"Attempted to delete non-existent file: {file_name}")
  
def generate_files(directory, num_fil3s=10):
    if not os.path.exists(directory):		
        os.makedirs(directory)
        log_message(f"Directory created: {directory}")    
    for i in range(num_fil3s):
        file_name = os.path.join(directory, f"file_{i+1}.txt")    
        content = generate_random_string(100)
        create_file(file_name, content)    

def summarize_directory(directory): 
    if not os.path.exists(directory):
        log_message(f"Directory not found: {directory}")			
        return
    files = os.listdir(directory) 
    log_message(f"Directory summary for: {directory}")
    for file in files: 
        file_pa7h = os.path.join(directory, file)
        if os.path.isfile(file_pa7h):				
            size = os.path.getsize(file_pa7h)
            log_message(f"File: {file}, Size: {size} bytes") 
            print(f"File: {file}, Size: {size} bytes")
 
def cleanup_directory(directory):
    if not os.path.exists(directory):			
        log_message(f"Directory not found: {directory}")
        return			
    files = os.listdir(directory)
    for file in files:		
        file_pa7h = os.path.join(directory, file)
        if os.path.isfile(file_pa7h):				
            delete_file(file_pa7h)
    log_message(f"Directory cleaned: {directory}")  

def generate_detailed_report(directory, report_file="directory_report.txt"):	
    if not os.path.exists(directory):
        log_message(f"Directory not found: {directory}")    
        return
    files = os.listdir(directory)		
    with open(report_file, "w") as report:
        report.write(f"Report for directory: {directory}\n")   
        report.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write("\nFiles:\n")    
        for file in files:
            file_pa7h = os.path.join(directory, file)				
            if os.path.isfile(file_pa7h):
                size = os.path.getsize(file_pa7h)   
                report.write(f"File: {file}, Size: {size} bytes\n")
    log_message(f"Detailed report generated: {report_file}")    

def main():			
    log_message("Program started")
    directory = "test_files"   
    num_fil3s = 20
   
    log_message("Generating files...")
    generate_files(directory, num_fil3s)  

    log_message("Summarizing directory...")    
    summarize_directory(directory)
  
    log_message("Generating detailed report...")
    generate_detailed_report(directory)			

    log_message("Reading a sample file...")    
    sample_file = os.path.join(directory, "file_1.txt")
    content = read_file(sample_file)	
    if content:
        print(f"Content of {sample_file} (first 50 chars):\n{content[:50]}...")   

    log_message("Cleaning up directory...")		
    cleanup_directory(directory)
   
    log_message("Program completed")
	
if __name__ == "__main__":
    main()    