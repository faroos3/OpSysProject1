'''
This is the main.py file for OpSys Project 1 F17 by Samad Farooqui, Aaron Taylor, and John C. Fantell. 

It will be implementing 3 CPU scheduling algorithms, and using them to get statistics about some input. 

The three algorithms implemented are First Come First Serve, Shortest Remaining Time, and Round Robin. 
'''

import sys 

# This function will get all the arguments in the filename. 
def get_instructions(file_name):
	return
	
if __name__ == '__main__':
	
	go_through_with_program = True 
	if len(sys.args) < 2: 
		print("ERROR: Not enough commandline arguments.")
		go_through_with_program = False 
	
	if go_through_with_program: 
		list_of_processes = get_instructions(sys.args[1])
		