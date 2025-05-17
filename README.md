# 📷 Distributed Image Processing System Using EC2 Instances

---

## 🧠 Overview

This project implements a distributed image processing system using a client-server architecture deployed across multiple AWS EC2 instances.

It demonstrates:

- Real-world application of distributed computing concepts
- TCP socket communication
- Python multithreading
- Basic client-side load balancing

---

## 🏗️ System Architecture

- 🖥️ Client: A GUI-based Python application that distributes image processing tasks across multiple cloud servers.
- ☁️ Servers: Each EC2 instance runs a socket server capable of processing image transformations.
- 🔄 Threading: Each image is split into 4 parts and processed in parallel using threads on the server side.
- 🔁 Load Balancing: The client uses round-robin IP rotation to distribute load across available servers.

---

## 🔧 Technologies Used

| 🧩 Category          | 🔧 Tools / Libraries                                       |
|---------------------|------------------------------------------------------------|
| Programming          | Python 3                                                  |
| Networking           | socket (TCP/IP communication)                             |
| Image Processing     | OpenCV (cv2), Pillow (PIL)                                |
| GUI                  | tkinter, customtkinter                                    |
| Threading            | Python threading module                                   |
| Cloud Infrastructure | AWS EC2 (Ubuntu 22.04 micro instances)                    |

---

## 🛠️ Features

- 📤 Upload multiple images
- 🎛️ Choose from the following operations:
  - Gaussian Blur
  - Bitwise Color Inversion
  - Edge Enhancement (sharpen)
- 🌐 Distribute processing tasks to multiple EC2 servers
- 🧵 Multithreaded image processing on the server side
- 📩 Receive processed images and save them locally
- 📊 Real-time progress updates via GUI

---

## 🚀 How It Works

1. ✅ The client pings EC2 IP addresses to check which servers are online.
2. 🔁 Each image is sent to a different server (using round-robin logic).
3. 🧵 The server splits the image into 4 quadrants and processes them in parallel using threads.
4. 📥 Processed image is reassembled and sent back to the client.
5. 💾 The client saves the processed image and updates the progress bar.

---

## 💻 Run the Project

### 📦 Dependencies

Install required packages:

```bash
pip install opencv-python pillow customtkinter
```

> 📝 Note:  
> - tkinter is usually pre-installed with Python.  
> - If it's missing on Linux, install it using:
>
>   ```bash
>   sudo apt install python3-tk
>   ```

---

### 🖥️ Client Setup (Windows)

1. Clone this repository to your local machine.
2. Open `client.py` and update the IP list:

   ```python
   ip_addresses = ['<EC2-IP-1>', '<EC2-IP-2>', '<EC2-IP-3>']
   ```

3. Run the client:

   ```bash
   python client.py
   ```

---

### ☁️ Server Setup (on each EC2 instance)

1. SSH into the EC2 instance.
2. Install required packages:

   ```bash
   pip3 install opencv-python pillow
   ```

3. Run the server:

   ```bash
   python3 server.py
   ```

> ⚠️ Make sure port 12345 is allowed in your EC2 Security Group (inbound rule).

---

## 📊 Performance

| Operation         | Avg. Processing Time (JPEG) |
|------------------|-----------------------------|
| Gaussian Blur     | 1.1 seconds                 |
| Color Inversion   | 1.2 seconds                 |
| Edge Enhancement  | 1.3 seconds                 |

- ✅ Handles multiple concurrent images
- ⚡ Low latency image transfer over TCP
- 🧩 Stateless server architecture allows scalability & fault tolerance
