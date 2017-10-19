## Ready: in the queue
## Running: actively using CPU
## Blocked: Blocked on IO

## Ready Queue -> CPU Burst -> Blocked ----
##	 ^									  |
##	 |								  	  |
##	 |									  |
##   --------------------------------------

#Queue, FIFO
class Queue(object):
	##create new queue
	def __init__(self):
		self.items = []

	##enqueue ADD ITEM TO BACK
	def enqueue(self, item):
		self.items.append(item)

	##dequeue remove front
	def dequeue(self):
		return self.items.pop(0)

	##isEmpty
	def isEmpty(self):
		return self.items == []

	##size
	def size(self):
		return len(self.items)

	def __str__(self):
		return str(self.items)

#Contains info for each process
class Process(object):

	def __init__(self,process_id,arrival_t,cpu_t,num_bursts,io_t):
		self.process_id = process_id;
		self.arrival_t = arrival_t
		##Initial arrival time
		self.arrival_t0 = arrival_t
		self.cpu_t = cpu_t
		self.num_bursts = num_bursts
		self.io_t = io_t
		self.process_end_t = -1
		self.wait_time = 0

	def get_process_id(self):
		return self.process_id

	def get_arrival_t(self):
		return self.arrival_t

	def get_arrival_t0(self):
		return self.arrival_t0

	def set_arrival_t(self, t):
		self.arrival_t += t

	def get_cpu_t(self):
		return self.cpu_t

	def get_num_bursts(self):
		return self.num_bursts

	def get_io_t(self):
		return self.io_t
	
	def increase_wait_time(self): 
		self.wait_time +=1 

	def set_process_end_t(self,t):
		self.process_end_t = t

	def get_process_end_t(self):
		return self.process_end_t
		
	def get_wait_time(self):
		return self.wait_time

	# Decrease number of bursts by 1
	def burst_complete(self):
		self.num_bursts -= 1

	# Compare processes based on CPU burst time
	def __lt__(self, other):
		return self.get_cpu_t() < other.get_cpu_t()

	def __str__(self):
		return self.process_id

	def __repr__(self):
		return str(self)
		

#Keeps track of processes in CPU burst
class CPU_Burst(object):
	def __init__(self):
		self.process_running = None
		self.start_t = None
		self.total_time = -1

	##Time t
	def ready(self,t):
		self.total_time += 1
		# No process in cpu
		if(self.process_running == None):
			return True
		# Process in queue is finished, set queue to idle
		if(self.total_time == (self.start_t + self.process_running.get_cpu_t())):
			return True
		return False

	##Add new process to queue
	def set_cpu(self,process,start_t):
		self.process_running = process
		self.start_t = start_t

	def get_current_cpu_process(self):
		return self.process_running

###io burst

def fcfs(process_list):
	##Time
	i=0
	ready_queue = Queue()

	print("time {}ms: Simulator started for FCFS [Q {}]".format(i,ready_queue))

	##Nothing on CPU to begin with
	cpu = CPU_Burst()
	while(1):
		##Number of processes
		processes_complete = 0

		for j in process_list:

			##First time seen
			if(i == j.get_arrival_t0()):
				ready_queue.enqueue(j)
				print("time {}ms: Process {} arrived and added to ready queue [Q {}]".format(i,j,ready_queue))
			##Any other time
			elif(i == j.get_arrival_t() and j.get_num_bursts()>0):
				ready_queue.enqueue(j)

			##If a processes has finished all of its bursts mark it as complete
			if(j.get_num_bursts() == 0):
				processes_complete += 1
		##If CPU is ready to accept a process
		if(cpu.ready(i)):
			##Get current process running in CPU (if it exists)
			current_process = cpu.get_current_cpu_process()
			if(current_process != None):
				print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]".format(i,current_process,current_process.get_num_bursts(),ready_queue))
				##Process with I/O time plus context switch
				##Modify arrival time to account for I/O plus context switch
				i_o_t = i + 4 + current_process.get_io_t()
				current_process.set_arrival_t(i_o_t)
				print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]".format(i,current_process,i_o_t,ready_queue))
				if(current_process.get_num_bursts() == 0):
					print("time {}ms: Process {} terminated [Q {}]".format(i,current_process,ready_queue))
			if((processes_complete == len(process_list))):
				print("time {}ms: Simulation ended for FCFS".format(i,current_process,i_o_t,ready_queue))
				break
			##Queue still has processes
			if(ready_queue.isEmpty() == False):
				##Get the first process on the queue
				new_process = ready_queue.dequeue()
				##Put it into the CPU
				cpu.set_cpu(new_process,i)
				print("time {}ms: Process {} started using the CPU [Q {}]".format(i,new_process,ready_queue))
				##Decriment number of bursts remaining for process
				new_process.burst_complete()
			else:
				##CPU is idle
				cpu.set_cpu(None,None)
		i+=1


def main():
	#A|0|168|5|287
	#B|0|385|1|0
	#C|190|97|5|2499
	#D|250|1770|2|822
	process_list = list([Process('A',0,168,5,287),Process('B',0,385,1,0),Process('C',190,97,5,2499), Process('D',250,1770,2,822)])
	fcfs(process_list)

	##Number of processes to simulate
	n = 0

	##Time to perform context_switch (ms)
	t_cs = 8
	

if __name__ == '__main__':
	main()

