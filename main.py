import math
import time
import random


##
# Please, Dont...
##

UUID_LIST: list = [0 for i in range(1000000)]


def newUUID():
    uuid = math.floor(random.random() * 1000000)
    while UUID_LIST.__getitem__(uuid):
        uuid = math.floor(random.random() * 1000000)
    UUID_LIST[uuid] = True
    return uuid


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
        self.cur_sort = 0  # cur_sort: 0 -> Created Time / 1 -> Name / 2 -> Extension
        self.cur_dir = True  # cur_dir: True -> Ascending Order / False -> Descending Order

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

    def sort(self):
        if self.cur_sort == 0:  # Created Time
            self.contents.sort(key=lambda x: x.time, reverse=(not self.cur_dir))
        elif self.cur_sort == 1:  # Name
            self.contents.sort(key=lambda x: x.name, reverse=(not self.cur_dir))
        elif self.cur_sort == 2:  # Extension
            self.contents.sort(key=lambda x: x.extension, reverse=(not self.cur_dir))


root = Folder("root", None)
current_dir = root
selected_dir: File = None
copying_dir: File = None
moving_dir: File = None
dic: dict = {}
sortBy = ("Created Time", "Name", "Extension")
sortDir = ("Ascending Order", "Descending Order")
cur_sort = 0
sort_selection = False
sort_upperDown = False


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
    file = File(name, current_dir, extension, time.localtime(), newUUID())
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
    try:
        t = dic[ord(select)]
    except KeyError:
        print("[ Select File/Folder ] Wrong input: Try again please.")
        return selectFile()
    if dic[ord(select)] is None:
        print("[ Select File/Folder ] Invalid value; Try again please.")
        time.sleep(0.3)
        return None

    try:
        return dic[ord(select)]
    except KeyError:
        print("[ Select File/Folder ] Wrong input; Try again please.")
        return selectFile()


def deleteFile():
    selected_dir.prev.contents.remove(selected_dir)


def searchFile():
    search = input("[ Search File/Folder ] Enter the name or extension of the file you are looking for: ")
    if "." in search:
        extension, name = "", ""
        tmp = False
        for c in search:
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


if __name__ == "__main__":
    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        LIST = ["Create File", "Create Folder", "Search File/Folder"]
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

        if current_dir.cur_dir:
            tmp = "Ascending"
        else:
            tmp = "Descending"

        LIST.append("Sort by: %s - %s" % (sortBy[current_dir.cur_sort], tmp))
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
                print(f"[ {chr(idx)} ] {d.getName():17s} ", end="")
                now = d.time
                print("%04d/%02d/%02d %02d:%02d:%02d" % (
                    now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                idx += 1
        print("==========================================")
        if sort_selection:
            idx = 1
            while idx <= len(sortBy):
                print("[ %02d ] %s" % (idx, sortBy[idx - 1]))
                idx += 1
        elif sort_upperDown:
            idx = 1
            while idx <= len(sortDir):
                print("[ %02d ] %s" % (idx, sortDir[idx - 1]))
                idx += 1
        else:
            idx = 1
            while idx <= len(LIST):
                print("[ %02d ] %s" % (idx, LIST[idx - 1]))
                idx += 1
        try:
            if sort_selection:
                select = sortBy[int(input("Choose how you want to sort: ")) - 1]
            elif sort_upperDown:
                select = sortDir[int(input("Choose between ascending and descending order: ")) - 1]
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
            moving_dir = None
            copying_dir = None
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
        elif "Delete" in select:
            deleteFile()
            selected_dir = None
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
            sort_upperDown = True
        elif "Name" in select:
            current_dir.cur_sort = 1
            sort_selection = False
            sort_upperDown = True
        elif "Extension" in select:
            current_dir.cur_sort = 2
            sort_selection = False
            sort_upperDown = True
        elif select == "Ascending Order":
            current_dir.cur_dir = True
            sort_upperDown = False
        elif select == "Descending Order":
            current_dir.cur_dir = False
            sort_upperDown = False
        elif "Search" in select:
            searchFile()
