import sys

def pytail(arguments):
    with open(arguments[0]) as f:
        if len(arguments) > 1 :
            lines = f.readlines() [-int(arguments[1]):]
            
        else:
            lines = f.readlines() [-10:]
    
    for line in lines:
        print(line)
        
pytail(sys.argv[1:])