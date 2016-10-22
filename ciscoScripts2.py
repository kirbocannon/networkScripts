from fabric.api import run, env, open_shell, execute
from fabric import tasks, exceptions
from datetime import datetime
from ftplib import FTP, error_perm
import os

env.hosts = ['172.16.1.35', '172.16.1.36', '172.16.1.37'] #define hosts
env.user = 'cisco' # master username
env.password = 'cisco' # master password
time = datetime.now()
env.parallel = True # run parallel execution for simultaneous connections
env.disable_known_hosts = True # disable host key checking

def getBackupCfg(): # run backup commands
    try:
        open_shell("copy run ftp://cisco@172.16.1.200 \n" # backup
                   "\n"
                   "\n"
                   "exit")
    except exceptions.NetworkError as e:
        print(e)


def renameFTPFile(): # rename FTP files
    with FTP("172.16.1.200") as ftp: # connect to ftp server
        ftp.login('cisco') # ftp server username
        files = ftp.nlst()
        # for each new backup file on ftp server, write to local path here temporarily
        # then, check for hostname, then rename file with hostname
        for file in files:
            if "-confg" in file: # we are only concerned about the initial files created by the switch
                try:
                    retr_file = 'RETR {}'.format(file)
                    ftp.retrbinary(retr_file, open(file, 'wb').write) #temporarily write to current directory
                except (error_perm, AttributeError):
                    pass
                with open(file, 'r') as f: # search hostname
                    lines = f.readlines()
                    for line in lines:
                        if 'hostname' in line:
                            hostname = line.split(" ")
                            hostname = hostname[1].strip('\n') # remove extra return
                ftp.rename(file, '{}-{}-{}-{}-{}-{}-{}'.format(hostname, time.hour, time.minute, time.second,
                                                               time.month, time.day, time.year))
                os.remove(file) # cleanup temp files




if __name__ == '__main__':

    tasks.execute(getBackupCfg)
    tasks.disconnect_all()
    renameFTPFile()






#    for key, value in task_hostname.items(): # iterate over dict, asign hostname to hostname variable
#        hostname = value






