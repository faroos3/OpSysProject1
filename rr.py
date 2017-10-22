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
		self.final_end_time = 0
	def set_final_end_time(self, time):
		self.final_end_time = time
	def get_final_end_time(self):
		return self.final_end_time

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

def rr(process_list):
	##Time
	i=0
	original_bursts = [process.get_num_bursts() for process in process_list]
	total_bursts = sum(original_bursts)
	# 
	total_burst_time = total_num_bursts = 0
	for process in process_list:
		total_burst_time+= process.get_num_bursts() * process.get_cpu_t0()
		total_num_bursts+= process.get_num_bursts()
	wait_time = wait_with_context=avg_burst = total_burst_time/total_num_bursts
	# 
	##This will be used to "block" anything from executing on the cpu
	## when a context_switch has been initiated
	##This was needed because suppose process A finishes a timeslice at time t=0, triggering a context_switch 
	## In the original simulation, i would increment by 4, skipping over any process that arrives
	## between t=0 and t=4
	##To solve this problem i will increment by 1 each time and the counter will be used to adjust cpu
	## start times and i/o times where applicable
	counter = 0
	t_slice = 70
	##When the number of processes complete is equal to that of the number of processes
	##we can break (assuming the last process on the cpu is done (i.e. cpu is ready)))
	processes_complete = 0
	ready_queue = Queue()
	avg_wait = avg_turn = avg_cpu = preemption = num_cs = 0 # where the STATS are going to be initialized. 
	print("time {}ms: Simulator started for RR {}".format(i,ready_queue))
	##Nothing on CPU to begin with
	cpu = CPU_Burst()
	# Calculate some stats we can here 
	temp = 0 
	# for process in process_list: 
		# avg_cpu += process.get_cpu_t() * process.get_num_bursts()
		# print(avg_cpu)
	# avg_cpu /= len(process_list)
	# end calculating of some stats. 
	
	context_switch = False
	while(1):
		##We want to reset the counter to i each time, because when there is a context switch
		##i is being incremented by 4
		counter = i
		if((cpu.ready_rr(i) == 0) or (cpu.ready_rr(i) == 1) or (cpu.ready_rr(i) == 2)):
			##Get current process running in CPU (if it exists)
			current_process = cpu.get_current_cpu_process()
			if(current_process != None):
				##Process terminated (increment processes_complete) and increment the counter
				## to account for context switch
				if((current_process.get_num_bursts() == 0) and (cpu.ready_rr(i) == 2)):
					print("time {}ms: Process {} terminated {}".format(counter,current_process,ready_queue))
					current_process.set_final_end_time(counter)
					processes_complete += 1
					context_switch = True
					counter+= 4
				elif(cpu.ready_rr(i) == 1):
					##if it was preempted by timeslice
					if(not ready_queue.isEmpty()):
						new_time = current_process.get_cpu_t() - t_slice
						# print(("time {:d}ms: Time slice expired; process {} preempted with {:d}ms to go {}").format(counter, current_process, new_time, ready_queue))
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

			##First time seen (as in it came from process list)
			if(i == j.get_arrival_t0()):
				ready_queue.enqueue(j)
				print("time {}ms: Process {} arrived and added to ready queue {}".format(i,j,ready_queue))
			# ##Any other time (as in it came from)
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
				num_cs += 1
				counter += 4
				wait_time+= counter - new_process.get_arrival_t()-4
				wait_with_context+= counter - new_process.get_arrival_t()+4
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
			# num_cs +=1 
		i+=1

		
		# loops to help calculate stats 
		# for itr in range(len(process_list)):
			# if counter >= process_list[itr].get_arrival_t0(): # meaning it has arrived 
				# if process_list[itr] != current_process: # self-explanatory
					# if process_list[itr].get_arrival_t() != process_list[itr].get_arrival_t0() and counter > process_list[itr].get_arrival_t():
						# # I think this last if statement is the case for checking if it's not in IO time? 
						# process_list[itr].increase_wait_time()
	# area to calculate and return stats 	
	for itr in range(len(process_list)):
		possible_turn = process_list[itr].get_final_end_time() - process_list[itr].get_arrival_t0()
		possible_turn -= original_bursts[itr] * process_list[itr].get_io_t()
		avg_turn += possible_turn
		avg_wait += process_list[itr].get_final_end_time() - process_list[itr].get_arrival_t0() - (num_cs * 4) - (preemption * 8)
	avg_wait /= total_bursts
	#avg_wait = wait_time/total_bursts
	avg_wait_context = wait_with_context/total_bursts
	avg_turn += avg_wait_context + avg_burst
	# 
	return [float(avg_burst),float(avg_wait),float(avg_turn),num_cs,preemption]
