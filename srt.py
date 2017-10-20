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


def srt(process_list):	
	t = 0    				# time in ms
	t_cs = 8 				# time to perform context switch
	IO_list = {} 			# { {time process's IO will finish : process} }
	ready = True			# CPU state
	ready_queue = []		# heapq, [ [process cpu burst time, process] ]
	burst_end_time = 0 		# time the current process will finish it's burst
	current_process = None
	completed_processes = []
	preempt = context_switch = finished = False  # check for context switch and completion

	# turnaround time = arrivaltime + t
	context = avg_wait = avg_turn = avg_burst = preemption = 0

	print("time 0ms: Simulator started for SRT [Q <empty>]")
	while(finished != True):
		
		'''
		If the current process has finised it's burst check if it has remaining bursts
		add it to the IO List and set the CPU up to take a new process. If not, mark
		the process as finished.
		'''
		if t != 0 and t == burst_end_time:
			current_process.burst_complete() # Decrement the number of bursts

			# Send process to complete IO
			if current_process.get_num_bursts() > 0:
				IO_list[t+current_process.get_io_t()+4] = current_process
				if current_process.get_num_bursts() == 1:
					print("time {}ms: Process {} completed a CPU burst; {} burst to go {}".format(t,current_process,current_process.get_num_bursts(),format_queue(ready_queue)))
				else:
					print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(t,current_process,current_process.get_num_bursts(),format_queue(ready_queue)))
				print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(t,current_process,t+current_process.get_io_t()+4,
				format_queue(ready_queue)))

				# Mark the CPU as open
				context_switch=True
				context+=1
				ready = True
				burst_end_time = 0
				current_process = None

			else:

				# Mark the process as completed and start a new one
				process.set_end_t(t)
				completed_processes.append(current_process)
				print("time {}ms: Process {} terminated {}".format(t,current_process,format_queue(ready_queue)))
				context_switch=True
				context+=1
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
					print("time {}ms: Process {} terminated {}".format(t,process,format_queue(ready_queue)))
					process.set_end_t(t)
					completed_processes.append(process)
				else:

					# Check for preemption 
					context_switch = True
					if process.get_cpu_t() < (burst_end_time - t):

						print("time {}ms: Process {} completed I/O and will preempt {} {}".format(t,process,current_process,format_queue(ready_queue)))
						if current_process == None:
							heapq.heappush(ready_queue,[burst_end_time-t+4, current_process])
						else:
							heapq.heappush(ready_queue,[burst_end_time-t+t_cs, current_process])
						context+=1
						preemption+=1

						# Mark the CPU as open
						ready = True
						burst_end_time = 0
						current_process = None

					else:

						heapq.heappush(ready_queue,[process.get_cpu_t(), process])
						print("time {}ms: Process {} completed I/O; added to ready queue {}".format(t,process,format_queue(ready_queue)))

		'''
		Check if a a processed arrived, then check for preemption
		or add it to the queue
		'''
		for process in process_list:

			if(t == process.get_arrival_t()):
				'''
				Check for preemption by comparing burst time of the process and 
				the remaining time of the current process
				'''
				if (process.get_cpu_t() < (burst_end_time - t)) or (process.get_cpu_t() == (burst_end_time - t) and (str(process) < str(current_process))):
					print("time {}ms: Process {} arrived and will preempt {} {}".format(t,process,current_process,format_queue(ready_queue)))

					# Add the current process back to the queue with it's remaining time
					heapq.heappush(ready_queue,[burst_end_time - t, current_process]) 

					# Set the process as the new current process
					context+=1
					preemption+=1
					context_switch =True
					
					# Mark the CPU as open
					ready = True
					burst_end_time = 0
					current_process = None

				else:

					# Add the process to the queue if there is no preemption
					heapq.heappush(ready_queue,[process.get_cpu_t(),process])
					print("time {}ms: Process {} arrived and added to ready queue {}".format(t,process,format_queue(ready_queue)))

		'''
		Check for preemption by objects in the queue
		'''
		# for i in range(len(ready_queue)):
		# 	if ready_queue[i][0] < (burst_end_time - t):
		# 		heapq.heappush(ready_queue, [burst_end_time - t, current_process])
		# 		ready = True
		# 		burst_end_time = 0
		# 		current_process = None

		# Start a process if the CPU is open
		if ready == True and len(ready_queue) > 0:
			context+=1
			context_switch = True
			ready = False
			queued_process = heapq.heappop(ready_queue)
			if current_process == None:
				burst_end_time = queued_process[0]+t+4
			else:
				burst_end_time = queued_process[0]+t+t_cs
			current_process = queued_process[1]
			if queued_process[0] < queued_process[1].get_cpu_t():
				print("time {}ms: Process {} started using the CPU with {}ms remaining {}".format(t+4,current_process,queued_process[0],format_queue(ready_queue)))
			else:
				print("time {}ms: Process {} started using the CPU {}".format(t+4,current_process,format_queue(ready_queue)))

		# Increase the wait time of all processes in the queue
		increase_wait_time(ready_queue)

		# Exit when all processes are complete (No mory CPU Bursts or IO Operations)
		if len(process_list) == len(completed_processes):
			t+=4 # account for final queue exit
			finished = True

		# Increment time normally if a context switch didn't occur
		if context_switch == True:
			if preempt == True:
				t+=t_cs
				preempt = False
			else:
				t+=4 # about to switch to new process
			context_switch = False
		else:
			t+=1

	print("time {}ms: Simulator ended for SRT".format(t))

	# Calulate stats
	for process in completed_processes:
		avg_burst+=process.get_cpu_t()
		avg_wait+=process.get_wait_time()
		avg_turn+= (process.get_end_t() - process.get_arrival_t() - (process.get_io_t() * 4) - process.get_wait_time())
	return [float(avg_burst)/len(process_list),float(avg_wait)/len(process_list),float(avg_turn)/len(process_list),context,preemption] 

if __name__ == '__main__':
	
	# Input 1
	# process_list = list([
	# 	Process('A',0,168,5,287),
	# 	Process('B',0,385,1,0),
	# 	Process('C',190,97,5,2499), 
	# 	Process('D',250,1770,2,822)
	# ])

	# Input 2
	# process_list = list([
	# 	Process('X',0,80,5,500)
	# ])

	# Input 3
	# process_list = list([
	# 	Process('X',0,560,5,20),
	# 	Process('Y',0,840,5,20),
	# 	Process('Z',0,924,5,20)
	# ])

	# Input 6
	process_list = list([
		Process("A",0,20,5,40),
		Process("B",20,36,2,100),
		Process("C",68,30,1,0)
	])

	srt(process_list)
