import subprocess

pro = subprocess.run(['ls','-l','/proc/1/fd'], capture_output=True);
pro1 = subprocess.run(['grep','socket'], capture_output=True, input=pro.stdout);
if "19748" in str(pro1.stdout):
	print("true");
