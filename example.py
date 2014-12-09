import lsystem

#create new system system
system = lsystem.LSystem()

#sets the amount of times to recursively draw
system.nvalue = 8
#method that takes the input and output files names, and then automatically draws the system
system.executeSystem("systems/striangle.lsys","scripts/striangle.py")