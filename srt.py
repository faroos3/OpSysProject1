from fcfs import Process
from fcfs import CPU_Burst
import heapq

# Format the queue for output
def format_queue(queue):
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


# While processes are in the queue, increase their wait time
def increase_wait_time(queue):
	for process in queue:
		(process[1]).increase_wait_time()


def SRT(process_list):	
	t = 0    				# time in ms
	t_cs = 4 				# time to perform context switch
	IO_list = {} 			# { {time process's IO will finish : process} }
	ready = True			# CPU state
	ready_queue = []		# heapq, [ [process cpu burst time, process] ]
	burst_end_time = 0 		# time the current process will finish it's burst
	current_process = None
	context_switch = False  # check for context switch
	completed_processes = []

	print("time 0ms: Simulator started for SRT [Q <empty>]")
	while(t < 50000):

		'''
		Check if a a processed arrived, then check for preemption
		or add it to the queue
		'''
		for process in process_list:

			if(t == process.get_arrival_t()):
				
				'''
				Check for preemption on arrival by comparing burst time of the process and 
				the remaining time of the current process
				'''
				if current_process != None and process.get_cpu_t() < (burst_end_time - t):
					
					print("time {}ms: Process {} arrived and will preempt {} {}".format(t,process,current_process,format_queue(ready_queue)))

					# Add the current process back to the queue with it's remaining time
					heapq.heappush(ready_queue,[burst_end_time - t, current_process]) 

					# Set the process as the new current process
					current_process = process
					print("time {}ms: Process {} started using the CPU {}".format(t,current_process,format_queue(ready_queue)))
					context_switch = True
					t += t_cs # Account for context switch
					burst_end_time = t+current_process.get_cpu_t()

				else:

					# Add the process to the queue if there is no preemption
					heapq.heappush(ready_queue,[process.get_cpu_t(),process])
					print("time {}ms: Process {} arrived and added to ready queue {}".format(t,process,format_queue(ready_queue)))

		# Start a process if the CPU is open
		if(ready == True and current_process == None):
			ready = False
			t += t_cs # Account for context switch
			queued_process = heapq.heappop(ready_queue)
			burst_end_time, current_process = queued_process[0]+t, queued_process[1]
			if queued_process[0] != current_process.get_cpu_t():
				print("time {}ms: Process {} started using the CPU with {}ms remaining {}".format(t,current_process,queued_process[0],format_queue(ready_queue)))
			else:
				print("time {}ms: Process {} started using the CPU {}".format(t,current_process,format_queue(ready_queue)))

		# Preemption Check
		if ready == False:
			for process in ready_queue:

				# If the current process's remaining time is more than a queued process, 
				if process[1].get_cpu_t() < (burst_end_time - t):
					
					# Add the current process to the queue with it's remaining time
					heapq.heappush(ready_queue,[burst_end_time - t, current_process]) 
					print("time {}ms: Process {} arrived and will preempt {} {}".format(t,process[1],current_process,format_queue(ready_queue)))
					current_process = heapq.heappop(ready_queue)[1]
					context_switch = True
					t += t_cs # Account for context switch
					burst_end_time = t+current_process.get_cpu_t()

		'''
		If the current process has finised it's burst check if it has remaining bursts
		add it to the IO List and set the CPU up to take a new process. If not, mark
		the process as finished.
		'''
		if ready == False and current_process != None and t == burst_end_time:
			current_process.burst_complete() # Decrement the number of bursts

			# Send process to complete IO
			if current_process.get_num_bursts() > 0:
				IO_list[t+current_process.get_io_t()] = current_process 
				print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(t,current_process,current_process.get_num_bursts(),format_queue(ready_queue)))
				print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(t,current_process,t+current_process.get_io_t(),
				format_queue(ready_queue)))
				current_process = None 
				ready = True
				context_switch = True
				t += t_cs # Account for context switch

			else:
				# Mark the process as completed and start a new one
				completed_processes.append(current_process)
				print("time {}ms: Process {} terminated {}".format(t,current_process,format_queue(ready_queue)))
				t += t_cs # Account for context switch
				queued_process = heapq.heappop(ready_queue)
				burst_end_time, current_process = queued_process[0]+t, queued_process[1]
				if queued_process[0] != current_process.get_cpu_t():
					print("time {}ms: Process {} started using the CPU with {}ms remaining {}".format(t,current_process,queued_process[0],format_queue(ready_queue)))
				else:
					print("time {}ms: Process {} started using the CPU {}".format(t,current_process,format_queue(ready_queue)))

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
					print("time {}ms: Process {} terminated {}".format(t,process,format_queue(ready_queue)))
					completed_processes.append(process)
				else:

					# Check for preemption 
					if process.get_cpu_t() < (burst_end_time - t):

						print("time {}ms: Process {} completed I/O and will preempt {} {}".format(t,process,current_process,format_queue(ready_queue)))
						heapq.heappush(ready_queue,[current_process.get_cpu_t(), current_process])
						current_process = process
						context_switch = True
						t += t_cs # Account for context switch
						burst_end_time = t+current_process.get_cpu_t()
						ready = False
						print("time {}ms: Process {} started using the CPU {}".format(t,current_process,format_queue(ready_queue)))

					else:
						print("time {}ms: Process {} completed I/O; added to ready queue {}".format(t,process,format_queue(ready_queue)))
						heapq.heappush(ready_queue,[process.get_cpu_t(), process])

				del IO_list[key]
				break

		# Increase the wait time of all processes in the queue
		increase_wait_time(ready_queue)

		# Exit when all processes are complete (No mory CPU Bursts or IO Operations)
		if len(ready_queue) == 0 and len(IO_list) < 0:
			break
		# if context_switch == True:
		# 	t+=t_cs
		# else:
		t+=1
	return completed_processes 

if __name__ == '__main__':
	
	# <proc-id>|<initial-arrival-time>|<cpu-burst-time>|<num-bursts>|<io-time>
	process_list = list([
		Process('A',0,168,5,287),
		Process('B',0,385,1,0),
		Process('C',190,97,5,2499), 
		Process('D',250,1770,2,822)
	])
	
	SRT(process_list)


