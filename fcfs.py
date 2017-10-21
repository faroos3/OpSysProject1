## Ready: in the queue
## Running: actively using CPU
## Blocked: Blocked on IO
from heapq import heappush, heappop

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
		if (len(self.items)) == 0:
			return "[Q <empty>]"
		else: 
			meh = "" 
			meh += "[Q "
			for i in self.items:
				meh += i.get_process_id() + ' '
			meh = meh.rstrip()
			meh += ']'
			return meh

#Contains info for each process
class Process(object):

	def __init__(self,process_id,arrival_t,cpu_t,num_bursts,io_t):
		self.process_id = process_id;
		self.arrival_t = arrival_t
		# Initial arrival time
		self.arrival_t0 = arrival_t
		self.end_t = 0
		self.cpu_t = cpu_t
		# Initial cpu burst time
		self.cpu_t0 = cpu_t
		self.num_bursts = num_bursts
		self.io_t = io_t
		self.process_end_t = -1
		self.wait_time = 0
		self.added = False

	def get_process_id(self):
		return self.process_id

	def get_arrival_t(self):
		return self.arrival_t

	def get_arrival_t0(self):
		return self.arrival_t0

	def get_end_t(self):
		return self.end_t

	def set_arrival_t(self, t):
		self.arrival_t = t

	def set_end_t(self, t):
		self.end_t = t

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

	def set_cpu_t(self,t):
		self.cpu_t = t

	def get_cpu_t0(self):
		return self.cpu_t0


	def wasAdded(self):
		return self.added

	def setAdded(self,boolean):
		self.added = boolean

	# Compare processes based on CPU burst time
	def __lt__(self, other):
		return self.get_process_id() < other.get_process_id()

	def __str__(self):
		return self.process_id

	def __repr__(self):
		return str(self)
		

#Keeps track of processes in CPU burst
class CPU_Burst(object):
	def __init__(self):
		self.process_running = None
		self.start_t = None
		self.t_slice = None

	##Time t
	def ready(self,t):
		# No process in cpu
		if(self.process_running == None):
			return True
		# Process in queue is finished, set queue to idle
		if(t == (self.start_t + self.process_running.get_cpu_t())):
			return True
		return False

	##Time t
	def ready_rr(self,t):
		# No process in cpu
		if(self.process_running == None):
			return 0
		if((t == self.start_t + self.t_slice) and (t != (self.start_t + self.process_running.get_cpu_t()))):
			return 1
		# Process in queue is finished, set queue to idle
		if(t == (self.start_t + self.process_running.get_cpu_t())):
			return 2
		return 3

	##Add new process to queue
	def set_cpu(self,process,start_t,t_slice):
		self.process_running = process
		self.start_t = start_t
		self.t_slice = t_slice

	def get_current_cpu_process(self):
		return self.process_running

# io burst

def fcfs(process_list):
	# Time
	i=0
	ready_queue = Queue()
	processes_complete = 0
	added = False
	context = avg_turn = avg_burst = preemption = 0

	print("time {}ms: Simulator started for FCFS {}".format(i,ready_queue))

	# Nothing on CPU to begin with
	cpu = CPU_Burst()
	context_switch = False

	###Avg Burst Time
	total_burst_time = total_num_bursts = 0
	for process in process_list:
		total_burst_time+= process.get_num_bursts() * process.get_cpu_t0()
		total_num_bursts+= process.get_num_bursts()
	avg_burst = total_burst_time/total_num_bursts


	###Total wait Time
	wait_time=0
	wait_with_context=0

	###Total number of context switches
	total_context = 0

	while(1):
		# If CPU is ready to accept a process
		if(cpu.ready(i)):
			# Get current process running in CPU (if it exists)
			current_process = cpu.get_current_cpu_process()
			if(current_process != None):
				if(current_process.get_num_bursts() == 0):
					print("time {}ms: Process {} terminated {}".format(i,current_process,ready_queue))
					processes_complete += 1
					context_switch = True
					context+=1
					i += 4
				else:
					if(current_process.get_num_bursts()>1):
						print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(i,current_process,current_process.get_num_bursts(),ready_queue))
					else:
						print("time {}ms: Process {} completed a CPU burst; {} burst to go {}".format(i,current_process,current_process.get_num_bursts(),ready_queue))
					# Process with I/O time plus context switch
					# Modify arrival time to account for I/O plus context switch
					i_o_t = i + 4 + current_process.get_io_t()
					print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(i,current_process,i_o_t,ready_queue))
					current_process.set_arrival_t(i_o_t)
					context_switch = True
					i += 4
				
			if((processes_complete == len(process_list))):
				print("time {}ms: Simulator ended for FCFS".format(i))
				break
				# Number of processes

		for j in process_list:
			##Time added to ready queue
			# Any other time
			if(i == j.get_arrival_t() and j.get_arrival_t() != j.get_arrival_t0()):
				ready_queue.enqueue(j)
				print("time {}ms: Process {} completed I/O; added to ready queue {}".format(i,j,ready_queue))
			elif(context_switch and ((i-4) == j.get_arrival_t() and j.get_arrival_t() != j.get_arrival_t0())):
				ready_queue.enqueue(j)
				print("time {}ms: Process {} completed I/O; added to ready queue {}".format(i-4,j,ready_queue))
						# First time seen
			elif(i == j.get_arrival_t0()):
				ready_queue.enqueue(j)
				print("time {}ms: Process {} arrived and added to ready queue {}".format(i,j,ready_queue))
			elif(context_switch and ((i-4) == j.get_arrival_t0())):
				ready_queue.enqueue(j)
				print("time {}ms: Process {} completed I/O; added to ready queue {}".format(i-4,j,ready_queue))
		# If CPU is ready to accept a process
		if(cpu.ready(i) or (cpu.ready(i-4) and context_switch)):
			# Queue still has processes
			if(ready_queue.isEmpty() == False):
				##Get the first process on the queue
				new_process = ready_queue.dequeue()

				#Context switch
				context_switch = True
				total_context+= 1
				i += 4

				##Put it into the CPU
				cpu.set_cpu(new_process,i,None)

				wait_time+= i - new_process.get_arrival_t()-4
				wait_with_context+= i - new_process.get_arrival_t()+4
				print("time {}ms: Process {} started using the CPU {}".format(i,new_process,ready_queue))
				##Decriment number of bursts remaining for process
				new_process.burst_complete()
				
			else:
				##CPU is idle
				cpu.set_cpu(None,None,None)

		if(context_switch != True):
			i+=1
		else:
			context_switch = False


	avg_wait_time = wait_time/total_num_bursts
	avg_wait_with_context = wait_with_context/total_num_bursts
	avg_turnaround_time = avg_wait_with_context + avg_burst

	return [float(avg_burst),float(avg_wait_time),float(avg_turnaround_time),float(total_context),0]
