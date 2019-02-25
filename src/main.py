#!/usr/bin/env python3
import	os
import	sys
from	game	import	*



os.chdir(os.path.dirname(sys.argv[0]))

if __name__ == "__main__" :
	theApp = App()
	theApp.on_execute()
 