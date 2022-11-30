from scp import SCPClient
from paramiko import SSHClient

import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import os


'''
scp get file and display histogram

press 'q' to exit
press key any else to display next

'''


exit_flag=False

def _ssh_run_remote_command(cmd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="192.168.10.192",
                       username="root",
                       password="rgbd123gp")
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    out = stdout.read().decode().strip()
    error = stderr.read().decode().strip()

    print(out)
    if error:
        raise Exception('There was an error pulling the runtime: {}'.format(error))
    ssh_client.close()
    return out

def on_key_press(event):
    global exit_flag
    if event.key == 'q':
        exit_flag=True
    #print(event.key, exit_flag)
    plt.close()

def grayHist(img):
    #pixelSequence = img.reshape([640 * 480, ])
    numberBins = 256
    fig = plt.figure(figsize=(6,4))
    histogram, bins, patch = plt.hist(img, numberBins, [0,256],
                                      facecolor='black', histtype='bar')
    plt.xlabel("gray label")
    plt.ylabel("number of pixels")
    #plt.axis([50, 240, 0, np.max(histogram)])
    #fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    plt.show()



ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('192.168.10.192', 22, 'root', 'rgbd123gp')

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())

# Uploading the 'test' directory with its content in the
# '/home/user/dump' remote directory
#scp.put('test', recursive=True, remote_path='/home/user/dump')

while True:
    if exit_flag:
        print ("quit")
        break

    #print(exit_flag)
    stdin,stdout,stderr = ssh.exec_command("irImageSave 1")
    print(stdout.read().decode().strip())
    #scp.put('test.txt', 'test2.txt')
    scp.get('/tmp/ir.bin')

    with open('ir.bin','rb') as f:
        dataBytes = f.read()
        image= np.frombuffer(dataBytes, dtype=np.uint8)
        grayHist(image)

scp.close()


