from fcfs import Process
from fcfs import CPU_Burst
import Queue as Q

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


def SRT(process_list):
	
	time = 0 # measured in ms
	cpu = CPU_Burst()
	ready_queue = Q.PriorityQueue()
	current_process = cpu.get_current_cpu_process()

	while(time < 20000):

		if time == 0:
			print("time {}ms: Simulator started for SRT [Q <empty>]".format(0))

		'''
		Check if a a processed arrived,then check for preemption
		or add it to the queue
		'''
		for process in process_list:

			if(time == process.get_arrival_t()):

				if(cpu.ready(time) == False and current_process != None):
					if (process < current_process):
						cpu.set_cpu(process,time)
						ready_queue.put(current_process)
						print("time {}ms: Process {} arrived and will preempt {} {}".format(time,process,w_process,format_queue(ready_queue)))

				else:	
					ready_queue.put(process)
					print("time {}ms: Process {} arrived and added to the ready queue {}".format(time,process,format_queue(ready_queue)))

		# Check if CPU is ready to accept a process (ready state)
		if(cpu.ready(time)):
			
			# Get current process running in CPU (if it exists)
			current_process = cpu.get_current_cpu_process()
			if(current_process != None):

				# If the process has remaining CPU bursts, add it to the back of the queue
				if(current_process.get_num_bursts() > 0):
						ready_queue.put(current_process)

			if(ready_queue.empty() == False):
				
				# Get the first process on the queue, put it into the CPU
				new_process = ready_queue.get()
				cpu.set_cpu(new_process,time)

				# Decriment number of bursts remaining for process
				new_process.burst_complete()

		time+=1
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


