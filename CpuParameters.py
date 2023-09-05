class CpuUtilizationChild:
	prev_iteration_data = [];
	prev_interrupt = 0;
	prev_context_switch = 0;
	previous_available_memory = 0;
	
	cpu_y_axis = [];
	memory_y_axis = [];
#	cpu_x_axis = [];

	number_of_interrupt = 0
	number_of_ctxt_switch = 0

	def getPreviousIterationData(self):
		return self.prev_iteration_data;
	def getPreviousInterrupts(self):
		return self.prev_interrupt;
	def getPreviousContextSwitch(self):
		return self.prev_context_switch;
	def getPreviousAvailableMemory(self):
		return self.previous_available_memory;
		
#	def setPreviousIterationData(self, currentValue):
#		self.prev_iteration_data = currentValue;
#	def setPreviousInterrupts(self, currentValue):
#		self.prev_interrupt = currentValue;
#	def setPreviousContextSwitch(self, currentValue):
#		self.prev_context_switch = currentValue;
#	def setPreviousAvailableMemory(self, currentValue):
#		self.previous_available_memory = currentValue;
		
	
	

