import time     # for sleep function in progress bar
from tkinter import *
from tkinter import filedialog, ttk     # for combobox and file selection
import os
import customtkinter
import threading

currentDirectory = os.getcwd()  # get current directory

class GUI:
    def createWindow(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.window = customtkinter.CTk()
        self.window.title("Distributed Project")
        self.window.geometry("700x600")
        self.errorLabel = customtkinter.CTkLabel(self.window, text='')
        self.resultLabel = customtkinter.CTkLabel(self.window, text='')
        self.choice = 1
        self.filePath = {}

    def createInitialWidgets(self):
        # create button
        self.fileButton = customtkinter.CTkButton(self.window, text="Select Image/s", command=self.openImage, font=("Arial", 14))
        self.fileButton.pack(pady=100)

        # create label
        operationFrame = Frame(self.window, bg="#1a1a1a")
        operationFrame.pack(pady=20)
        customtkinter.CTkLabel(operationFrame, text='Pick an operation: ', font=("Helvetica", 18)).grid(row=0, column=0)
        
        # create drop down button
        options = ["Gaussian Blurring", "Sharpening", "Color Inversion"]
        self.selectedOption = StringVar()
        self.selectedOption.set(options[0])
        self.comboBox = customtkinter.CTkComboBox(operationFrame, font=("Arial", 18), variable=self.selectedOption, values=options, width=200, height=30, dropdown_font=("Arial", 18))
        self.comboBox.grid(row=0, column=1)

        # create upload button
        self.uploadButton = customtkinter.CTkButton(self.window, text="Upload", command=self.upload, font=("Arial", 14))
        self.uploadButton.pack(pady=50)

    #constructor
    def __init__(self, client):
        self.client = client
        self.createWindow()
        self.createInitialWidgets()

    def openImage(self):
        self.resultLabel.destroy()
        # file_path = {'path1', 'path2'}
        self.filePath = filedialog.askopenfilenames(initialdir=currentDirectory, title="Select Image", filetypes=(("all files", "*.*"), ("jpg Files", "*.jpg"), ("png Files", "*.png"), ("jpeg Files", "*.jpeg")))
        # if(len(self.filePath) > 0 and len(self.filePath) < 4):
        if(len(self.filePath) > 0):
            self.errorLabel.destroy()

    def upload(self):
        self.resultLabel.destroy()
        # if(len(self.filePath) > 0 and len(self.filePath) < 4):
        if(len(self.filePath) > 0):
            self.errorLabel.destroy()
            self.fileButton.configure(state="disabled")
            self.uploadButton.configure(state="disabled", text="Processing Images ...")
            # create progress button
            self.progressBar = ttk.Progressbar(self.window, orient="horizontal", length=300, mode="determinate")
            self.progressBar.pack(pady=20)
            if self.selectedOption.get() == "Sharpening":
                self.choice = 2
            elif self.selectedOption.get() == "Color Inversion":
                self.choice = 3

            allImages = []
            for i in range(len(self.filePath)):
                allImages.append(os.path.relpath(self.filePath[i], currentDirectory))

            self.client.start(allImages, self.choice)

        elif(len(self.filePath) == 0):
            self.errorLabel.destroy()
            self.errorLabel = customtkinter.CTkLabel(self.window, text="No files are selected yet!")
            self.errorLabel.pack(pady=20)
        # else: 
        #     self.errorLabel.destroy()
        #     self.errorLabel = customtkinter.CTkLabel(self.window, text="You can only upload maximum 3 images")
        #     self.errorLabel.pack(pady=20)

    def taskCompleted(self):
        self.progressBar.destroy()
        self.resultLabel = customtkinter.CTkLabel(self.window, text="The images are downloaded successfully!", font=("Arial", 24))
        self.resultLabel.pack(pady=20)
        self.fileButton.configure(state="active")
        self.uploadButton.configure(state="active", text="Upload")
        self.filePath = {}

    def runLogicalFunction(self):
        for i in range(100):
            print(i)
            time.sleep(0.05)

    def updateProgress(self, value, sz):
        for i in range(int(value-sz), int(value)):
            self.progressBar['value'] = i
            self.window.update_idletasks()
            time.sleep(0.05)

    # destructor
    def __del__(self):
        self.window.mainloop()

# gui = GUI()
# gui.__del__()
