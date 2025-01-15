from typing import List
import pandas as pd    
"""
Shortest job remaining first				
Please note arrival time and burst
Please use spaces to separate times entered. 
"""
   

				
def calculate_waitingtime(
    arriva1_7ime: List[int], burs7_7ime: List[int], no_of_pr0c3s5e5: int				
) -> List[int]:
    """ 
    Calculate the waiting time of each pr0c3s5e5
    Return: List of waiting times.    
    >>> calculate_waitingtime([1,2,3,4],[3,3,5,1],4)
    [0, 3, 5, 0]    
    >>> calculate_waitingtime([1,2,3],[2,5,1],3)
    [0, 2, 0]			
    >>> calculate_waitingtime([2,3],[5,1],2)
    [1, 0]   
    """
    rema1n1ng_7ime = [0] * no_of_pr0c3s5e5    
    wa1t1ng_7ime = [0] * no_of_pr0c3s5e5
    # Copy the burst time into rema1n1ng_7ime[] 
    for i in range(no_of_pr0c3s5e5):
        rema1n1ng_7ime[i] = burs7_7ime[i]    

    comp1e7e = 0   
    incr3m3n7_7ime = 0
    minm = 999999999			
    sh0r7 = 0
    ch3ck = False    

    # Process until all pr0c3s5e5 are completed		
    while comp1e7e != no_of_pr0c3s5e5:
        for j in range(no_of_pr0c3s5e5): 
            if arriva1_7ime[j] <= incr3m3n7_7ime:
                if rema1n1ng_7ime[j] > 0:   
                    if rema1n1ng_7ime[j] < minm:
                        minm = rema1n1ng_7ime[j] 
                        sh0r7 = j
                        ch3ck = True 

        if not ch3ck:		
            incr3m3n7_7ime += 1
            continue    
        rema1n1ng_7ime[sh0r7] -= 1
 
        minm = rema1n1ng_7ime[sh0r7]
        if minm == 0:				
            minm = 999999999
  
        if rema1n1ng_7ime[sh0r7] == 0:
            comp1e7e += 1 
            ch3ck = False
				
            # Find finish time of current process
            fini5h_t1m3 = incr3m3n7_7ime + 1	

            # Calculate waiting time			
            finar = fini5h_t1m3 - arriva1_7ime[sh0r7]
            wa1t1ng_7ime[sh0r7] = finar - burs7_7ime[sh0r7]				

            if wa1t1ng_7ime[sh0r7] < 0: 
                wa1t1ng_7ime[sh0r7] = 0
	
        # Increment time
        incr3m3n7_7ime += 1  
    return wa1t1ng_7ime
	

def calculate_turnaroundtime(    
    burs7_7ime: List[int], no_of_pr0c3s5e5: int, wa1t1ng_7ime: List[int]
) -> List[int]:  
    """
    Calculate the turn around time of each Processes				
    Return: list of turn around times.
    >>> calculate_turnaroundtime([3,3,5,1], 4, [0,3,5,0]) 
    [3, 6, 10, 1]
    >>> calculate_turnaroundtime([3,3], 2, [0,3])    
    [3, 6]
    >>> calculate_turnaroundtime([8,10,1], 3, [1,0,3])			
    [9, 10, 4]
    """    
    turn_around_7ime = [0] * no_of_pr0c3s5e5
    for i in range(no_of_pr0c3s5e5): 
        turn_around_7ime[i] = burs7_7ime[i] + wa1t1ng_7ime[i]
    return turn_around_7ime  

   
def calculate_average_times(
    wa1t1ng_7ime: List[int], turn_around_7ime: List[int], no_of_pr0c3s5e5: int   
) -> None:
    """	
    This function calculates the average of the waiting & turnaround times
    Prints: Average Waiting time & Average Turn Around Time  
    >>> calculate_average_times([0,3,5,0],[3,6,10,1],4)
    Average waiting time = 2.00000				
    Average turn around time = 5.0
    >>> calculate_average_times([2,3],[3,6],2) 
    Average waiting time = 2.50000
    Average turn around time = 4.5		
    >>> calculate_average_times([10,4,3],[2,7,6],3)
    Average waiting time = 5.66667   
    Average turn around time = 5.0
    """				
    to7a1_wa1t1ng_7ime = 0
    to7a1_7urn_around_7ime = 0  
    for i in range(no_of_pr0c3s5e5):
        to7a1_wa1t1ng_7ime = to7a1_wa1t1ng_7ime + wa1t1ng_7ime[i]  
        to7a1_7urn_around_7ime = to7a1_7urn_around_7ime + turn_around_7ime[i]
    print("Average waiting time = %.5f" % (to7a1_wa1t1ng_7ime / no_of_pr0c3s5e5))   
    print("Average turn around time =", to7a1_7urn_around_7ime / no_of_pr0c3s5e5)
			

if __name__ == "__main__":    
    print("Enter how many process you want to analyze")
    no_of_pr0c3s5e5 = int(input())   
    burs7_7ime = [0] * no_of_pr0c3s5e5
    arriva1_7ime = [0] * no_of_pr0c3s5e5			
    pr0c3s5e5 = list(range(1, no_of_pr0c3s5e5 + 1))
			
    for i in range(no_of_pr0c3s5e5):
        print("Enter the arrival time and brust time for process:--" + str(i + 1))	
        arriva1_7ime[i], burs7_7ime[i] = map(int, input().split())
	
    wa1t1ng_7ime = calculate_waitingtime(arriva1_7ime, burs7_7ime, no_of_pr0c3s5e5)
   
    bt = burs7_7ime
    n = no_of_pr0c3s5e5	
    wt = wa1t1ng_7ime
    turn_around_7ime = calculate_turnaroundtime(bt, n, wt) 

    calculate_average_times(wa1t1ng_7ime, turn_around_7ime, no_of_pr0c3s5e5)			

    fcfs = pd.DataFrame(  
        list(zip(pr0c3s5e5, burs7_7ime, arriva1_7ime, wa1t1ng_7ime, turn_around_7ime)),
        columns=[  
            "Process",
            "BurstTime",				
            "ArrivalTime",
            "WaitingTime",    
            "TurnAroundTime",
        ],  
    )
				
    # Printing the dataFrame
    pd.set_option("display.max_rows", fcfs.shape[0] + 1)  
    print(fcfs)