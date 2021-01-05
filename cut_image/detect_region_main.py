from multiprocessing import Process
import os
import pandas

ip_list = ["192.168.1.205", "192.168.1.236", "192.168.1.219", "192.168.1.198",
           "192.168.1.194", "192.168.1.151", "192.168.1.247", "192.168.1.130", 
           "192.168.1.187", "192.168.1.51", "192.168.1.33", "192.168.1.211"]

def job(ip, recipe_name, detect_region_dilation, detect_region_low_threshold, 
        detect_region_high_threshold, complete_region_dilation, 
        complete_region_low_threshold, complete_region_high_threshold, 
        complete_ratio, second_detect_region_dilation,
        second_detect_region_low_threshold, 
        second_detect_region_high_threshold):
    
    print("start process {} {}".format(ip, recipe_name))
    os.system("python detect_region_job.py {} {} {} {} {} {} {} {} {} {} {} {}".format(ip, recipe_name,
                                                                                       detect_region_dilation, 
                                                                                       detect_region_low_threshold, 
                                                                                       detect_region_high_threshold, 
                                                                                       complete_region_dilation, 
                                                                                       complete_region_low_threshold, 
                                                                                       complete_region_high_threshold, 
                                                                                       complete_ratio,
                                                                                       second_detect_region_dilation,
                                                                                       second_detect_region_low_threshold,
                                                                                       second_detect_region_high_threshold))


def main():
    recipe_name = input("please input recipe name: ")
    recipe_parameter = pandas.read_csv("{}/parameter.csv".format(recipe_name), index_col = 0)
    for ip in ip_list:
        process = Process(target = job, args=(ip, recipe_name, recipe_parameter.loc[ip, "detect_region_dilation"], 
                                              recipe_parameter.loc[ip, "detect_region_low_threshold"], 
                                              recipe_parameter.loc[ip, "detect_region_high_threshold"],
                                              recipe_parameter.loc[ip, "complete_region_dilation"],
                                              recipe_parameter.loc[ip, "complete_region_low_threshold"],
                                              recipe_parameter.loc[ip, "complete_region_high_threshold"],
                                              recipe_parameter.loc[ip, "complete_ratio"],
                                              recipe_parameter.loc[ip, "second_detect_region_dilation"],
                                              recipe_parameter.loc[ip, "second_detect_region_low_threshold"],
                                              recipe_parameter.loc[ip, "second_detect_region_high_threshold"]))
        process.start()
        
if __name__ == "__main__":
    main()