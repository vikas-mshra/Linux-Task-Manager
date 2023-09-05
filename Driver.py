import CpuUtilization
class Driver(CpuUtilization.CpuUtilization):
	def __init__(self):
		self.executeCPUStatisticsScript();
	def executeCPUStatisticsScript(self):
		self.fetchCPUStatisticsAlongWithInterruptContextSwitchesMemoryUtilization();
		self.calculatingCPUStatisticsInIntervals();

def main():
	Driver();

if __name__ == '__main__':
	main();
