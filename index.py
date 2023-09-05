import copy
import time
from tkinter import ttk
from tkinter import CENTER
from tkinter import LEFT
from tkinter import Y
from tkinter import BOTH
from tkinter import S
from tkinter import RIGHT
from tkinter import TOP
from tkinter import BOTTOM
from tkinter import VERTICAL
from tkinter import StringVar
from tkinter import Tk
from CpuUtilization import CpuUtilization
from DiskStatistics import DiskStatistics
from NetworkStatistics import NetworkStatistics
from ProcessStatistics import ProcessStatistics
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import time

#style.use('fivethirtyeight')
tabOneFig = Figure(figsize = (6, 50), dpi = 100)
tabOneFig.set_figheight(8)
tabOneFig.set_figwidth(15)

# adding the subplot
tabOneGraphOne = tabOneFig.add_subplot(211)
tabOneGraphTwo = tabOneFig.add_subplot(212)

tabTwoFig = Figure(figsize = (6, 50), dpi = 100)
tabTwoFig.set_figheight(8)
tabTwoFig.set_figwidth(13)

# adding the subplot
tabTwoGraphOne = tabTwoFig.add_subplot(211)
tabTwoGraphTwo = tabTwoFig.add_subplot(212)

globalInterval = 2;
globalWallTime = None;

class MainWindow(CpuUtilization, DiskStatistics, NetworkStatistics, ProcessStatistics):
	def __init__(self, master):
		self.master = master;
		self.master.title("Task Manager");
		self.master.minsize(600, 600);
#		self.master.iconbitmap('@/home/vikas-mshra/Downloads/tm.xbm');
		self.createTabs();

	def createStyleForTabs(self):
		self.customed_style = ttk.Style()
		self.customed_style.configure('Custom.TNotebook.Tab', padding=[12, 12], font=('Helvetica', 10))

	def createTabs(self):
		
		self.createStyleForTabs();
		self.tabControl = ttk.Notebook(self.master, style = 'Custom.TNotebook');
		self.tab1 = ttk.Frame(self.tabControl);
		self.tab2 = ttk.Frame(self.tabControl);
		self.tab3 = ttk.Frame(self.tabControl);
		self.tab4 = ttk.Frame(self.tabControl);
		self.tab5 = ttk.Frame(self.tabControl);

		self.tabControl.add(self.tab1, text='System Performance');
		self.tabControl.add(self.tab2, text='Disk I/O');
		self.tabControl.add(self.tab3, text='Network I/O');
		self.tabControl.add(self.tab4, text='Processes');
		self.tabControl.add(self.tab5, text='Keyboard Monitor');

		self.tabControl.pack(expand = 1, fill = 'both');
		self.createFirstTab();
		self.createSecondTab();
		self.createThirdTab();
		self.createFourthTab();
		self.createFifthTab();

	def createFirstTab(self):
		ttk.Label(self.tab1, text="Time interval (in sec): ", font=('Arial',12,'bold')).grid(row=0, columnspan=9, sticky='e');
		
		interval = StringVar();
		interval.set("2");
		ttk.Entry(self.tab1, textvariable=interval, justify = CENTER, width=10).grid(row=0, column=9, sticky='w',padx=5,pady=5);

		self.calculatingCPUStatisticsInIntervals();
		self.globalWallTime = self.getWallTime();

		curr_row = 0;

		total_rows = len(self.cpuOutputList);
		total_columns = len(self.cpuOutputList[0])
		cpuList=[];
		cpuValues={};
		tempHolder=[];
		for i in range(total_rows):
			for j in range(total_columns):	 
				if i == 0:
					ttk.Label(self.tab1, justify = CENTER, text=self.cpuOutputList[i][j], font=('Arial',12,'bold')).grid(row=curr_row+1, column=j);
				elif j==0:
					ttk.Label(self.tab1, text=self.cpuOutputList[i][j], font=('Arial',11)).grid(row=curr_row+1, column=j, padx=2)				
				else:
					cpuValues[i,j] = StringVar()
					ttk.Label(self.tab1, textvariable=cpuValues[i,j], font=('Arial',11)).grid(row=curr_row+1, column=j, padx=2)				
					tempHolder.append(cpuValues[i,j]);
			if len(tempHolder) > 0:
				cpuList.append(copy.copy(tempHolder));
				tempHolder.clear()
			curr_row += 1;
		
		ttk.Label(self.tab1, text="").grid(row=curr_row+1, column=0, columnspan=3, pady = 20, padx = 10, sticky ='w');		
		curr_row += 1;

		total_rows = len(self.memoryOutputList);
		total_columns = len(self.memoryOutputList[1])
		memoryList=[];
		memoryValues={};

		for i in range(total_rows):
			for j in range(total_columns):
				if i == 0:
					ttk.Label(self.tab1, justify=CENTER, text=self.memoryOutputList[i][j], font=('Arial',12,'bold')).grid(row=curr_row+1, column=j)
				else:
					memoryValues[i,j] = StringVar()
					ttk.Label(self.tab1, textvariable=memoryValues[i,j], font=('Arial',11)).grid(row=curr_row+1, column=j, padx=2)
					memoryList.append(memoryValues[i,j]);
			curr_row += 1;

		ttk.Label(self.tab1, text="").grid(row=curr_row+1, column=0, columnspan=3, pady = 20, padx = 10, sticky ='w');		
		curr_row += 1;
			
		ttk.Label(self.tab1, justify=CENTER, text="No. of processes per second", font=('Arial',12,'bold')).grid(row=curr_row+1, column=0, columnspan=3);
		curr_row += 1;
		interruptLabelName = StringVar();
		ttk.Label(self.tab1, justify= CENTER, textvariable=interruptLabelName).grid(row=curr_row+1, column=0, columnspan=3);

		curr_row += 1;
		ttk.Label(self.tab1, justify=CENTER, text="No. of context switch per second", font=('Arial',12,'bold')).grid(row=curr_row+1, column=0, columnspan=3)
		curr_row += 1;
		ctxtLabelName = StringVar();
		ttk.Label(self.tab1, justify= CENTER, textvariable=ctxtLabelName).grid(row=curr_row+1, column=0, columnspan=3);
				
		self.tab1.columnconfigure(4, weight=1)
		canvas = FigureCanvasTkAgg(tabOneFig, master = self.tab1);
		canvas.draw()		
		canvas.get_tk_widget().grid(row=1, rowspan=17, column=5, columnspan=5, sticky='nsew')

		self.firstTabData(cpuList, memoryList, interruptLabelName, ctxtLabelName, interval);
		
	def firstTabData(self, cpuList, memoryList, interruptLabelName, ctxtLabelName, interval):
		if not str(interval.get()).isdigit() or str(interval.get()).strip() == "":
			interval.set("2");
		
		self.globalInterval = int(interval.get());

		self.calculatingCPUStatisticsInIntervals();
		self.globalWallTime = self.getWallTime();

		total_rows = len(self.cpuOutputList);
		total_columns = len(self.cpuOutputList[0])
		
		#from 1st row the cpu table will start
		for i in range(total_rows):
			for j in range(total_columns):	 
				if i != 0 or j != 0:
					cpuList[i-1][j-1].set(self.cpuOutputList[i][j]);
		
		total_rows = len(self.memoryOutputList);
		total_columns = len(self.memoryOutputList[1])

		for i in range(total_rows):
			for j in range(total_columns):
				if i != 0:
					memoryList[j].set(self.memoryOutputList[i][j]);
		
		interruptLabelName.set(self.number_of_interrupt);
		ctxtLabelName.set(self.number_of_ctxt_switch);

		tabOneGraphOne.clear();
 
		# plotting the graph
		tabOneGraphOne.plot(self.cpu_y_axis, label='CPU');
		tabOneGraphOne.set_ylabel("cpu utilization (%)");
		tabOneGraphOne.set_xticklabels([]);
		tabOneGraphOne.set_xticks([]);
		tabOneGraphOne.legend();

		tabOneGraphTwo.clear();
 
		# plotting the graph
		tabOneGraphTwo.plot(self.memory_y_axis, label='Memory');
		tabOneGraphTwo.set_ylabel("memory utilization (%)");
		tabOneGraphTwo.set_xticklabels([]);
		tabOneGraphTwo.set_xticks([]);
		tabOneFig.canvas.draw_idle();		
		tabOneGraphTwo.legend();

		self.tab1.after(int(interval.get())*1000,self.firstTabData, cpuList, memoryList, interruptLabelName, ctxtLabelName, interval);

	def createSecondTab(self):
		self.calculatingDiskStatisticsInIntervals(self.globalWallTime);
		curr_row = 0;
		
		total_rows = len(self.diskOutputList)
		total_columns = len(self.diskOutputList[0])
		ioList=[];
		ioValues={};
		tempHolder=[];
		#from 1st row the cpu table will start
		for i in range(total_rows):
			for j in range(total_columns):	 
				if i == 0:
					ttk.Label(self.tab2, justify = CENTER, text=self.diskOutputList[i][j], font=('Arial',12,'bold')).grid(row=curr_row+1, column=j, padx=10);
				elif j == 0:
					ttk.Label(self.tab2, justify = CENTER, text=self.diskOutputList[i][j], font=('Arial',12)).grid(row=curr_row+1, column=j);
				else:
					ioValues[i,j] = StringVar();
					ttk.Label(self.tab2, justify = CENTER, textvariable=ioValues[i,j], font=('Arial',11)).grid(row=curr_row+1, column=j, padx=5)				
					tempHolder.append(ioValues[i,j]);
			if len(tempHolder) > 0:
				ioList.append(copy.copy(tempHolder));
				tempHolder.clear();
			curr_row +=1;

		self.tab2.columnconfigure(5, weight=1)

		canvas = FigureCanvasTkAgg(tabTwoFig, master = self.tab2);
		canvas.draw()		
		canvas.get_tk_widget().grid(row=1, rowspan=17, column=5, columnspan=5, sticky='nsew')
		self.secondTabData(ioList);
		
	def secondTabData(self, ioList):
		self.calculatingDiskStatisticsInIntervals(self.globalWallTime);
		
		total_rows = len(self.diskOutputList)
		total_columns = len(self.diskOutputList[0])
		
		#from 1st row the cpu table will start
		for i in range(total_rows):
			for j in range(total_columns):	 
				if i != 0 or j != 0:
					ioList[i-1][j-1].set(self.diskOutputList[i][j])

		tabTwoGraphOne.clear(); 
		# plotting the graph
		tabTwoGraphOne.plot(self.io_y_axis[0], label='Disk Read');
		tabTwoGraphOne.plot(self.io_y_axis[2], label='Disk Write');

		tabTwoGraphOne.set_ylabel("Disk statistics(bytes/sec)");
		tabTwoGraphOne.set_xticklabels([]);
		tabTwoGraphOne.set_xticks([]);
		tabTwoGraphOne.legend();

		tabTwoGraphTwo.clear(); 
		# plotting the graph
		tabTwoGraphTwo.plot(self.io_y_axis[1], label='Block Read');
		tabTwoGraphTwo.plot(self.io_y_axis[3], label='Block Write');

		tabTwoGraphTwo.set_ylabel("Block statistics(bytes/sec)");
		tabTwoGraphTwo.set_xticklabels([]);
		tabTwoGraphTwo.set_xticks([]);
		tabTwoGraphTwo.legend();
		
		tabTwoFig.canvas.draw_idle();		

		self.tab2.after(self.globalInterval*1000,self.secondTabData, ioList);
	def createThirdTab(self):
		self.calculatingNetworkStatisticsInIntervals(self.globalWallTime);

		self.leftFrame = ttk.Frame(self.tab3);
		self.leftFrame.pack(side=LEFT, expand=0);
		self.rightFrame = ttk.Frame(self.tab3);
		self.rightFrame.pack(side=RIGHT, expand=1,fill=BOTH);
		
		ttk.Label(self.leftFrame, text="TCP active connection: ", font=('Arial',12,'bold')).grid(row=0,column=0,padx=5,pady=7);
		tcpActiveCon = StringVar();
		ttk.Label(self.leftFrame, textvariable=tcpActiveCon).grid(row=0,column=1,padx=5,pady=7)
		
		ttk.Label(self.leftFrame, text="TCP established connection: ", font=('Arial',12,'bold')).grid(row=1,column=0,padx=5,pady=7)
		tcpEstablishedCon = StringVar();
		ttk.Label(self.leftFrame, textvariable=tcpEstablishedCon).grid(row=1,column=1,padx=5,pady=7)

		ttk.Label(self.leftFrame, text="======================================", font=('Arial',12,'bold')).grid(row=2,columnspan=2,padx=5,pady=15)		
		ttk.Label(self.leftFrame, text="Network Utilization", font=('Arial',12,'bold')).grid(row=3,columnspan=2,padx=5,pady=15)
		ttk.Label(self.leftFrame, text="======================================", font=('Arial',12,'bold')).grid(row=4,columnspan=2,padx=5,pady=15)

		curr_row = 4;
		total_rows = len(self.networkOutputList);
		total_columns = 2
		networkList=[];
		networkValues={};
		tempHolder=[];
		for i in range(total_rows):
			for j in range(total_columns):	 
				if i == 0:
					ttk.Label(self.leftFrame, justify=CENTER, text=self.networkOutputList[i][j], font=('Arial',12,'bold')).grid(row=curr_row+1,column=j)
				elif j==0:
					ttk.Label(self.leftFrame, justify=CENTER, text=self.networkOutputList[i][j], font=('Arial',12)).grid(row=curr_row+1,column=j)
				else:
					networkValues[i,j] = StringVar()
					ttk.Label(self.leftFrame, justify=CENTER, textvariable=networkValues[i,j], font=('Arial',11)).grid(row=curr_row+1, column=j, padx=2)
					tempHolder.append(networkValues[i,j]);
			if len(tempHolder) > 0:
				networkList.append(copy.copy(tempHolder));
				tempHolder.clear()
			curr_row += 1;
		
						
		ttk.Label(self.rightFrame, text="Enter UserName or Connection type", font=('Arial',12,'bold')).pack();
		userInput = StringVar();
		ttk.Entry(self.rightFrame, textvariable=userInput).pack();
		
		self.nettree=ttk.Treeview(self.rightFrame, show="headings",height=20)

		n_vscroll = ttk.Scrollbar(self.rightFrame, orient = VERTICAL, command = self.nettree.yview)
		n_vscroll.pack(fill = Y, side = RIGHT)

		self.nettree['yscrollcommand'] = n_vscroll.set
		
		self.nettree["columns"]=("uname", "connectiontype", "programname", "localadd","localport","remoteadd","remoteport")
		self.nettree.column("uname", anchor=S, width=90)
		self.nettree.column("connectiontype", anchor=S, width=90)
		self.nettree.column("programname", anchor=S, width=90)
		self.nettree.column("localadd", anchor=S, width=150)
		self.nettree.column("localport", anchor=S, width=100)
		self.nettree.column("remoteadd", anchor=S, width=150)
		self.nettree.column("remoteport", anchor=S, width=120)

		self.nettree.heading("uname", text = "Username", anchor=S)
		self.nettree.heading("connectiontype", text = "Connection Type", anchor=S)
		self.nettree.heading("programname", text = "Program Name", anchor=S)
		self.nettree.heading("localadd", text = "Local Address", anchor=S)
		self.nettree.heading("localport", text = "Local Port No.", anchor=S)
		self.nettree.heading("remoteadd", text = "Remote Address", anchor=S)
		self.nettree.heading("remoteport", text = "Remote Port No.", anchor=S)
		
#		self.nettree.grid(row=2, column=1)
		self.nettree.pack(expand = 1, fill = BOTH)
		self.thirdTabData(tcpActiveCon, tcpEstablishedCon, userInput, networkList);
	
	def thirdTabData(self, tcpActiveCon, tcpEstablishedCon, userInput, networkList):
		rowIndex = 0

		#clear treeview before repopulating treeview
		self.nettree.delete(*self.nettree.get_children())

		self.calculatingNetworkStatisticsInIntervals(self.globalWallTime);

		tcpActiveCon.set(self.tcpActiveConnection);
		tcpEstablishedCon.set(self.tcpEstablishedConnection);
		self.input = userInput.get();

		#populate fetched values in treeview
		tcpData = self.tcpNetworkOutputList;
		for row in tcpData:
			if self.input in row[0] or self.input in "tcp":
				self.nettree.insert("",rowIndex, value=(row[0],"tcp",row[1],row[2],row[3],row[4],row[5]))
				rowIndex += 1;
		
		udpData = self.udpNetworkOutputList;
		for row in udpData:
			if self.input in row[0] or self.input in "udp":
				self.nettree.insert("",rowIndex, value=(row[0],"udp",row[1],row[2],row[3],row[4],row[5]))
				rowIndex += 1;
		
		total_rows = len(self.networkOutputList);
		total_columns = len(self.networkOutputList[0]);
		
		#from 1st row the cpu table will start
		for i in range(total_rows):
			for j in range(total_columns):	 
				if i != 0 or j != 0:
					networkList[i-1][j-1].set(self.networkOutputList[i][j]);
		
		self.tab3.after(self.globalInterval*1000, self.thirdTabData, tcpActiveCon, tcpEstablishedCon, userInput, networkList);

	def createFourthTab(self):
		self.fetchProcessesInInterval(self.globalWallTime);

						
		ttk.Label(self.tab4, text="Enter User/Process name", font=('Arial',12,'bold')).pack();
		userInput = StringVar();
		ttk.Entry(self.tab4, textvariable=userInput).pack();
		
		self.proctree=ttk.Treeview(self.tab4, show="headings",height=20)

		n_vscroll = ttk.Scrollbar(self.tab4, orient = VERTICAL, command = self.proctree.yview)
		n_vscroll.pack(fill = Y, side = RIGHT)

		self.proctree['yscrollcommand'] = n_vscroll.set
		
		self.proctree["columns"]=("processName", "userName", "userCPU","systemCPU","virtualMemory","physicalMemory")
		self.proctree.column("processName", anchor=S, width=90)
		self.proctree.column("userName", anchor=S, width=90)
		self.proctree.column("userCPU", anchor=S, width=150)
		self.proctree.column("systemCPU", anchor=S, width=100)
		self.proctree.column("virtualMemory", anchor=S, width=150)
		self.proctree.column("physicalMemory", anchor=S, width=120)

		self.proctree.heading("processName", text = "Process Name", anchor=S)
		self.proctree.heading("userName", text = "User Name", anchor=S)
		self.proctree.heading("userCPU", text = "User Mode Time(%)", anchor=S)
		self.proctree.heading("systemCPU", text = "System Mode Time(%)", anchor=S)
		self.proctree.heading("virtualMemory", text = "Virtual Memory (in bytes)", anchor=S)
		self.proctree.heading("physicalMemory", text = "Physical Memory", anchor=S)
		
		self.proctree.pack(expand = 1, fill = BOTH)
		self.fourthTabData(userInput);
	
	def fourthTabData(self, userInput):
		rowIndex = 0;
		#clear treeview before repopulating treeview
		self.proctree.delete(*self.proctree.get_children())

		self.fetchProcessesInInterval(self.globalWallTime);
		self.input = userInput.get();
		
		processData = self.processOutputList;

		#populate fetched values in treeview
		for row in processData:
			if self.input in row[0] or self.input in row[1]:
				self.proctree.insert("",rowIndex, value=(row[0],row[1],row[2],row[3],row[4], row[5]))
				rowIndex += 1;
				
		self.tab4.after(self.globalInterval*1000, self.fourthTabData, userInput);

	def createFifthTab(self):
		ttk.Label(self.tab5, text="Enter sample text here (Press Enter to see the result or exceed 128 characters)", font=('Arial',12,'bold')).pack(side=TOP, padx=15);
		self.topFrame = ttk.Frame(self.tab5);
		self.topFrame.pack(side=TOP, expand=1,fill=BOTH);

		ttk.Label(self.tab5, text="Output of the file", font=('Arial',12,'bold')).pack(anchor='nw', padx=20);
		self.bottomFrame = ttk.Frame(self.tab5);
		self.bottomFrame.pack(side=BOTTOM, expand=1,fill=BOTH);

		sampleText = StringVar();
		ttk.Entry(self.topFrame, textvariable=sampleText).pack(expand=1, fill=BOTH, side=BOTTOM, padx=20);

		output = StringVar();
		ttk.Label(self.bottomFrame, textvariable=output, font=('Arial',11)).pack(anchor='nw', padx=20);

		self.fifthTabData(output);

	def fifthTabData(self, output):
		data = open("/home/vikas-mshra/Desktop/second_part/Project/input.txt","r").read();
		output.set(data);
		self.tab5.after(self.globalInterval*1000, self.fifthTabData, output);
	


def main():
	root = Tk();
	app = MainWindow(root);
	root.mainloop();
	
if __name__ == '__main__':
	main();
