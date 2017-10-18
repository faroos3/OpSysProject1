from fcfs import Process
from fcfs import CPU_Burst
import Queue as Q

# Format the queue for output
def format_queue(queue):
	output = "[Q"
	if queue.qsize() == 0:
		output += " <empty>]"
	else:
		for i in range(queue.qsize()):
			if i == (queue.qsize() - 1):
				output += " " + str(queue.queue[i]) + "]"
			else:
				output += " " + str(queue.queue[i])
	return output

''' While processes are in the queue, increase their wait time'''
def increase_wait_time(queue):
	for i in range(queue.qsize()):
		queue.queue[i].increase_wait_time()


def SRT(process_list):
	
	t = 0    # time in ms
	t_cs = 8 # time to perform context switch
	ready = True
	IOList = {}
	ready_queue = Q.PriorityQueue()
	current_process = None
	start_time = 0

	print("time 0ms: Simulator started for SRT [Q <empty>]")
	while(t < 20000):

		'''
		Check if a a processed arrived,then check for preemption
		or add it to the queue
		'''
		for process in process_list:

			if(t == process.get_arrival_t()):

				# Preemption
				if(ready == False and current_process != None):
					if (process < current_process):
						ready_queue.put(current_process)
						print("time {}ms: Process {} arrived and will preempt {} {}".format(t,process,w_process,format_queue(ready_queue)))

				# Add the process to the queue
				if ready == True and current_process == None:
					ready_queue.put(process)
					ready = False
					print("time {}ms: Process {} arrived and added to the ready queue {}".format(t,process,format_queue(ready_queue)))

		# Starting process
		current_process = ready_queue.get(process)
		if ready == False:
			start_time = t

		'''
		If the current process has finised it's burst
		add it to the IO List and set the CPU up to take a new process
		'''
		if (t - start_time) == current_process.get_cpu_t():
			current_process.burst_complete() # Decrement the number of bursts
			IO_List.append({time,current_process}) 
			current_process = None 
			ready = True
			print("time {}ms: Process {} arrived and added to the ready queue {}".format(t,process,format_queue(ready_queue)))

		# Exit when all processes are complete (No mory CPU Bursts or IO Operations)
		if ready_queue.qsize():
			break
		t+=1
	return True 

if __name__ == '__main__':
	
	# <proc-id>|<initial-arrival-time>|<cpu-burst-time>|<num-bursts>|<io-time>
	process_list = list([
		Process('A',0,168,5,287),
		Process('B',0,385,1,0),
		Process('C',190,97,5,2499), 
		Process('D',250,1770,2,822)
	])

	# Number of processes to simulate
	n = 0

	SRT(process_list)


