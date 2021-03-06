from fcfs import *
import heapq

# Format the queue for output
def format_queue(queue):
	queue.sort(key=lambda x: x[1].get_process_id())
	output = "[Q"
	if len(queue) == 0:
		output += " <empty>]"
	else:
		for i in range(len(queue)):
			if i == (len(queue) - 1):
				output += " " + str(queue[i][1]) + "]"
			else:
				output += " " + str(queue[i][1])
	return output

def increase_wait(queue, time):
	for process in queue:
		process[1].increase_wait_t(time)

def srt(processes_list):	
	processes_list.sort(key=lambda x: x.get_process_id())
	t = 0    				# time in ms
	t_cs = 8 				# time to perform context switch
	IO_list = {} 			# { {time process's IO will finish : process} }
	ready = True			# CPU state
	ready_queue = []		# heapq, [ [process cpu burst time, process] ]
	burst_end_time = 0 		# time the current process will finish it's burst
	current_process = None
	completed_processes = []
	context_switch = finished = replace = False  # check for context switch and completion
	context = avg_wait = avg_turn = avg_burst = total_bursts = preemption = 0

	# Set up some stats
	for process in processes_list:
		total_bursts+=process.get_num_bursts()
		avg_burst+=process.get_cpu_t()*process.get_num_bursts()

	print("time 0ms: Simulator started for SRT [Q <empty>]")
	while(finished != True):
		
		'''
		If the current process has finised it's burst check if it has remaining bursts
		add it to the IO List and set the CPU up to take a new process. If not, mark
		the process as finished.
		'''
		if t != 0 and t == burst_end_time:
			current_process.burst_complete() # Decrement the number of bursts
			return_time = t+current_process.get_io_t()+4 # IO end time with account for context switch

			# Send process to complete IO
			if current_process.get_num_bursts() > 0:
				replace = True
				IO_list[return_time] = current_process
				if current_process.get_num_bursts() == 1:
					print("time {}ms: Process {} completed a CPU burst; {} burst to go {}".format(t,current_process,current_process.get_num_bursts(),format_queue(ready_queue)))
				else:
					print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(t,current_process,current_process.get_num_bursts(),format_queue(ready_queue)))
				print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(t,current_process,return_time,
				format_queue(ready_queue)))

			else:
				
				# Mark the process as completed
				current_process.set_end_t(t)
				completed_processes.append(current_process)
				if len(ready_queue) == 2:
						increase_wait_t(ready_queue,4)
				print("time {}ms: Process {} terminated {}".format(t,current_process,format_queue(ready_queue)))
				
			# If the queue is empty we won't need to account for the 2nf half of the context switch
			if len(ready_queue) != 0:
				replace = True
			ready = True
			burst_end_time = 0
			current_process = None

		'''
		Check if a processes finished their IO, if it did, check if
		any bursts are left. If bursts are left, check for preemption
		or add it to the queue, if not mark it as finished.
		'''

		for key in IO_list:
			if key == t:
				process = IO_list[key]

				# Check if process terminated
				if process.get_num_bursts() == 0:
					context_switch = True
					print("time {}ms: Process {} terminated {}".format(t,process,format_queue(ready_queue)))
					process.set_end_t(t)
					if len(ready_queue) == 1:
						increase_wait(ready_queue,4)
					completed_processes.append(process)
				else:

					# Check for preemption 
					IO = True
					context_switch = True
					if process.get_cpu_t() < (burst_end_time - t):
						replace = True
						print("time {}ms: Process {} completed I/O and will preempt {} {}".format(t,process,current_process,format_queue(ready_queue)))
						process.increase_wait_t(4)
						if (len(ready_queue) == 0): # If the queue is empty, the current process won't we taken off after we add it back
							current_process.increase_wait_t(4)
						heapq.heappush(ready_queue,[(burst_end_time-t,str(current_process)), current_process])
						heapq.heappush(ready_queue,[(process.get_cpu_t(),str(process)), process])
						preemption+=1

						# Mark the CPU as open
						ready = True
						burst_end_time = 0
						current_process = None

					else:
						context_switch = True
						# if (len(ready_queue) == 0):
							# process.increase_wait_t(4)
						heapq.heappush(ready_queue,[(process.get_cpu_t(),str(process)), process])
						print("time {}ms: Process {} completed I/O; added to ready queue {}".format(t,process,format_queue(ready_queue)))

		'''
		Check if a a processed arrived, then check for preemption
		or add it to the queue
		'''
		for process in processes_list:

			if(t == process.get_arrival_t()):
				'''
				Check for preemption by comparing burst time of the process and 
				the remaining time of the current process
				'''
				if (process.get_cpu_t() < (burst_end_time - t)) or (process.get_cpu_t() == (burst_end_time - t) and (str(process) < str(current_process))):
					print("time {}ms: Process {} arrived and will preempt {} {}".format(t,process,current_process,format_queue(ready_queue)))

					replace = True

					# Add the current process back to the queue with it's remaining time
					current_process.increase_wait_t(8)
					heapq.heappush(ready_queue,[(burst_end_time - t,str(current_process)), current_process]) 

					# Add the process to the queue if there is no preemption
					process.increase_wait_t(4)
					heapq.heappush(ready_queue,[(process.get_cpu_t(),str(process)),process])

					# Set the process as the new current process
					preemption+=1
					context_switch =True
					
					# Mark the CPU as open
					ready = True
					burst_end_time = 0
					current_process = None

				else:

					# Add the process to the queue if there is no preemption
					# if (len(ready_queue) == 0): # improves case 6
						# process.increase_wait_t(4)
					heapq.heappush(ready_queue,[(process.get_cpu_t(),str(process)),process])
					context_switch = True
					print("time {}ms: Process {} arrived and added to ready queue {}".format(t,process,format_queue(ready_queue)))

		# Start a process if the CPU is open
		if ready == True and len(ready_queue) > 0:
			ready = False
			context_switch = True
			queued_process = heapq.heappop(ready_queue)
			new_time = t
			if replace == True:
				burst_end_time = queued_process[0][0]+t+t_cs # context switch for taking off queue
				new_time +=t_cs
				increase_wait(ready_queue,8)
			elif context_switch == True:
				burst_end_time = queued_process[0][0]+t+4 # context switch for taking off queue
				new_time+= 4
				increase_wait(ready_queue,4)

			current_process = queued_process[1]
			if queued_process[0][0] < queued_process[1].get_cpu_t():
				print("time {}ms: Process {} started using the CPU with {}ms remaining {}".format(new_time,current_process,queued_process[0][0],format_queue(ready_queue)))
			else:
				print("time {}ms: Process {} started using the CPU {}".format(new_time,current_process,format_queue(ready_queue)))

		# Exit when all processes are complete (No mory CPU Bursts or IO Operations)
		if len(processes_list) == len(completed_processes):
			context_switch = True # account for final exit from CPU
			finished = True

		# Increment time normally if a context switch didn't occur
		if replace == True:
			t+=t_cs
			context+=0.5
			replace = False
		elif context_switch == True:
			t+=4 # about to switch to new process
			context+=0.5
			context_switch = False
		else:
			t+=1
			increase_wait(ready_queue,1)

	print("time {}ms: Simulator ended for SRT".format(t))

	# Calulate stats
	# Average turnaround time = total turnaround time for all processes / total number of CPU bursts (for ALL processes)
	# Turnaround time for a single process = finished time - arrival time - (iotime * (number of bursts -1))
	# Theoretically, the below should work as well:
	# Turnaround time for a single process = total context switch time + (number of bursts) * cpu burst time + wait time
	 
	# Add the turnaround times for each process and you get the total turnaround time for all processes.
	 
	# Average wait time = total wait time / total number of CPU bursts (for ALL processes)
	# Wait time for a single process = total time process spends in the ready queue
	for process in sorted(completed_processes):
		avg_wait+=process.get_wait_t()
		# avg_turn+= process.get_end_t() - process.get_arrival_t() - (process.get_io_t() * ())
	return [float(avg_burst)/total_bursts,float(avg_wait)/total_bursts,float(avg_turn)/total_bursts,int(context),preemption] 

# if __name__ == '__main__':
	
	# Input 1 WORKING
	# process_list = list([
	# 	Process('A',0,168,5,287),
	# 	Process('B',0,385,1,0),
	# 	Process('C',190,97,5,2499), 
	# 	Process('D',250,1770,2,822)
	# ])

	# Input 2 WORKING
	# process_list = list([
	# 	Process('X',0,80,5,500)
	# ])

	# Input 3 WORKING, Wait time off BY 4
	# process_list = list([
	# 	Process('X',0,560,5,20),
	# 	Process('Y',0,840,5,20),
	# 	Process('Z',0,924,5,20)
	# ])

	# Input 4 WORKING
	# process_list = list({
	# 	Process('A',0,100,4,200),
	# 	Process('B',0,101,4,200),
	# 	Process('C',0,102,4,200),
	# 	Process('X',0,103,4,200),
	# 	Process('Y',0,104,4,200),
	# 	Process('Z',0,105,4,200)
	# })
	# Input 5 OFF BY 4
	# process_list = list([
	# 	Process('T',0,700,5,20),
	# 	Process('U',20,340,6,40),
	# 	Process('V',190,940,3,200)
	# ])

	# Input 6 WORKING 
	# process_list = list([
	# 	Process("A",0,20,5,40),
	# 	Process("B",20,36,2,100),
	# 	Process("C",68,30,1,0)
	# ])

	# print(srt(process_list))