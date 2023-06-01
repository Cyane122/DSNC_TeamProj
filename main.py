import math
import time
import random

"""
" TODO-THINGS
" 1. UPDATE FILE/FOLDER
" 2. Init()
" 3. 실제로 돌려보면서 오류 최대한 찾아서 고쳐보기!
"""


UUID_LIST: list = [False for i in range(1000000)]  # To prevent UUID duplication...


def newUUID():
    uuid = math.floor(random.random() * 1000000)
    while UUID_LIST[uuid]:
        uuid = math.floor(random.random() * 1000000)
    UUID_LIST[uuid] = True
    return uuid


class File:

    def __init__(self, name, prev, extension, time, UUID):
        self.name: str = name
        self.prev: Folder = prev
        self.time = time
        self.extension: str = extension
        self.UUID = UUID

    def getName(self):
        if self.extension == "dir":
            return self.name
        else:
            return self.name + "." + self.extension

    def getLocation(self):
        if self.extension == "dir":
            loc = self.name
        else:
            loc = self.name + "." + self.extension
        file: File = self
        while file.prev is not None:
            file: Folder = file.prev
            if file.extension == "dir":
                t: str = file.name
            else:
                t: str = file.name + "." + file.extension
            loc = t + "\\" + loc

        return loc

    def getType(self):
        if self.extension == "dir":
            return "Folder"
        else:
            return f".{self.extension} file"


class Folder(File):
    def __init__(self, name, prev):
        super().__init__(name, prev, "dir", time.localtime(), newUUID())
        self.contents: list = []
        self.cur_sort = 0  # cur_sort: 0 -> Created Time / 1 -> Name / 2 -> Extension
        self.order = True  # order: True -> Ascending Order / False -> Descending Order

    def addFile5(self, name, extension, time, UUID):
        file = File(name, self, extension, time, UUID)
        tmpFile = file
        if not self.containsName(file):
            self.contents.append(file)
            return
        k = 1
        while self.containsName(file):
            file = File(tmpFile.name + " (" + str(k) + ")", self, file.extension)
            k += 1
        self.contents.append(file)

    def addFolder5(self, name):
        file = Folder(name, self)
        tmpFile = file
        if not self.containsName(file):
            self.contents.append(file)
            return
        k = 1
        while self.containsName(file):
            file = File(tmpFile.name + " (" + str(k) + ")", self, file.extension, time.localtime(), newUUID())
            k += 1
        self.contents.append(file)

    def addFolder(self, folder):
        self.contents.append(folder)

    def addFile(self, addFile):
        if addFile.extension == "dir":
            self.addFolder5(addFile.name)
        else:
            self.addFile5(addFile.name, addFile.extension, addFile.time, addFile.UUID)

    def containsName(self, item):
        for _ in self.contents:
            if _.name == item.name and _.extension == item.extension:
                return True
        return False

    def contains(self, item):
        if len(self.contents) == 0:
            return False
        for _ in self.contents:
            if _.UUID == item.UUID:
                return True
        return False

    def sort(self):
        if self.cur_sort == 0:  # Created Time
            self.contents.sort(key=lambda x: x.time, reverse=(not self.order))
        elif self.cur_sort == 1:  # Name
            self.contents.sort(key=lambda x: x.name, reverse=(not self.order))
        elif self.cur_sort == 2:  # Extension
            self.contents.sort(key=lambda x: x.extension, reverse=(not self.order))


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
    temp: File = selected_dir
    select = int(input(f"[ Delete File ] Are you sure to delete ${temp.getName()}? If not, input 1: "))
    if select == 1:
        return
    cur: File = current_dir
    while cur.prev is not None:
        cur = cur.prev
        if cur == selected_dir:
            print("[ Delete File ] The folder you currently belong to cannot be deleted!")
            time.sleep(0.7)
            return
    selected_dir.prev.contents.remove(selected_dir)
    selected_dir.prev = None


def searchFile():
    search = input("[ Search File/Folder ] Enter the name or extension of the file you are looking for: ")
    searchList = []
    q: list = [root]
    if "." in search:  # If input has "Extension"
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
        if name == "*" and extension != "*":
            while len(q) != 0:
                if q[0].extension == extension:
                    searchList.append(q[0])
                if q[0].extension == "dir":
                    for d in q[0].contents:
                        q.append(d)
                q.pop(0)
        elif extension == "*" and name != "*":
            while len(q) != 0:
                if q[0].name == name:
                    searchList.append(q[0])
                if q[0].extension == "dir":
                    for d in q[0].contents:
                        q.append(d)
                q.pop(0)
        elif extension == "*" and name == "*":
            while len(q) != 0:
                searchList.append(q[0])
                if q[0].extension == "dir":
                    for d in q[0].contents:
                        q.append(d)
                q.pop(0)
        else:
            while len(q) != 0:
                if q[0].name == name and q[0].extension == extension:
                    searchList.append(q[0])
                if q[0].extension == "dir":
                    for d in q[0].contents:
                        q.append(d)
                q.pop(0)
    else:  # not Extension
        name = search
        while len(q) != 0:
            if name in q[0].name or name in q[0].extension:
                searchList.append(q[0])
            if q[0].extension == "dir":
                for d in q[0].contents:
                    q.append(d)
            q.pop(0)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("==============================================================")
    print("Search Result - %s - %d found " % (search, len(searchList)))
    print("==============================================================")
    idx: int = 65  # chr(idx) = 'A'
    for k in dic.keys():
        dic[k] = None

    if len(searchList) == 0:
        print("Didn't find anything...")
    else:
        for d in searchList:
            dic[idx]: File = d
            print(f"[ {chr(idx)} ] {d.getName():17s} {d.getLocation()}")
            idx += 1
    print("==============================================================")
    LIST = ["Select File/Folder", "Go back"]
    idx = 1
    while idx <= len(LIST):
        print("[ %02d ] %s" % (idx, LIST[idx - 1]))
        idx += 1
    select = LIST[int(input("Choose what you want to do: ")) - 1]
    if select == "Select File/Folder":
        tmp = selectFile()
        if tmp is not None:
            global selected_dir
            selected_dir = tmp
            global current_dir
            current_dir = tmp.prev
    elif select == "Go back":
        return


def renameFile():
    print("[ Rename File/Folder ] Alert! You can ONLY change file name, not extension!")
    change_name = input("[ Rename File/Folder] Enter the name of the file/folder you want to change. By entering"
                        " nothing, you can cancel the change: ")
    if len(change_name) == 0:
        return
    selected_dir.name = change_name
    selected_dir.time = time.localtime()


def init():
    temp: Folder = Folder("temp", root)
    folder2020: Folder = Folder("2020", root)
    root.addFolder(temp)
    root.addFolder(folder2020)
    t: File = File("t", root, "txt", time.localtime(), newUUID())
    microsoft: Folder = Folder("Microsoft", root)
    root.addFolder(microsoft)
    root.addFile(t)
    desktop: File = File("desktop", root, "jpg", time.localtime(), newUUID())
    mainFolder: Folder = Folder("mainFolder", temp)
    temp.addFolder(mainFolder)
    temp.addFile(desktop)
    commonFiles: Folder = Folder("common files", microsoft)
    microsoft.addFolder(commonFiles)

# 선택된 파일은 다른 폴더로 이동하면 그 선택이 취소됨. 복사나 이동할 거면 그 위치에서 하기.


if __name__ == "__main__":  # PROGRAM MAIN
    init()
    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        LIST = ["Create File", "Create Folder", "Search File/Folder"]
        select = 0
        if selected_dir is not None and selected_dir.prev != current_dir:
            selected_dir = None
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
                    LIST.append("Copy Folder")
                    LIST.append("Move Folder")
                    LIST.append("Rename %s" % selected_dir.name)
                    LIST.append("Delete " + selected_dir.name)
            else:
                if current_dir.contains(selected_dir):
                    LIST.append("Unselect File")
                    LIST.append("Copy File")
                    LIST.append("Move File")
                    LIST.append("Rename %s.%s" % (selected_dir.name, selected_dir.extension))
                    LIST.append("Delete " + selected_dir.name + "." + selected_dir.extension)

        if current_dir.prev is not None:
            LIST.append("Goto " + current_dir.prev.name)

        if current_dir.order:
            tmp = "Ascending"
        else:
            tmp = "Descending"

        LIST.append("Sort by: %s - %s" % (sortBy[current_dir.cur_sort], tmp))
        current_dir.sort()

        LIST.append("Quit")

        print("==============================================================")
        print("Python File Manager")
        print("Current Directory: ", current_dir.getLocation())
        if selected_dir is not None:
            if selected_dir.extension == "dir":
                print("Selected Folder:", selected_dir.getLocation())
            else:
                print("Selected File:", selected_dir.getLocation())
        if copying_dir is not None:
            print("<< Copying", copying_dir.getLocation(), ">>")
        if moving_dir is not None:
            print("<< Moving", moving_dir.getLocation(), ">>")
        print("==============================================================")
        idx: int = 65  # chr(idx) = 'A'

        for k in dic.keys():
            dic[k] = None

        if len(current_dir.contents) == 0:
            print("this folder is empty...")
        else:
            for d in current_dir.contents:
                dic[idx]: File = d
                print(f"[ {chr(idx)} ]  {d.getName():17s} ", end="")
                now = d.time
                print("%04d/%02d/%02d %02d:%02d:%02d" % (
                    now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec), end = "")
                print(f"    {d.getType()}")
                idx += 1
        print("==============================================================")
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
            current_dir.addFile(File(copying_dir.name, current_dir, copying_dir.extension, time.localtime(), newUUID()))
        elif "Move" in select:
            current_dir.addFile(File(moving_dir.name, current_dir,
                                     moving_dir.extension, time.localtime(), moving_dir.UUID))
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
            current_dir.order = True
            sort_upperDown = False
            current_dir.time = time.localtime()
        elif select == "Descending Order":
            current_dir.order = False
            sort_upperDown = False
            current_dir.time = time.localtime()
        elif "Search" in select:
            searchFile()
        elif "Rename" in select:
            renameFile()
        elif select == "Quit":
            break
