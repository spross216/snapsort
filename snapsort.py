import os
import shutil
import pyheif
import io 
import exifread
from datetime import datetime
from dataclasses import dataclass
import tkinter as tk
from tkinter import filedialog

monthDict ={
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

@dataclass
class FileDate:
    year = str
    month = str
    day = str

def sort(startingDirectory, endingDirectory):
    for filename in os.listdir(startingDirectory):
        if filename.endswith('.HEIC') or filename.endswith('.HEIF'):
            filepath = os.path.join(startingDirectory, filename)
            heifFile = pyheif.read(filepath)
            
            for metadata in heifFile.metadata:
                if metadata['type'] == 'Exif':
                    stream = io.BytesIO(metadata['data'][6:])
                    tags = exifread.process_file(stream, details=False)
                    dateTimeOriginal = str(tags.get("EXIF DateTimeOriginal"))
                    if dateTimeOriginal is not None:
                        dateTime = datetime.strptime(str(dateTimeOriginal), '%Y:%m:%d %H:%M:%S')
                        fileDate = FileDate()
                        fileDate.year=str(dateTime.year)
                        fileDate.month=monthDict[dateTime.strftime('%m')]
                        fileDate.day=dateTime.strftime('%d')
                
                        yearDir = os.path.join(endingDirectory, fileDate.year)
                        if not os.path.exists(yearDir):
                            os.mkdir(yearDir)
                        monthDir = os.path.join(yearDir, fileDate.month)
                        if not os.path.exists(monthDir):
                            os.mkdir(monthDir)
                        dayDir = os.path.join(monthDir, fileDate.day)
                        if not os.path.exists(dayDir):
                            os.mkdir(dayDir)
                        
                        newFilePath = os.path.join(dayDir, filename)
                        shutil.move(filepath, newFilePath)


class Gui:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('400x200')
        self.root.title('Snap Sort')
    
    def createFrame(self):
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.pack()
    
    def startingDirectory(self):
        self.startingDirectory = filedialog.askdirectory()
        return self.startingDirectory

    def endingDirectory(self):
        self.endingDirectory = filedialog.askdirectory()
        return self.endingDirectory
    
    def sortButtonClick(self):
        startingDir = self.startingDirectory
        endingDir = self.endingDirectory
        sort(startingDir, endingDir)

    def createButtons(self):
        self.sortButton = tk.Button(self.mainFrame, text='Sort', command= self.sortButtonClick)
        self.sortButton.pack()

        self.startingDirectoryButton = tk.Button(self.mainFrame, text='Select a Directory to Sort', command=self.startingDirectory)
        self.startingDirectoryButton.pack()

        self.endingDirectoryButton = tk.Button(self.mainFrame, text='Select the Destination Directory', command=self.endingDirectory)
        self.endingDirectoryButton.pack()



if __name__ == '__main__':
    snap = Gui()
    snap.createFrame()
    snap.createButtons()
    snap.root.mainloop()



