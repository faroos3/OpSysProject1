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
	completed_processes = []
	context = avg_wait = avg_turn = avg_burst = preemption = 0

	print("time {}ms: Simulator started for FCFS {}".format(i,ready_queue))

	# Nothing on CPU to begin with
	cpu = CPU_Burst()
	context_switch = False

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
					context+=1
					i += 4
				
			if((processes_complete == len(process_list))):
				print("time {}ms: Simulator ended for FCFS".format(i))
				break
				# Number of processes

		for j in process_list:
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
				j.setAdded(True)
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
				i += 4
				context+=1

				##Put it into the CPU
				cpu.set_cpu(new_process,i,None)

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

	# Calulate stats
	for process in completed_processes:
		avg_wait+=process.get_wait_time()
		avg_burst+=process.get_cpu_t()
		avg_turn+=process.get_wait_time()+process.get_cpu_t()
	
	return [float(avg_burst),float(avg_wait),float(avg_turn),context,preemption] 

def rr(process_list):
	##Time
	i=0
	counter = 0
	t_slice = 70
	processes_complete = 0
	ready_queue = Queue()
	preemption = num_cs = 0 # where the STATS are going to be initialized. 
	print("time {}ms: Simulator started for RR {}".format(i,ready_queue))

	##Nothing on CPU to begin with
	cpu = CPU_Burst()

	context_switch = False
	while(1):
		counter = i
		if((cpu.ready_rr(i) == 0) or (cpu.ready_rr(i) == 1) or (cpu.ready_rr(i) == 2)):
			##Get current process running in CPU (if it exists)
			current_process = cpu.get_current_cpu_process()
			if(current_process != None):
				if((current_process.get_num_bursts() == 0) and (cpu.ready_rr(i) == 2)):
					print("time {}ms: Process {} terminated {}".format(counter,current_process,ready_queue))
					processes_complete += 1
					context_switch = True
					counter+= 4
				elif(cpu.ready_rr(i) == 1):
					##if it was preempted by timeslice
					if(not ready_queue.isEmpty()):
						new_time = current_process.get_cpu_t() - t_slice
						print(("time {:d}ms: Time slice expired; process {} preempted with {:d}ms to go {}").format(counter, current_process, new_time, ready_queue))
						cpu.set_cpu(None,None,None)
						print(("time {:d}ms: Time slice expired; process {} preempted with {:d}ms to go {}").format(i, current_process, new_time, ready_queue))
						#!
						preemption += 1
						current_process.set_cpu_t(new_time)
						ready_queue.enqueue(current_process)
						context_switch = True
						counter+= 4
					else:
						new_time = current_process.get_cpu_t() - t_slice
						print(("time {:d}ms: Time slice expired; no preemption because ready queue is empty {}").format(counter,ready_queue))
						current_process.set_cpu_t(new_time)
						cpu.set_cpu(current_process,i,t_slice)
						i+=1
						counter+=1
						continue
				else:
					if(current_process.get_num_bursts()>1):
						print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(counter,current_process,current_process.get_num_bursts(),ready_queue))
					else:
						print("time {}ms: Process {} completed a CPU burst; {} burst to go {}".format(counter,current_process,current_process.get_num_bursts(),ready_queue))
					##Process with I/O time plus context switch
					##Modify arrival time to account for I/O plus context switch
					current_process.set_cpu_t(current_process.get_cpu_t0())
					i_o_t = counter + 4 + current_process.get_io_t()
					print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(counter,current_process,i_o_t,ready_queue))
					current_process.set_arrival_t(i_o_t)
					cpu.set_cpu(None,None,None)
					context_switch = True
					counter+= 4

			if((processes_complete == len(process_list))):
				print("time {}ms: Simulator ended for RR".format(counter))
				break
		for j in process_list:

			##First time seen
			if(i == j.get_arrival_t0()):
				ready_queue.enqueue(j)
				print("time {}ms: Process {} arrived and added to ready queue {}".format(i,j,ready_queue))
			# ##Any other time
			elif(i == j.get_arrival_t()):
				ready_queue.enqueue(j)
				print("time {}ms: Process {} completed I/O; added to ready queue {}".format(i,j,ready_queue))
		if((cpu.ready_rr(i) == 0) or (cpu.ready_rr(i) == 1) or (cpu.ready_rr(i) == 2)):
			##Queue still has processes
			if(not ready_queue.isEmpty()):
				##Get the first process on the queue
				new_process = ready_queue.dequeue()
				#Context switch
				context_switch = True
				counter += 4
				cpu.set_cpu(new_process,counter,t_slice)

				##Decriment number of bursts remaining for process
				##First slice of a new burst
				if(new_process.get_cpu_t() == new_process.get_cpu_t0()):
					new_process.burst_complete()
					print("time {}ms: Process {} started using the CPU {}".format(counter,new_process,ready_queue))
				else:
					print("time {}ms: Process {} started using the CPU with {}ms remaining {}".format(counter,new_process,new_process.get_cpu_t(),ready_queue))
			else:
				##CPU is idle
				cpu.set_cpu(None,None,None)
		if(not context_switch):
			counter+=1
		else:
			context_switch = False
			num_cs +=1 
		i+=1

		
		# loops to help calculate stats 
		for itr in range(len(process_list)):
			if i > process_list[itr].get_arrival_t0: # meaning it has arrived 
				if process_list[itr] != current_process: # self-explanatory
					if process_list[itr].get_arrival_t() != process_list[itr].get_arrival_t0() and i > process_list[itr].get_arrival_t():
						# I think this last if statement is the case for checking if it's not in IO time? 
						process_list[itr].increase_wait_time()
	# area to calculate and return stats 	
	stats = [num_cs, preemption]
	return 
