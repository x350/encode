import os
import sys
import subprocess
from multiprocessing import Process
from queue import Queue
from multiprocessing import Pool


def detect_platform():
    return sys.platform


def detect_content_dir(name_dir, name_curent_dir):
    if detect_platform() == 'win32':
        my_dir = subprocess.Popen(['dir', name_curent_dir], stdout=subprocess.PIPE, shell=True, encoding='cp866')
        for line in my_dir.stdout:
            if len(line) < 3:
                continue
            if line.split()[2] == '<DIR>' and line.split()[3] == name_dir:
                return os.path.join(name_curent_dir, name_dir)
    elif detect_platform() == 'linux':
        my_dir = subprocess.Popen(['ls', name_curent_dir], stdout=subprocess.PIPE, shell=True)
        for line in my_dir.stdout:
            if line.decode('utf-8').strip() == name_dir:
                return os.path.join(name_curent_dir, name_dir)


def make_dir(name_new_dir):
    if detect_platform == 'win32':
        args = ['mkdir', name_new_dir]
    elif detect_platform == 'linux':
        args = ['mkdir ' + name_new_dir]
    subprocess.Popen(['mkdir', name_new_dir], shell=True)
    return os.path.join(os.getcwd(), name_new_dir)


def run_programm(programm):
    print("Process PID =", os.getpid())
    subprocess.Popen(programm, stdout=subprocess.PIPE)


def make_commands(name_command):
    dir_sourse = input("Input source dir: ")
    if not detect_content_dir(dir_sourse, os.getcwd()):
        print("There is't this folder.")
        exit(1)
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
            result.append([name_command, os.path.join(dir_sourse, item), '-resize', size, os.path.join(dir_result, item)])
    return result


if __name__ == '__main__':

    if detect_platform() == 'win32':
        name_command = 'convert.exe'
    elif detect_platform() == 'linux':
        name_command = 'convert'
    else:
        print("Unknown platform")

# ----------------------------
# Single process

    # for i in make_commands(name_command):
    #     run_programm(i)

# ----------------------------
# Number of foto = number of process

    # q = Queue()
    # for i in make_commands(name_command):
    #     q.put(i)
    #
    # while True:
    #     proc = Process(target=run_programm, args=(q.get(),))
    #     proc.start()
    #     proc.join()
    #     if q.empty():
    #         print('Queue is empty.')
    #         break

# ----------------------------
# Four process

    with Pool(processes=4) as pool:
        pool.map(run_programm, make_commands(name_command))




