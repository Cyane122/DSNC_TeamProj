from datetime import datetime


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

    def getDisplayName(self):
        return self.name + "." + self.extension


class Folder(File):
    def __init__(self, name, prev):
        super().__init__(name, prev, "dir")
        self.contents = []

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


if __name__ == "__main__":

    root = Folder("root", None)
    current_dir = root
    selected_dir = root

    while True:

        LIST = ["Create File",
                "Create Folder"
                ]
        if selected_dir is None:
            LIST.append("Select File/Folder")
        else:
            LIST.append("Deselect File/Folder")
        select = 0

        print("==========================================")
        print("Python File Manager")
        print("Current Direction: ", current_dir.getLocation())

        if selected_dir is not None:
            print("Selected Direction:", current_dir.getLocation())

        print("==========================================")
        print(current_dir.getDisplayName())
        for _file_ in current_dir.contents:
            print(" ㄴ", _file_.getDisplayName())
        print("==========================================")

        tmp = 1
        for k in LIST:
            print("[", tmp, "]", k)
            tmp += 1

        select = (input("Choose what you want to do: "))

        if select == "1":
            _input_ = input("[ Create File ] Insert your file name with extension (e.g. file.jpg): ")
            extension, name = "", ""
            tmp = False
            for c in _input_:
                if c == '.':
                    tmp = True
                    continue

                if tmp:
                    extension = extension + c
                else:
                    name = name + c

            file = File(name, current_dir, extension)
            k = 1
            tmp = False
            while current_dir.contains(file):
                tmp = True
                file = File(name + " (" + str(k) + ")", current_dir, extension)
                k += 1

            if tmp:
                print("[ Create File ] Duplicate file name: File name is changed into", file.getDisplayName())
            current_dir.addFile(file)

        elif select == "2":
            name = input("[ Create Folder ] Insert your file name (e.g. folder): ")

            folder = Folder(name, current_dir)
            k = 1
            tmp = False
            while current_dir.contains(folder):
                tmp = True
                folder = Folder(name + " (" + str(k) + ")", current_dir)
                k += 1

            if tmp:
                print("[ Create Folder ] Duplicate folder name: folder name is changed into", folder.name)

            current_dir.addFile(folder)

        elif select == "3":
            print("Select File/Folder")
