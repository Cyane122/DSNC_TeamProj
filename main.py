from datetime import datetime
import keyboard
import os
import time


class CustomError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class File:
    def __init__(self, name, prev, extension):
        self.name = name
        self.prev = prev
        self.time = datetime.now()
        self.extension = extension

    def getName(self):
        return self.name + "." + self.extension


class Folder(File):
    def __init__(self, name, prev):
        super().__init__(name, prev, "dir")
        self.contents = []
        self.isOpened = False

    def getLocation(self):
        loc = self.name
        file = self
        while file.prev is not None:
            file = file.prev
            loc = file.name + "\\" + loc

        return loc

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


def fileTree(_dir, depth):
    for d in _dir.contents:
        if selected_dir == d:
            print(">  ")
        else:
            print("   ")
        for _ in range(depth):
            print(" ", end="")
        print("ㄴ", end=" ")
        print(d.getName())
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
    current_selection = root
    while True:
        fileTreeWith(root, 0, current_selection)
        if keyboard.is_pressed("DOWN"):
            if current_selection.isOpened:
                current_selection = current_selection.contents[0]
            else:
                current_selection = current_selection.prev.contents[
                    current_selection.prev.contents.find(current_selection) + 1]
        elif keyboard.is_pressed("ENTER"):
            return current_selection
        # TODO("함수 마저 완성")


if __name__ == "__main__":
    while True:

        LIST = ["Create File", "Create Folder"]
        select = 0

        if selected_dir is None:
            LIST.append("Select File/Folder")
        else:
            if selected_dir is Folder:
                LIST.append("Unselect Folder")
                LIST.append("Copy Folder")
                LIST.append("Move Folder")
            else:
                LIST.append("Unselect File")
                LIST.append("Copy File")
                LIST.append("Move File")

        print("==========================================")
        print("Python File Manager")
        print("Current Direction: ", current_dir.getLocation())
        print("==========================================")
        var = "   "
        if selected_dir == root:
            var = ">  "
        print(var + current_dir.name)
        fileTree(current_dir, 0)
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
            selected_dir = selectFile()
