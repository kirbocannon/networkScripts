# This simple script will backup the running config on an Cisco IOSv (Tested only in VIRL for now)
# device with SSH enabled. The script will also copy the newest backups locally (in the same directory
# as the python script, look for the hostname, and use that and date/time information to rename the backup
# file to something useful. This had to be done because I found no other way to scan thru files with this FTP module
# also some file cleanup  and connection termination is done at the end


from fabric.api import env, open_shell
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







