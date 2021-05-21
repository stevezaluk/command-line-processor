import os, sys, time, datetime
from random import randint
from datetime import date
"""
    Abstraction of an inode (index node)

    Index Nodes represent file system objects such as directories and files.
    Index nodes store file metadata like the inode id, creation/modified time,
    its user and groups and also its permssions
"""
class inode(object):
    def __init__(self):
        self.id = randint(100, 999)
        self.creation_time = datetime.datetime.now()
        self.user = 'user'
        self.group = 'group'

"""
    Abstraction of a directory

    The names of this directories, files and subdirectories are stored within the map variable as index nodes do not store file names
    A directory is nothing more than a list of file names pointing to there corresponding index node id's

    name (str) : The name of your directory
    parent (Directory) : The parent of this directory
    map (dict) : The map of the directory (filename:node) with node being an inode object
"""
class Directory(inode):
    def __init__(self, name, parent):
        inode.__init__(self)
        self.name = name
        self.parent = parent
        self.map = {".":self, "..":parent}

"""
    Abstraction of a file
"""
class File(inode):
    def __init__(self):
        inode.__init__(self)

"""
    Main Command Line processor
"""
class CLI(object):
    def __init__(self):
        self.current_dir = Directory('/', None) # the root directory

    def usage(self):
        print('help : Displays this text')
        print('exit : Exit the CLI')
        print('ls : List directory structure')
        print('pwd : List your present working directory')
        print('cd DIRECTORY : Change your directory')
        print('mkdir NAME : Create a directory')
        print('touch NAME : Create a file')
        print('rm NAME : Remove a directory or file')

    def list_structure(self, recursive=False):
        for x in self.current_dir.map:
            inode = self.current_dir.map[x]
            if inode is None:
                pass
            else:
                print('{id} {u}  {g}    {ct}  {n}'.format(id=inode.id, u=inode.user, g=inode.group, ct=inode.creation_time, n=x))

    def change_directory(self, directory):
        found = False
        for dir in self.current_dir.map:
            if dir == '..' and self.current_dir.parent is None: # account for the root directory not having a parent
                pass
            elif dir == directory:
                found = True
                self.current_dir = self.current_dir.map[dir]

        if found is False:
            print('[!] cd: directory not found: ', directory)

    def mkdir(self, name, parent):
        d = Directory(name, parent)
        self.current_dir.map.update({"{}".format(d.name):d})

    def touch(self, name):
        f = File()
        self.current_dir.map.update({"{}".format(name):f})

    def remove(self, name):
        found_file = False
        for inode in self.current_dir.map:
            if inode == name:
                found_file = True

        if found_file:
            self.current_dir.map.pop(name)
            print('Removed: {}'.format(name))
        elif found_file is False:
            print('[!] inode does not exist')

    def check_cli_arguments(self, args):
        if len(args) == 0:
            print('[!] Cant check list with no items')
        elif len(args) < 2:
            print('[!] not enough arguments for {}'.format(args[0]))

    def main(self):
        print('--- Welcome ---')
        while True:
            read = input('{} $ '.format(self.current_dir.name))
            read = read.split(' ')
            if read[0] == 'exit' or read[0] == 'quit':
                print('--- Goodbye ---')
                sys.exit(0)
            elif read[0] == 'help':
                self.usage()
            elif read[0] == 'mkdir':
                if len(read) < 2:
                    print('[!] not enough arguments for mkdir (need 1)')
                else:
                    self.mkdir(read[1], self.current_dir)
            elif read[0] == 'touch':
                if len(read) < 2:
                    print('[!] not enough arguments for touch (need 1)')
                else:
                    self.touch(read[1])
            elif read[0] == 'ls':
                self.list_structure()
            elif read[0] == 'pwd':
                print('PWD: ', self.current_dir.name)
            elif read[0] == 'cd':
                if len(read) < 2:
                    print('[!] not enough arguments for cd (need 1)')
                else:
                    self.change_directory(read[1])
            elif read[0] == 'rm':
                if len(read) < 2:
                    print('[!] not enough arguments for rm (need 1)')
                else:
                    self.remove(read[1])
            else:
                print('[!] command not found: ', read[0])

if __name__ == '__main__':
    c = CLI()
    c.main()
