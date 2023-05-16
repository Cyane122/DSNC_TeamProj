import time
import keyboard
import os
import time


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
            if _.name == item.name and _.extension == item.extension:
                return True
        return False

    def isOpened(self):
        return self.isOpened


root = Folder("root", None)
current_dir = root
selected_dir = None
dic: dict = {}


def fileTree(_dir, depth):
    for d in _dir.contents:
        for _ in range(depth):
            print("   ", end="")
        if selected_dir == d:
            print(">  ", end="")
        else:
            print("   ")
        print("ㄴ", end=" ")
        print(d.getName(), end="")
        if d is Folder and d.isOpened():
            fileTree(d, depth + 1)


def fileTreeWith(_dir, depth, cur):
    for d in _dir.contents:
        if selected_dir == d and cur != d:
            print(">  ")
        elif selected_dir != d and cur == d:
            print("-> ")
        elif selected_dir == d and cur == d:
            print("->>")
        else:
            print("   ")
        for _ in range(depth):
            print(" ", end="")
        print("ㄴ", end=" ")
        print(d.getName())
        if d is Folder and d.isOpened():
            fileTree(d, depth + 1)


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


def copyFileFolder():
    pass


def moveFileFolder():
    pass


if __name__ == "__main__":
    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        LIST = ["Create File", "Create Folder"]
        select = 0

        if selected_dir is None:
            LIST.append("Select File/Folder")
        else:
            if selected_dir is Folder:
                LIST.append("Unselect Folder")
                if current_dir.contains(selected_dir):
                    LIST.append(("Goto " + selected_dir.name))
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
            copyFileFolder()
        elif select == "Move File" or select == "Move Folder":
            moveFileFolder()
        elif selected_dir is not None and select == "Goto " + selected_dir.name:
            current_dir = selected_dir
        elif select == "Move to " + current_dir.prev.name:
            current_dir = current_dir.prev