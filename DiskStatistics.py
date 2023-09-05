import time
import math
import os
from DiskParameters import DiskUtilizationChild;
class DiskStatistics(DiskUtilizationChild):
	diskOutputList = [];
	def calculatingDiskStatisticsInIntervals(self, wall):

		# reading the /proc/stat file
		lines = open("/proc/diskstats").readlines()
		curr_disk_iteration_data = []
		for line in lines:
			if "sda" in line:
				row = line.split();
				
				#fetching all row starting with the cpu
				row_data = [row[2], row[3], row[5], row[7], row[9]];
				curr_disk_iteration_data.append(row_data);

		self.readIt = True;
		self.diskOutputList = [];
		self.diskOutputList.append(["Device\nname", "disk\nread", "Sector\nread", "Disk\nwrite", "Sector\nwrite"])
			
		self.tempDataDiskRead = [];
		self.tempDataSectorRead = [];
		self.tempDataDiskWrite = [];
		self.tempDataSectorWrite = [];
		if len(self.io_y_axis) > 0:
			self.tempDataSectorWrite = self.io_y_axis.pop(3);
			self.tempDataDiskWrite = self.io_y_axis.pop(2);
			self.tempDataSectorRead = self.io_y_axis.pop(1);
			self.tempDataDiskRead = self.io_y_axis.pop(0);
			
		self.readIt = True;
		
		for row_index in range(len(curr_disk_iteration_data)):
			
			#calculating the delta for user_mode, system_mode, idle_mode
			if len(self.getDiskPreviousIterationData()) != 0:
				disks_read_delta = int(curr_disk_iteration_data[row_index][1]) - int(self.getDiskPreviousIterationData()[row_index][1])
				sector_read_delta = int(curr_disk_iteration_data[row_index][2]) - int(self.getDiskPreviousIterationData()[row_index][2])
				disks_write_delta = int(curr_disk_iteration_data[row_index][3]) - int(self.getDiskPreviousIterationData()[row_index][3])
				sector_write_delta = int(curr_disk_iteration_data[row_index][4]) - int(self.getDiskPreviousIterationData()[row_index][4])
			else:
				disks_read_delta = int(curr_disk_iteration_data[row_index][1])
				sector_read_delta = int(curr_disk_iteration_data[row_index][2])
				disks_write_delta = int(curr_disk_iteration_data[row_index][3]);
				sector_write_delta = int(curr_disk_iteration_data[row_index][4]);
				
			#calculating the user_mode and system_mode utilization
			average_disk_read = round((disks_read_delta*100)/wall,1);
			average_sector_read = round((sector_read_delta*100)/wall,1);			
			average_disk_write = round((disks_write_delta*100)/wall,1);
			average_sector_write = round((sector_write_delta*100)/wall,1);
			
			if self.readIt == True:
				self.tempDataDiskRead.append(average_disk_read);
				self.tempDataSectorRead.append(average_sector_read);
				self.tempDataDiskWrite.append(average_disk_write);
				self.tempDataSectorWrite.append(average_sector_write);
				self.io_y_axis.extend((self.tempDataDiskRead, self.tempDataSectorRead, self.tempDataDiskWrite, self.tempDataSectorWrite));			
				self.readIt = False;

			listData = [curr_disk_iteration_data[row_index][0], average_disk_read, average_sector_read, average_disk_write, average_sector_write];
			self.diskOutputList.append(listData);
		
		#assigning the current cpu usage and number of interrupts & context switch to the previous variable.
		self.prev_disk_iteration_data = curr_disk_iteration_data;		

