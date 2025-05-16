import io
import os
import socket
from threading import Thread
import numpy as np
import cv2
from PIL import Image

# -------------------------------   imports done

BUFFER_SIZE = 4096
operation_number = 0


def worker(img_part):
    if operation_number == 1:
        img_part = cv2.GaussianBlur(img_part, (9, 9), 20)

    elif operation_number == 2:
        img_part2 = cv2.GaussianBlur(img_part, (9, 9), 20)
        img_part = cv2.addWeighted(img_part, 3.5, img_part2, -2.5, 0)

    elif operation_number == 3:
        img_part = cv2.bitwise_not(img_part)

    return img_part


class ThreadWithReturnValue(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


# -------------------------------   variables, function, and class declaration done

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # created a socket called 'server'
server.bind(('0.0.0.0/0', 12345))   # attached the shown ip address and port number to this socket

server.listen()     # socket listening for incoming connection requests

while True:
    client_socket, _ = server.accept()  # accept connection from this 'client' socket -- connection established
    # ----------------------------------- new socket created to represent only this connection
    with client_socket:
        file_stream = io.BytesIO()
        image_chunk = client_socket.recv(BUFFER_SIZE)

        while image_chunk:
            file_stream.write(image_chunk)
            image_chunk = client_socket.recv(BUFFER_SIZE)

            if image_chunk == b"1" or image_chunk == b"2" or image_chunk == b"3":
                operation_number = int(image_chunk.decode())
                break
        # ------------------------------------- image and operation number have been received

        image = np.array(Image.open(file_stream))
        h, w, channels = image.shape
        half_vertical = w // 2
        half_horizontal = h // 2

        top_left = image[:half_horizontal, :half_vertical]
        top_right = image[:half_horizontal, half_vertical:]
        bottom_left = image[half_horizontal:, :half_vertical]
        bottom_right = image[half_horizontal:, half_vertical:]

        # --------------------------------------- image split into 4 quarters across 4 threads

        # ---------- Image Processing - Start ----------- #
        t1 = ThreadWithReturnValue(target=worker, args=(top_left,))
        t2 = ThreadWithReturnValue(target=worker, args=(top_right,))
        t3 = ThreadWithReturnValue(target=worker, args=(bottom_left,))
        t4 = ThreadWithReturnValue(target=worker, args=(bottom_right,))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        image[:half_horizontal, :half_vertical] = t1.join()
        image[:half_horizontal, half_vertical:] = t2.join()
        image[half_horizontal:, :half_vertical] = t3.join()
        image[half_horizontal:, half_vertical:] = t4.join()
        # ---------- Image Processing - End ----------- #

        # ------------------------------------------------- processed image parts joined together

        Image.fromarray(image).save('server_img.jpeg', format='JPEG')

        with open('server_img.jpeg', 'rb') as file:
            file_data = file.read(BUFFER_SIZE)

            while file_data:
                client_socket.send(file_data)
                file_data = file.read(BUFFER_SIZE)

        client_socket.send(b"%IMAGE_COMPLETED%")    # optional line
        os.unlink('server_img.jpeg')
