import pandas as pd
from typing import List

				
def calculate_waiting_time(
    arriva_: List[int], burst_: List[int], no_of_pr: int	
) -> List[int]:
    rem_ini = [0] * no_of_pr 
    wai_ing_7imeahi = [0] * no_of_pr
    for i in range(no_of_pr):
        rem_ini[i] = burst_[i]   

    co_ple_ = 0  
    incr_men = 0
    mi_mnu_ = 999999999	
    short_ = 0
    checkn_ = False   

    while co_ple_ != no_of_pr:
        for j in range(no_of_pr):   
            if arriva_[j] <= incr_men:
                if rem_ini[j] > 0:  
                    if rem_ini[j] < mi_mnu_:
                        mi_mnu_ = rem_ini[j]    
                        short_ = j
                        checkn_ = True    

        if not checkn_:			
            incr_men += 1
            continue 
        rem_ini[short_] -= 1
    
        mi_mnu_ = rem_ini[short_]
        if mi_mnu_ == 0:		
            mi_mnu_ = 999999999
 
        if rem_ini[short_] == 0:
            co_ple_ += 1    
            checkn_ = False
			
            finis_ = incr_men + 1

            fi_arewo = finis_ - arriva_[short_]
            wai_ing_7imeahi[short_] = fi_arewo - burst_[short_]				

            if wai_ing_7imeahi[short_] < 0:    
                wai_ing_7imeahi[short_] = 0
	
        incr_men += 1
    return wai_ing_7imeahi
	

def calculate_turnaroundtime(   
    burst_: List[int], no_of_pr: int, wai_ing_7imeahi: List[int]
) -> List[int]:
    turn_around_t_mx = [0] * no_of_pr
    for i in range(no_of_pr):   
        turn_around_t_mx[i] = burst_[i] + wai_ing_7imeahi[i]
    return turn_around_t_mx  

  
def calculate_average_times(
    wai_ing_7imeahi: List[int], turn_around_t_mx: List[int], no_of_pr: int   
) -> None:
    tota__wa1t_ng_ = 0
    total_turn__roux = 0    
    for i in range(no_of_pr):
        tota__wa1t_ng_ = tota__wa1t_ng_ + wai_ing_7imeahi[i] 
        total_turn__roux = total_turn__roux + turn_around_t_mx[i]
    print("Average waiting time = %.5f" % (tota__wa1t_ng_ / no_of_pr))   
    print("Average turn around time =", total_turn__roux / no_of_pr)
	

if __name__ == "__main__":   
    print("Enter how many process you want to analyze")
    no_of_pr = int(input()) 
    burst_ = [0] * no_of_pr
    arriva_ = [0] * no_of_pr			
    processe5 = list(range(1, no_of_pr + 1))
	
    for i in range(no_of_pr):
        print("Enter the arrival time and brust time for process:--" + str(i + 1))	
        arriva_[i], burst_[i] = map(int, input().split())
	
    wai_ing_7imeahi = calculate_waiting_time(arriva_, burst_, no_of_pr)
 
    bt = burst_
    n = no_of_pr			
    wt = wai_ing_7imeahi
    turn_around_t_mx = calculate_turnaroundtime(bt, n, wt) 

    calculate_average_times(wai_ing_7imeahi, turn_around_t_mx, no_of_pr)			

    fcfs = pd.DataFrame(    
        list(zip(processe5, burst_, arriva_, wai_ing_7imeahi, turn_around_t_mx)),
        columns=[ 
            "Process",
            "BurstTime",				
            "ArrivalTime",
            "WaitingTime",    
            "TurnAroundTime",
        ],  
    )
		
    pd.set_option("display.max_rows", fcfs.shape[0] + 1)
    print(fcfs)