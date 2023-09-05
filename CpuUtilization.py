import time
import math
import os
import subprocess
import multiprocessing
from CpuParameters import CpuUtilizationChild;

class CpuUtilization(CpuUtilizationChild):
	wall_time = None;
	cpuOutputList = [];
	memoryOutputList = [];
	def calculatingCPUStatisticsInIntervals(self):
		
		self.wall_time = None;
		# reading the /proc/stat file
		lines = open("/proc/stat").readlines()
		curr_iteration_data = []
		cpuCount = multiprocessing.cpu_count()
		for line in lines:
			if cpuCount > -1:
				row = line.split();
				row_data = [row[0], row[1], row[3], row[4]]
				curr_iteration_data.append(row_data);
				cpuCount-=1;
			else:
				break;

		#fetching row with the interrupt information
		p=subprocess.Popen("cat /proc/stat|grep intr", stdout=subprocess.PIPE,shell=True)
		(interrupts, err) = p.communicate()
		curr_interrupt = int(interrupts.split()[1])

		#fetching the context switch information
		p=subprocess.Popen("cat /proc/stat|grep ctxt", stdout=subprocess.PIPE,shell=True)
		(ctswitch, err) = p.communicate()
		curr_context_switch = int(ctswitch.split()[1])

		self.readIt = True;
		self.cpuOutputList = [];
		self.cpuOutputList.append(["CPU\nname", "User\nmode(%)", "System\nmode(%)", "Total(%)"])
		for row_index in range(len(curr_iteration_data)):
			
			#calculating the delta for user_mode, system_mode, idle_mode
			user_mode_delta = int(curr_iteration_data[row_index][1])
			system_mode_delta = int(curr_iteration_data[row_index][2])
			idle_mode_delta = int(curr_iteration_data[row_index][3]);

			if len(self.getPreviousIterationData()) != 0:
				user_mode_delta -= int(self.getPreviousIterationData()[row_index][1])
				system_mode_delta -= int(self.getPreviousIterationData()[row_index][2])
				idle_mode_delta -= int(self.getPreviousIterationData()[row_index][3])
				
			#calculating the wall_time
			if self.wall_time == None:
				self.calculateWallTime(user_mode_delta, system_mode_delta, idle_mode_delta);
			walltime = self.getWallTime();
				
			
			#calculating the user_mode and system_mode utilization
			user_mode_utilization = round((user_mode_delta*100)/walltime, 1);
			system_mode_utilization = round((system_mode_delta*100)/walltime, 1);			
			
			total_utilization = round((user_mode_utilization + system_mode_utilization));
			
			if self.readIt == True:
				self.cpu_y_axis.append(total_utilization);
#				self.cpu_x_axis.append(time.strftime("%H:%M:%S"));
				self.readIt = False;

			self.cpuOutputList.append([curr_iteration_data[row_index][0], user_mode_utilization, system_mode_utilization, total_utilization]);
		
		#calculating the interrupts and context_switch delta
		interrupt_delta = int(curr_interrupt) - int(self.getPreviousInterrupts());
		context_switch_delta = int(curr_context_switch) - int(self.getPreviousContextSwitch());
		
		#calculating the number of interrupts and the context_switch
		lines = open("/proc/meminfo").readlines()
		for line in lines:
			row = line.split(":");
			if row[0].strip() == "MemTotal":
				total_memory = math.floor((int)(row[1].strip().split(" ")[0])/1024);
			elif row[0].strip() == "MemAvailable":
				curr_available_memory = math.floor((math.floor((int)(row[1].strip().split(" ")[0])/1024) + self.getPreviousAvailableMemory())/2);
				break;
		self.memoryOutputList = [];
		self.memoryOutputList.append(["Available\n(MB)", "Total\n(MB)", "Utilization\n(%)"])
		utilization = round((total_memory - curr_available_memory)*100/total_memory,2);
		self.memoryOutputList.append([curr_available_memory, total_memory, utilization]);
		self.memory_y_axis.append(utilization);

		#assigning the current cpu usage and number of interrupts & context switch to the previous variable.
		self.number_of_interrupt = math.floor(interrupt_delta * 100/walltime);
		self.number_of_ctxt_switch = math.floor(context_switch_delta * 100/walltime);
		self.prev_iteration_data = curr_iteration_data;
		self.prev_interrupt = curr_interrupt;
		self.prev_context_switch = curr_context_switch;
		self.previous_available_memory = curr_available_memory;
	
	def calculateWallTime(self, user_mode, system_mode, idle_mode):
		self.wall_time = user_mode + system_mode + idle_mode;
	
	def getWallTime(self):
		return self.wall_time;
		

