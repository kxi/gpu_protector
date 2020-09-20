import subprocess
import os
import sys
from datetime import datetime
import time
import yaml
from logger import make_logger

LOGGER = make_logger(sys.stderr, "gpu_protector")

def main():

    kill_temperature = int(sys.argv[1])

    with open("miner_conf.yaml", 'r') as f:
        miner_name_list = yaml.load(f, Loader=yaml.FullLoader)
    LOGGER.info("Miner Program List: {}".format(miner_name_list))
    print("Miner Program List: {}".format(miner_name_list))

    process = subprocess.Popen("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader", stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
    output = process.communicate()[0]

    for i, line in enumerate(output.splitlines(),0):
        gputemp = int(line.decode())
        LOGGER.info("GPU #{} Temperature = {}".format(i, gputemp))
        print("GPU #{} Temperature = {}".format(i, gputemp))

        if gputemp >= kill_temperature:
            LOGGER.critical("GPU #{} Temperature = {} is OVER Tempreature {}".format(i, gputemp, kill_temperature))
            print("GPU #{} Temperature = {} is OVER Tempreature {}".format(i, gputemp, kill_temperature))

            for miner in miner_name_list:
                process = subprocess.Popen("killall {}".format(miner), stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
                process.communicate()
                LOGGER.critical("KILL Process: {}".format(miner))
                print("KILL Process: {}".format(miner))

            LOGGER.critical("KILL Process: watchdog.py")
            for line in os.popen("ps ax | grep miner_watchdog.py | grep -v grep"):
                fields = line.split()
                pid = fields[0]
                process = subprocess.Popen("kill {}".format(pid), stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
                process.communicate()

            break

        time.sleep(1)

main()
