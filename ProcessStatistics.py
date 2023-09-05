import pwd
import os
import subprocess
from ProcessStatisticsParameters import ProcessUtilizationChild;
class ProcessStatistics(ProcessUtilizationChild):
	processOutputList = [];
	def fetchProcessesInInterval(self, walltime):

		process = subprocess.Popen("ls /proc | grep '^[0-9]'", stdout=subprocess.PIPE,shell=True)
		(output, err) = process.communicate();
		numberOfProcesses = output.split();

		curr_iteration_data = {};
		for pid in numberOfProcesses:
			try:
				processId = bytes.decode(pid);
				processDescription = str(open("/proc/" + processId + "/stat").readlines()).split();
				
				#fetching the process name
				processName = processDescription[1][1:-1]

				#fetching the userName for the process
				userName = "";
				lines = open("/proc/" + processId + "/environ").readlines()
				line = str(lines).split("USER=");
				if len(line) > 1:
					userName = line[1].split("\\x00")[0];
				
				#fetching other description
				userMode = processDescription[13];
				sysMode = processDescription[14];
				virtualMemory = processDescription[22];

				physicalMemory = bytes.decode(subprocess.check_output("cat /proc/" + processId + "/smaps | grep Rss | awk '{print $2}' | awk '{s+=$1} END {printf s}'", shell=True));
				curr_iteration_data[processId] = [processName, userName, userMode, sysMode, virtualMemory, physicalMemory, processId];
				self.processOutputList.append([processName, userName, userMode, sysMode, virtualMemory, physicalMemory]);
				
			except FileNotFoundError:
				continue;

		if len(curr_iteration_data) > 0:
			key_list = list(curr_iteration_data.keys());

			self.processOutputList = [];
			for key in key_list:				
				#calculating the delta for user_mode, system_mode, idle_mode

				user_mode_delta = float(curr_iteration_data.get(key)[2]);
				sys_mode_delta = float(curr_iteration_data.get(key)[3]);

				if not self.getPreviousIterationProcessData().get(key) == None:
					user_mode_delta -= float(self.getPreviousIterationProcessData().get(key)[2]);
					sys_mode_delta -= float(self.getPreviousIterationProcessData().get(key)[3]);
				
				#calculating utilization
				user_mode_utilization = round(user_mode_delta*100/float(walltime),1);
				sys_mode_utilization = round(sys_mode_delta*100/float(walltime),1);

				self.processOutputList.append([curr_iteration_data.get(key)[0], curr_iteration_data.get(key)[1], user_mode_utilization, sys_mode_utilization, curr_iteration_data.get(key)[4], curr_iteration_data.get(key)[5]]);

		self.prev_process_iteration_data = curr_iteration_data;
