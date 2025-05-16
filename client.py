import socket
import time
from threading import Thread
import subprocess
import gui

operation_number = 0
BUFFER_SIZE = 4096
ip_addresses = ['13.60.58.23', '16.171.40.22', '13.60.241.188']
threads_list = []

class Client:

    def worker(self, ipAddr, fileItem, opNum, index):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ipAddr, 12345))

        with client:  # optional line
            with open(fileItem, 'rb') as file:
                image_chunk = file.read(BUFFER_SIZE)

                while image_chunk:
                    client.send(image_chunk)
                    time.sleep(1)
                    image_chunk = file.read(BUFFER_SIZE)

            client.send(f'{opNum}'.encode())

            with open('client_file_edited' + str(index) + '.jpeg', 'wb') as file:
                image_chunk = client.recv(BUFFER_SIZE)

                while image_chunk:
                    file.write(image_chunk)
                    image_chunk = client.recv(BUFFER_SIZE)

                    if image_chunk == b"%IMAGE_COMPLETED%":  # optional line
                        break


    def start(self, images_list, opNumber):
        operation_number = opNumber

        for i, item in enumerate(images_list):

            up_ipAddr = 0
            for j, ip in enumerate(ip_addresses):
                hostname = ip
                batcmd = "ping -n 1 " + hostname
                try:
                    result = subprocess.check_output(batcmd, shell=True)
                    if b"Received = 1" in result:
                        up_ipAddr = j
                        break
                except:
                    pass

            threads_list.append(Thread(target=self.worker, args=(ip_addresses[up_ipAddr], item, operation_number, i)))

            ip_addresses.append(ip_addresses.pop(up_ipAddr))

            # i % len(ip_addresses)

        for i, th in enumerate(threads_list):
            th.start()
            th.join()
            # gui_obj.updateProgress((100/len(images_list))*(i+1))
            gui_obj.updateProgress((100/len(images_list))*(i+1), 100/len(images_list))

        gui_obj.taskCompleted()

client = Client()
gui_obj = gui.GUI(client)
gui_obj.__del__()
