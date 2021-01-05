from multiprocessing import Process
import os
import pandas

ip_list = ["192.168.1.107"]

def job(ip, recipe_name):
    
    print("start process {} {}".format(ip, recipe_name))
    os.system("python detect_leak_job.py {} {}".format(ip, recipe_name))


def main():
    recipe_name = input("please input recipe name: ")
    for ip in ip_list:
        process = Process(target = job, args=(ip, recipe_name))
        process.start()
        
if __name__ == "__main__":
    main()