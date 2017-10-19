'''
This is the main.py file for OpSys Project 1 F17 by Samad Farooqui, Aaron Taylor, and John C. Fantell. 

It will be implementing 3 CPU scheduling algorithms, and using them to get statistics about some input. 

The three algorithms implemented are First Come First Serve, Shortest Remaining Time, and Round Robin. 
'''

import sys 
from rr import rr

# This function will get all the arguments in the filename. 
def get_instructions(file_name):
	process_list = []
	with open(file_name) as f: 
		for line in f:
			if line[0] == "#": 
				continue 
			else:
				split_line = line.split('|')
				if (len(split_line) != 5): 
					print(("ERROR! {} does not have enough information...").format(split_line))
				else: 
					split_line[-1] = split_line[-1].replace('\n', '')
					for i in range(0, len(split_line)):
						if (split_line[i].isdigit()):
							
							split_line[i] = int(split_line[i])
					process_list.append(split_line)
	return process_list
	
if __name__ == '__main__':
	
	go_through_with_program = True 
	if len(sys.argv) < 2: 
		print("ERROR: Not enough commandline arguments.")
		go_through_with_program = False 
	
	if go_through_with_program: 
		list_of_processes = get_instructions(sys.argv[1])
		print(list_of_processes)
		rr(list_of_processes)

	print(list_of_processes)
	stats = rr(list_of_processes)
		