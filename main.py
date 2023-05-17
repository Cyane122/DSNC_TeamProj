import math
import time
import random


##
# Please, Dont...
##

def newUUID():
    return math.floor(random.random() * 1000000)


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

    def __init__(self, name, prev, extension, time, UUID):
        self.name: str = name
        self.prev: Folder = prev
        self.time = time
        self.extension: str = extension
        self.UUID = UUID

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
        super().__init__(name, prev, "dir", time.localtime(), newUUID())
        self.contents = []
        self.isOpened = False
        self.cur_sort = 0  # cur_sort: 0 -> Created Time / 1 -> Name / 2 -> Extension

    def addFile(self, addFile):
        file = File(addFile.name, self, addFile.extension, addFile.time, newUUID())
        if not self.containsName(file):
            self.contents.append(addFile)
            return
        k = 1
        while self.containsName(file):
            file = File(addFile.name + " (" + str(k) + ")", self, addFile.extension)
            k += 1
        self.contents.append(addFile)

    def containsName(self, item):
        for _ in self.contents:
            if _.name == item.name and _.extension == item.extension:
                return True
        return False

    def contains(self, item):
        for _ in self.contents:
            if _.UUID == item.UUID:
                return True
        return False

    def isOpened(self):
        return self.isOpened

    def sort(self):
        if self.cur_sort == 0:  # Created Time
            self.contents.sort(key=lambda x: x.time)
        elif self.cur_sort == 1:  # Name
            self.contents.sort(key=lambda x: x.name)
        elif self.cur_sort == 2:  # Extension
            self.contents.sort(key=lambda x: x.extension)


root = Folder("root", None)
current_dir = root
selected_dir: File = None
copying_dir: File = None
moving_dir: File = None
dic: dict = {}
sortBy = ("Created Time", "Name", "Extension")
cur_sort = 0
sort_selection = False


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
    if extension == "dir":
        print("[ Create File ] *.dir extension not allowed; It's for Folder.")
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

    try:
        return dic[ord(select)]
    except KeyError:
        print("[ Select File/Folder ] Wrong input; Try again please.")
        return selectFile()


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
            LIST.append("Goto " + current_dir.prev.name)

        LIST.append("Sort by: %s" % (sortBy[current_dir.cur_sort]))
        current_dir.sort()

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
                print(f"[ {chr(idx):2s} ] {d.getName():17s} ", end="")
                now = d.time
                print("%04d/%02d/%02d %02d:%02d:%02d" % (
                    now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                idx += 1
        print("==========================================")
        if not sort_selection:
            idx = 1
            while idx <= len(LIST):
                print("[ %02d ] %s" % (idx, LIST[idx - 1]))
                idx += 1
        else:
            idx = 1
            while idx <= len(sortBy):
                print("[ %02d ] %s" % (idx, sortBy[idx - 1]))
                idx += 1
        try:
            if sort_selection:
                select = sortBy[int(input("Choose how you want to sort: ")) - 1]
            else:
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
        elif current_dir.prev is not None and select == "Goto " + current_dir.prev.name:
            current_dir = current_dir.prev
        elif "Paste" in select:
            current_dir.addFile(File(copying_dir.name, current_dir, copying_dir.extension))
        elif "Move" in select:
            current_dir.addFile(File(moving_dir.name, current_dir, moving_dir.extension))
            moving_dir.prev.contents.remove(moving_dir)
            moving_dir = None
        elif "Sort by" in select:
            sort_selection = True
        elif "Time" in select:
            current_dir.cur_sort = 0
            sort_selection = False
        elif "Name" in select:
            current_dir.cur_sort = 1
            sort_selection = False
        elif "Extension" in select:
            current_dir.cur_sort = 2
            sort_selection = False

