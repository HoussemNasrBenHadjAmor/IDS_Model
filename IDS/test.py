import sys
import datetime
import os
# Check if at least two arguments are provided (script name is the first argument)
if len(sys.argv) >= 3:
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
    arg4 = sys.argv[4]
    arg5 = sys.argv[5]
    print("Argument 1:", arg1)
    print("Argument 2:", arg2)
    print("Argument 3:", arg3)
    print("Argument 4:", arg4)
    print("Argument 5:", arg5)

else:
    print("Please provide at least two command-line arguments.")
