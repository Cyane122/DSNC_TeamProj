import math
import time
import keyboard
import os
import time
import random


##
##

class CustomError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class File:
    def __init__(self, name, prev, extension):
        self.name: str = name
        self.prev: Folder = prev
        self.time = time.localtime()
        self.extension: str = extension
        self.UUID = math.floor(random.random() * 1000000)

    def getName(self):
        return self.name + "." + self.extension

    def getLocation(self):
        loc = self.name + "." + self.extension
        file = self
        while file.prev is not None:
            file = file.prev
            t: str = file.name + "." + file.extension
            loc = t + "\\" + loc

        return loc


class Folder(File):
    def __init__(self, name, prev):
        super().__init__(name, prev, "dir")
        self.contents = []
        self.isOpened = False

    def addFile(self, addFile):
        self.contents.append(addFile)

    def contains(self, item):
        for _ in self.contents:
            if _.UUID == item.UUID:
                return True
        return False

    def isOpened(self):
        return self.isOpened


root = Folder("root", None)
current_dir = root
selected_dir: File = None
copying_dir: File = None
moving_dir: File = None
dic: dict = {}


def createFile():
    _input_ = input("[ Create File ] Insert your file name with extension (e.g. file.jpg): ")
    extension, name = "", ""
    tmp = False
    for c in _input_:
        if c == '.':
            if tmp:
                name = name + '.' + extension
                extension = ""
            else:
                tmp = True
            continue
        if tmp:
            extension = extension + c
        else:
            name = name + c
    if extension == "":
        print("[ Create File ] Wrong input; Try again.")
        createFile()
        return
    file = File(name, current_dir, extension)
    k = 1
    while current_dir.contains(file):
        file = File(name + " (" + str(k) + ")", current_dir, extension)
        k += 1

    current_dir.addFile(file)


def createFolder():
    name = input("[ Create Folder ] Insert your file name (e.g. folder): ")

    folder = Folder(name, current_dir)
    k = 1
    while current_dir.contains(folder):
        folder = Folder(name + " (" + str(k) + ")", current_dir)
        k += 1

    current_dir.addFile(folder)


def selectFile():
    select = input("[ Select File/Folder ] Enter the alphabet of the file/folder you want to select: ")
    print(type(dic[ord(select)]))
    if dic[ord(select)] is None:
        print("[ Select File/Folder ] Invalid value; Try again please.")
        time.sleep(0.3)
        return None
    return dic[ord(select)]


if __name__ == "__main__":
    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        LIST = ["Create File", "Create Folder"]
        select = 0

        if copying_dir is not None:
            LIST.append("Paste " + copying_dir.getName())

        if moving_dir is not None and moving_dir.prev != current_dir:
            LIST.append("Move " + moving_dir.getName() + " to " + current_dir.getName())

        if selected_dir is None:
            LIST.append("Select File/Folder")
        else:
            if selected_dir.extension == "dir":
                LIST.append("Unselect Folder")
                if current_dir.contains(selected_dir):
                    LIST.append(("Goto " + selected_dir.name))
                print(current_dir.contains(selected_dir))
                LIST.append("Copy Folder")
                LIST.append("Move Folder")
                LIST.append("Delete " + selected_dir.name)
            else:
                LIST.append("Unselect File")
                LIST.append("Copy File")
                LIST.append("Move File")
                LIST.append("Delete " + selected_dir.name + "." + selected_dir.extension)

        if current_dir.prev is not None:
            LIST.append("Move to " + current_dir.prev.name)

        print("==========================================")
        print("Python File Manager")
        print("Current Direction: ", current_dir.getLocation())
        if selected_dir is not None:
            print("Selected Direction:", selected_dir.getLocation())
        if copying_dir is not None:
            print("<< Copying", copying_dir.getLocation(), ">>")
        if moving_dir is not None:
            print("<< Moving", moving_dir.getLocation(), ">>")
        print("==========================================")
        idx: int = 65  # chr(idx) = 'A'

        for k in dic.keys():
            dic[k] = None

        if len(current_dir.contents) == 0:
            print("this folder is empty...")
        else:
            for d in current_dir.contents:
                dic[idx]: File = d
                print(f"[{chr(idx)}] {d.getName():18s}", end="")
                now = d.time
                print("%04d/%02d/%02d %02d:%02d:%02d" % (
                    now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                idx += 1
        print("==========================================")
        idx = 1
        while idx <= len(LIST):
            print("[", idx, "]", LIST[idx - 1])
            idx += 1
        try:
            select = LIST[int(input("Choose what you want to do: ")) - 1]
        except ValueError:
            print("Invalid value. Try again please.")
            time.sleep(0.3)
            continue

        if select == "Create File":
            createFile()
        elif select == "Create Folder":
            createFolder()
        elif select == "Select File/Folder":
            tmp = selectFile()
            if tmp is not None:
                selected_dir = tmp
        elif select == "Unselect File" or select == "Unselect Folder":
            selected_dir = None
        elif select == "Copy File" or select == "Copy Folder":
            copying_dir = selected_dir
            selected_dir = None
        elif select == "Move File" or select == "Move Folder":
            moving_dir = selected_dir
            selected_dir = None
        elif selected_dir is not None and select == "Goto " + selected_dir.name:
            current_dir = selected_dir
        elif select == "Move to " + current_dir.prev.name:
            current_dir = current_dir.prev
