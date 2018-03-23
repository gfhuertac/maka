import os
import sys

def executer(fileName):
    file = open(fileName,'r')
    for line in file:
        os.system("python author.py -a '%s'" % line)
    file.close()

def checker(fileName):
    splited = fileName.split('.')
    if splited[-1]=='txt':
        return True
    return False



def main():
    if(len(sys.argv) == 2):
        fileName = sys.argv[1]
        if(checker(fileName)):
            executer(fileName)
    else:
        print("""
        Command of use: python multiples_author.py nameOfFile.txt
        Where the name of file have to have an author per line.
        """)
if __name__ == "__main__":
    main()
