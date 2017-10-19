'''
This is the file which contains the Round Robin algorithm. 
'''

import math
from fcfs import Queue, Process, CPU_Burst


'''
Pseudo-code for RR 

Notes: 
	-Using John's process class, may need to make some mods. 
	-Question - calling burst_complete() should change it in the 
		master list right? Yeah it will, adding it back later.
	- might need to make an equals operator for Process so i can .index()
	- add a member variable to John's thing called wait time 
	-- go through each process and check to see if it's the active process. Go through the I/O adjacency list. if it's not there, and it's not the active process, and i is greater than arrival time, then up wait time by 1. 
	- need to add a variable to keep track of cs and preepmtions. 
RR PC: 
	real_process_list = [] # going to use the Process class S/O John 
	for process in process_list: 
		process_obj = Process(process)
		real_process_list.append(process_obj)
	t_slice = 70 # this is the time_slice that each process gets. 
	t_cs = 8 
	q = Queue()
	# this is the active time_slice - when this is equal to t_slice
	# it will preempt if there is a process running. 
	t_action = 0 
	i = 0
	j = 0 
	num_cs = 0 
	num_preempts = 0
	all_done = False # boolean flag to see if we're done w/ all processes. 
	cs_flag = False # context switch flag. if it happens, then don't i+=1.
	current_process_i = 0 
	active_process = None # this is if there is an active process running. 
	cpu = CPU_Burst() # might not use this. will try not to. 
	# set up an adjacency list of active times left per burst for each process
	remaining_burst_times = [] 
	io_list = [] 
	for num in range(len(process_list)):
		remaining_burst_times.append(0)
		io_list.append(0, None) # first entry is time to add back to q, second is process. 
	
	# start the timer. 
	while i < 50000: # arbitrarily big ms number. 
		cs_flag = False # should be false to start. 
		for process in process_list:
			if(i == process.get_arrival_t()):
				q.enqueue(process)
				print Process whatever arrived and added to the ready q then print q
		
		
		if(q isn't empty and active_process == None):
			# there's no active process and there's crap 
			# in the queue. 
			# also have to make sure the process isn't in the io_list wait no you don't since IO_list stuff adds it. 
			active_process = q.dequeue() 
			# active_process.burst_complete() # should this come in a section where it actually completes? not here? it's not FCFS...
			t_action = 0 # IMPORTANT! What to compare t_slice to.
			for current_process_i in range(len(real_process_list)):
				if real_process_list[current_process_i].get_process_id() == active_process.get_process_id():
					# should set current_process_i to what it's supposed to be but if it doesn't then have it use k and set current_process_i to k before break. 
					break 
			# above loop should always return the index, need it for remaining_burst_times list 
			io_list[current_process_i] = (0, False)
			if(remaining_burst_times[current_process_i] <= 0): # means it's not from a previous thing 
				remaining_burst_times[current_process_i] = active_process.get_cpu_t()
			i += cs_time # should be all good for context switches. Don't think flag is needed. Actually don't think this is needed. 
			cs_flag = True
			
			print Process whatever started using the CPU (print q)
			
		# preempt
		if t_action == t_slice and remaining_burst_times[current_process_i] != 0:
			t_action = 0 # reset this. 
			print time and time slice expired; process (id) terminated with remaining_burst_times[current_process_i]ms to go and q
			q.enqueue(active_process)
			# I don't think I need to set active_process to anything since above handles it.
			active_process = None 
			
		elif remaining_burst_times[current_process_i] == 0: #don't preempt, done. 
			t_action = 0 
			active_process.burst_complete()
			if (active_process.get_num_bursts() == 0):
				print process id terminated print q 
				active_process =None 
				break 
			else: # has more bursts to complete. 
				print Process (id) completed a CPU burst; active_process.get_num_bursts left to go. 
				time_to_start = i + active_process.get_I/O_time()
				print Process id switching out; will block on I/O until time_to_start print q 
				io_list[current_process_i] = (time_to_start, active_process)
				active_process = None 
		
		# Go through the IO list and see if there's anything that has to be added. 
		for item in io_list: 
			if item[0] == i: 
				print Process id completed IO. added to ready queue print q 
				q.enqueue(item[1])
				item = (0,false) 
		# 
		if(q is empty): 
			for each process in real process_list: 
				if there's a process arrival time larger than i: 
					set all_done = false 
		
		if(all_done):
			print we're done w/ the time. 
			break 
		
		
		i +=1 
		t_action +=1 
		remaining_burst_times[current_process_i] -=1
		
'''

def rr(process_list):
	real_process_list = [] # going to use the Process class S/O John 
	for process in process_list: 
		process_obj = Process(process[0], process[1], process[2], process[3], process[4])
		real_process_list.append(process_obj)
	t_slice = 70 # this is the time_slice that each process gets. 
	t_cs = 8 
	q = Queue()
	# this is the active time_slice - when this is equal to t_slice
	# it will preempt if there is a process running. 
	t_action = 0 
	i = 0
	j = 0 
	num_cs = 0 
	num_active_processes = 0
	num_preempts = 0
	all_done = False # boolean flag to see if we're done w/ all processes. 
	cs_flag = False # context switch flag. if it happens, then don't i+=1.
	current_process_i = 0 
	active_process = None # this is if there is an active process running. 
	cpu = CPU_Burst() # might not use this. will try not to. 
	# set up an adjacency list of active times left per burst for each process
	remaining_burst_times = [] 
	io_list = [] 
	print("time 0ms: Simulator started for RR [Q <empty>]")
	for num in range(len(process_list)):
		remaining_burst_times.append(0)
		io_list.append((0, None)) # first entry is time to add back to q, second is process. 
	
	while (i < 200000): # start the process 
		cs_flag = False
		all_done = True # dangerous, but try it anyway. 
		for process in real_process_list:
			if(i == process.get_arrival_t()):
				q.enqueue(process)
				print(("time {:d}ms: Process {} arrived and added to ready queue").format(i, process.get_process_id()), str(q))
				num_active_processes +=1 # WARNING 
		if (not q.isEmpty() and active_process == None):
			active_process = q.dequeue()
			t_action = 0
			for current_process_i in range(len(real_process_list)):
				if real_process_list[current_process_i].get_process_id() == active_process.get_process_id():
					break
			io_list[current_process_i] = (0, False)
			if(remaining_burst_times[current_process_i] <= 0):
				remaining_burst_times[current_process_i] = active_process.get_cpu_t()
			# if not first process 
			if (num_active_processes != 1):
				i += t_cs//2
				cs_flag = True
			# put print statement here 
			print(("time {:d}ms: Process {} started using the CPU").format(i, active_process.get_process_id()), str(q)) # q doesn't have an str. 
		# preempt
		if t_action == t_slice and remaining_burst_times[current_process_i] != 0: 
			if not q.isEmpty(): # there are other processes waiting to run 
				t_action = 0 
				print(("time {:d}ms: Time slice expired; process {} preempted with {:d}ms to go").format(i, active_process.get_process_id(), remaining_burst_times[current_process_i]), str(q))
				q.enqueue(active_process)
				active_process = None 
				num_preempts += 1
			else: # continue on with the current process 
				t_action = 0
				print("time {:d}ms: Time slice expired; no preemption because ready queue is empty".format(i), str(q))
		elif remaining_burst_times[current_process_i] == 0: # don't think I need to do anything w/ time_slice here, if there's an issue then do so
			# this should be if a process is all done. 
			t_action = 0 
			active_process.burst_complete()
			if active_process.get_num_bursts() == 0: 
				print(("time {:d}ms: Process {} terminated").format(i, active_process.get_process_id()), str(q))
				active_process = None 
			elif (active_process.get_num_bursts() != 0):
				print(("time {:d}ms: Process {} completed a CPU burst; {:d} to go").format(i, active_process.get_process_id(), active_process.get_num_bursts()), str(q))
				time_to_start = i + active_process.get_io_t()
				print(("time {:d}ms: Process {} switching out of CPU; will block on I/O until time").format(i, active_process.get_process_id()), str(time_to_start)+"ms", str(q))
				io_list[current_process_i] = (time_to_start, active_process)
				active_process = None 
				i += t_cs
				cs_flag = True
		
		# go through I/O list and see if anything needs to be added. 
		for itr in range(len(io_list)):
			if io_list[itr][0] == i and io_list[itr][1] != None:
				q.enqueue(io_list[itr][1])
				print(("time {:d}ms: Process {} completed I/O; added to ready queue").format(i, io_list[itr][1].get_process_id()), str(q))
				io_list[itr] = ((0, False))
		if(q.isEmpty()):
			for process_itr in real_process_list:
				if process_itr.get_arrival_t() > i:
					all_done = False
			for itr in range(len(io_list)):
				if io_list[itr][0] != 0 and io_list[itr][1] != None:
					all_done = False
		else:
			all_done = False
		if (all_done):
			print(("time {:d}ms: Simulator ended for RR").format(i))
			break 
		if(not cs_flag):
			i+=1 
		t_action += 1 
		remaining_burst_times[current_process_i] -=1 
	return 0 # will be a tuple of stats. 