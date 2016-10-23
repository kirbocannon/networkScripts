# This simple script will first get the hostname of a switch for later use in the filename creation. Then, it will
# backup the running config on an Cisco IOSv (Tested only in VIRL for now)
# device with SSH enabled. The script will send the command to backup to an ftp server (although you can
# specify any type of server, and then it will name the file appropriately with the time and hostname.


from fabric.api import env, open_shell, run, settings, hide
from fabric import tasks, exceptions
from datetime import datetime
from ftplib import FTP, error_perm
import os

env.hosts = ['172.16.1.35'] #define hosts
env.user = 'cisco' # master username
env.password = 'cisco' # master password
time = datetime.now()
env.parallel = True # run parallel execution for simultaneous connections
env.disable_known_hosts = True # disable host key checking
hostname = ""

def getHostname():
    global hostname
    with settings(hide('stdout')): # suppress uneeded output
        hostname = run("show run | i hostname", shell=False)
        return hostname

def getBackupCfg(): # run backup commands
    try:
        open_shell("copy run ftp://cisco@172.16.1.200/{}-config-{}-{}-{}-{}-{}-{} \n" # backup
                   "\n"
                   "\n"
                   "\n"
                   "exit".format(hostname, time.hour, time.minute, time.second,
                                 time.month, time.day, time.year))
    except exceptions.NetworkError as e:
        print("Issue with a node:", e)




if __name__ == '__main__':
    hostname = tasks.execute(getHostname)
    hostname = list(hostname.values())[0].split(" ")[1]
    print(hostname)
    tasks.execute(getBackupCfg)
    tasks.disconnect_all()
    #renameFTPFile()







