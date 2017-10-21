'''
This is the main.py file for OpSys Project 1 F17 by Samad Farooqui, Aaron Taylor, and John C. Fantell. 

It will be implementing 3 CPU scheduling algorithms, and using them to get statistics about some input. 

The three algorithms implemented are First Come First Serve, Shortest Remaining Time, and Round Robin. 
'''

import sys 
from fcfs import *
from fcfs import rr
from srt import srt

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
					continue
				else: 
					split_line[-1] = split_line[-1].replace('\n', '')
					for i in range(0, len(split_line)):
						if (split_line[i].isdigit()):
							split_line[i] = int(split_line[i])
					process_list.append(split_line)
	return process_list

# Format the stats of each algorithm
def print_stats(stats, algorithm):
	print("Algorithm",algorithm)
	print("-- average CPU burst time: {:.2f} ms".format(stats[0]))
	print("-- average wait time: {:.2f} ms".format(stats[1]))
	print("-- average turnaround time: {:.2f} ms".format(stats[2]))
	print("-- total number of context switches: {}".format(stats[3]))
	print("-- total number of preemptions: {}".format(stats[4]))

if __name__ == '__main__':
	 
	process_list = []
	process_input = []
	go_through_with_program = True

	if len(sys.argv) < 3: 
		print("ERROR: Not enough commandline arguments.")
		go_through_with_program = False 
	
	if go_through_with_program:

		# Get file input 
		list_of_processes = get_instructions(sys.argv[1])

		# Convert file input to a series of Process objects
		process_list = [Process(p[0],p[1],p[2],p[3],p[4]) for p in list_of_processes]
		process_list1 = [Process(p[0],p[1],p[2],p[3],p[4]) for p in list_of_processes]
		process_list2 = [Process(p[0],p[1],p[2],p[3],p[4]) for p in list_of_processes]

		# Call each algorithm and report the stats
		fcfs = fcfs(process_list)
		print("")
		srt = srt(process_list1)
		print("")
		rr = rr(process_list2)
		filename = sys.argv[2]
		with open(filename,'w') as f:
			f.write("Algorithm FCFS\n")
			f.write("-- average CPU burst time: {:.2f}".format(fcfs[0])+ " ms\n")
			f.write("-- average wait time: {:.2f}".format(fcfs[1])+ " ms\n")
			f.write("-- average turnaround time: {:.2f}".format(fcfs[2])+ " ms\n")
			f.write("-- total number of context switches: {}".format(int(fcfs[3])) + "\n")
			f.write("-- total number of preemptions: {}".format(int(fcfs[4])) + "\n")
			f.write("Algorithm SRT\n")
			f.write("-- average CPU burst time: {:.2f}".format(srt[0])+ " ms\n")
			f.write("-- average wait time: {:.2f}".format(srt[1])+ " ms\n")
			f.write("-- average turnaround time: {:.2f}".format(srt[2])+ " ms\n")
			f.write("-- total number of context switches: {}".format(int(srt[3])) + "\n")
			f.write("-- total number of preemptions: {}".format(int(srt[4])) + "\n")
			f.write("Algorithm RR\n")
			f.write("-- average CPU burst time: {:.2f}".format(rr[0])+ " ms\n")
			f.write("-- average wait time: {:.2f}".format(rr[1])+ " ms\n")
			f.write("-- average turnaround time: {:.2f}".format(rr[2])+ " ms\n")
			f.write("-- total number of context switches: {}".format(int(rr[3])) + "\n")
			f.write("-- total number of preemptions: {}".format(int(rr[4])) + "\n")
		# print(rr)
		# print_stats(fcfs(process_list), "FCFS")
		# print_stats(srt,"SRT")
		