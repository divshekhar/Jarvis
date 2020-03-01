import os
import subprocess as sp


class CommandPrompt:

    def cwd(self):
        result = os.getcwd()
        directory = ''
        for i in result:
            directory = directory + i
            if i == '\\':
                directory = ''

        disk = result[0]
        return (disk, directory,)
