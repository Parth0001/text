import sys

print 'entry console'
with open(sys.argv[1], 'w') as file:
    for command in iter(lambda: raw_input('>>> '), ''):
        print ''.join(reversed(command)) # do something with it
        print >>file, command # pass the command to view window
        file.flush()
