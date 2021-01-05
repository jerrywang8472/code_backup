from multiprocessing import Process
import os

ip_list = ["192.168.1.205", "192.168.1.236", "192.168.1.219", "192.168.1.198",
           "192.168.1.194", "192.168.1.151", "192.168.1.247", "192.168.1.130", 
           "192.168.1.187", "192.168.1.51", "192.168.1.33", "192.168.1.211"]

def job(ip, recipe_name):
    print("start process {} {}".format(ip, recipe_name))
    os.system("python set_complete_job.py {} {}".format(ip, recipe_name))


def main():
    recipe_name = input("please input recipe name: ")
    for ip in ip_list:
        process = Process(target = job, args=(ip, recipe_name))
        process.start()
        
if __name__ == "__main__":
    main()