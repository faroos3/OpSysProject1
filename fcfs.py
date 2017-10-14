## Ready: in the queue
## Running: actively using CPU
## Blocked: Blocked on IO

## Ready Queue -> CPU Burst -> Blocked ----
##	 ^									  |
##	 |								  	  |
##	 |									  |
##   --------------------------------------

##Queue, FIFO
class Queue(object):
	##create new queue
	def __init__(self):
		self.items = []

	##enqueue ADD ITEM TO BACK
	def enqueue(self, item):
		self.items.append(item)

	##dequeue remove front
	def dequeue(self):
		# print(self.items[0])
		return self.items.pop(0)

	##isEmpty
	def isEmpty(self):
		return self.items == []

	##size
	def size(self):
		return len(self.items)

##Contains info for each process
class Process(object):

	def __init__(self,process_id,arrival_t,cpu_t,num_bursts,io_t):
		self.process_id = process_id;
		self.arrival_t = arrival_t
		self.cpu_t = cpu_t
		self.num_bursts = num_bursts
		self.io_t = io_t
		
		##Start and End times of CPU burst
		self.cpu_start = 0
		self.cpu_end = 0

	def get_process_id(self):
		return self.process_id

	def get_arrival_t(self):
		return self.arrival_t

	def get_cpu_t(self):
		return self.cpu_t

	def get_num_bursts(self):
		return self.num_bursts

	def get_io_t(self):
		return self.io_t

	#Start time of cpu burst
	def set_cpu_start(self,start_t):
		self.cpu_start = start_t

	#End time of cpu burst
	def set_cpu_start(self,end_t):
		self.cpu_end = end_t

	def __str__(self):
		return self.process_id

##Keeps track of processes in CPU burst
class CPU_Burst(object):
	def __init__(self):
		self.process_running = None
		self.start_t = None
		self.total_time = -1

	##Time t
	def ready(self,t):
		self.total_time += 1
		##No process in cpu
		if(self.process_running == None):
			return True
		##Process in queue is finished, set queue to idle
		if(self.total_time == (self.start_t + self.process_running.get_cpu_t())):
			print('Process: {} Start Time: {} Total Time: {}'.format(self.process_running, self.start_t, self.total_time))
			self.process_running = None
			return True
		return False

	##Add new process to queue
	def set_cpu(self,process,start_t):
		self.process_running = process
		self.start_t = start_t

def fcfs(process_list):
	t_cs = 8
	##Time
	i=0
	ready_queue = Queue()
	##Nothing on CPU to begin with
	cpu = CPU_Burst()
	while(i<5000):
		for j in process_list:
			##If new process arrives, add to queue
			if(i == j.get_arrival_t()):
				ready_queue.enqueue(j)
		##If CPU is ready for new process take first one from queue
		if(cpu.ready(i)):
			if(ready_queue.isEmpty() == False):
				cpu.set_cpu(ready_queue.dequeue(),i)
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

