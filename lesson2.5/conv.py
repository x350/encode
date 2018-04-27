import os
import sys
import subprocess

def detect_patform():
	return sys.platform

def detect_content_dir(name_dir, name_curent_dir):
	my_dir = subprocess.Popen(['dir', name_curent_dir], stdout=subprocess.PIPE, shell=True, encoding='cp866')
	for line in my_dir.stdout:
		if len(line) < 3:
			continue
		if line.split()[2] == '<DIR>' and line.split()[3] == name_dir:
			return os.path.join(name_curent_dir, name_dir)


def make_dir(name_new_dir):
	subprocess.Popen(['mkdir', name_new_dir], shell=True)
	return os.path.join(os.getcwd(), name_new_dir)


def run_programm(programm):	
	subprocess.Popen(programm, stdout=subprocess.PIPE)



# def make_command_with_output_dir(command, path):
# 	name_file = os.path.basename(command[2])
# 	command[5] = os.path.join(path, name_file)
# 	return command[1:]

def make_commands():
	dir_sourse = input("Input source dir: ")
	size = input("Input size in px: ")
	dir_result = input("Input result dir: ")
	new_path = None
	new_path = detect_content_dir(dir_result, os.getcwd())
	if not new_path:
		new_path = make_dir(dir_result)
	list_dir = os.listdir(dir_sourse)
	result = []
	if list_dir:
		for item in list_dir:
			result.append(['convert.exe', os.path.join(dir_sourse, item), '-resize', size, os.path.join(dir_result, item)])
	return result	




# command = ['conv.py', 'convert.exe', 'Source\\face-04.jpg', '-resize', '200', 'output.jpg']
# print(command)



# print([os.path.join('Source', item) for item in os.listdir('Source')])

# run_programm(make_command_with_output_dir(command, new_path))

for i in make_commands():
	run_programm(i)