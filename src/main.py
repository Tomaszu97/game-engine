from game import *
import os

os.chdir(os.path.dirname(sys.argv[0]))

if __name__ == "__main__" :
	theApp = App()
	theApp.on_execute()
 