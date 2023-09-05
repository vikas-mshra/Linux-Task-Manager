import pwd
import os
import subprocess
import socket
from NetworkStatisticsParameters import NetworkUtilizationChild;
class NetworkStatistics(NetworkUtilizationChild):
	tcpNetworkOutputList = [];
	udpNetworkOutputList = [];
	tcpActiveConnection = "";
	tcpEstablishedConnection = "";
	networkOutputList = [];
	def calculatingNetworkStatisticsInIntervals(self, walltime):
		self.tcpNetworkOutputList = [];
		# reading the /proc/stat file
		lines = open("/proc/net/tcp").readlines()
		
		listOfProcess = subprocess.Popen("ls -t /proc | grep '^[0-9]'", stdout=subprocess.PIPE,shell=True)
		(output, err) = listOfProcess.communicate();
		numberOfProcesses = output.split();
		for line in lines:		
			row = line.split();
			if row[0][0:1].isdigit():
#				print(row[1][9:]);

				inode = row[9];
				for pid in numberOfProcesses:
					try:
						fd = subprocess.run(['grep','socket'], capture_output=True, input=subprocess.run(['ls','-l','/proc/' + bytes.decode(pid) + '/fd'], capture_output=True).stdout);

						if inode in str(fd.stdout):
							processName = str(open("/proc/" + bytes.decode(pid) + "/stat").readlines()).split()[1][1:-1];
							break;
					except FileNotFoundError:
						continue;
				hexSourceIP = row[1][:8];
				decSourceIP = "%i.%i.%i.%i"%(int(hexSourceIP[0:2],16),int(hexSourceIP[2:4],16),int(hexSourceIP[4:6],16),int(hexSourceIP[6:8],16))

				hexDestIP = row[2][:8];
				decDestIP = "%i.%i.%i.%i"%(int(hexDestIP[0:2],16),int(hexDestIP[2:4],16),int(hexDestIP[4:6],16),int(hexDestIP[6:8],16))
				uname = pwd.getpwuid(int(row[7]))[0]
				try:
					decSourceIP = socket.gethostbyaddr(decSourceIP)[0];
				except socket.herror:
					pass;
				try:
					decDestIP = socket.gethostbyaddr(decDestIP)[0];
				except socket.herror:
					pass;

				self.tcpNetworkOutputList.append([uname, processName, decSourceIP, int(row[1][9:],16), decDestIP, int(row[2][9:],16)]);

		self.udpNetworkOutputList = [];
		# reading the /proc/stat file
		lines = open("/proc/net/udp").readlines()
		for line in lines:
			row = line.split();
			if row[0][0:1].isdigit():
				inode = row[9];
				for pid in numberOfProcesses:
					try:
						fd = subprocess.run(['grep','socket'], capture_output=True, input=subprocess.run(['ls','-l','/proc/' + bytes.decode(pid) + '/fd'], capture_output=True).stdout);


						if inode in str(fd.stdout):
							processName = str(open("/proc/" + bytes.decode(pid) + "/stat").readlines()).split()[1][1:-1];
							break;
					except FileNotFoundError:
						continue;
				hexSourceIP = row[1][:8];
				decSourceIP = "%i.%i.%i.%i"%(int(hexSourceIP[0:2],16),int(hexSourceIP[2:4],16),int(hexSourceIP[4:6],16),int(hexSourceIP[6:8],16))

				hexDestIP = row[2][:8];
				decDestIP = "%i.%i.%i.%i"%(int(hexDestIP[0:2],16),int(hexDestIP[2:4],16),int(hexDestIP[4:6],16),int(hexDestIP[6:8],16))
				uname = pwd.getpwuid(int(row[7]))[0]
				try:
					decSourceIP = socket.gethostbyaddr(decSourceIP)[0];
				except socket.herror:
					pass;
				try:
					decDestIP = socket.gethostbyaddr(decDestIP)[0];
				except socket.herror:
					pass;

				self.udpNetworkOutputList.append([uname, processName, decSourceIP, int(row[1][9:],16), decDestIP, int(row[2][9:],16)]);
		
		process = subprocess.Popen("cat /proc/net/snmp|grep Tcp", stdout=subprocess.PIPE,shell=True)
		(lines, err) = process.communicate()
		row = lines.split();
		self.tcpActiveConnection = row[21];
		self.tcpEstablishedConnection = row[25];
		
		#calculating network utilization
		
		
		lines = open("/proc/net/dev").readlines()
		curr_iteration_data = [];
		for line in lines:
			row = line.split();
			if ":" in row[0] and "lo" not in row[0]:
				readBytes = float(row[1])
				transmitBytes = float(row[9])
				process = subprocess.Popen("sudo ethtool enp0s3|grep -i speed", stdout=subprocess.PIPE,shell=True)
				(output, err) = process.communicate();
				speed = bytes.decode(output.split()[1][:-4])
				curr_iteration_data.append([row[0][:-1], readBytes, transmitBytes, speed])

		self.networkOutputList = [];
		self.networkOutputList.append(["Name", "Utilization(%)"])
		for row_index in range(len(curr_iteration_data)):
			
			#calculating the delta for user_mode, system_mode, idle_mode
			read_bytes_delta = float(curr_iteration_data[row_index][1])
			transmit_bytes_delta = float(curr_iteration_data[row_index][2])

			if len(self.getPreviousIterationData()) != 0:
				read_bytes_delta -= float(self.getPreviousIterationData()[row_index][1])
				transmit_bytes_delta -= float(self.getPreviousIterationData()[row_index][2])

			total_bytes = read_bytes_delta + transmit_bytes_delta;
			
			#calculating utilization
			utilization = total_bytes*.01/(walltime * float(curr_iteration_data[row_index][3]));
			self.networkOutputList.append([curr_iteration_data[row_index][0], round(utilization,2)]);
		
			
		self.prev_network_iteration_data = curr_iteration_data;
	
