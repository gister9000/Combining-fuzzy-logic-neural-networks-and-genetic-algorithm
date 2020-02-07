import sys
from tkinter import *
import numpy
import matplotlib.pyplot as plt


root = Tk()
c = Canvas(root, bg='white', width=600, height=600)
c.grid(row=1, columnspan=5)
logging = 0
log = []
final = []
previous = None

def motion(event):
    global log
    global previous
    x, y = event.x, event.y
    if logging == 1:
        log.append([x,y])
        string = '{}, {}'.format(x, y)
        print(string)
        if previous:
            c.create_line(previous[0], previous[1], x, y)
def startlog(event):
    global logging
    global log
    global final
    logging = 1
    log = []
    final = []

def stoplog(event):
    global logging 
    global log
    global final
    logging = 0
    
    # calculate arithmetic mean for translation
    Tcx = 0.0
    Tcy = 0.0
    for dot in log:
        Tcx += dot[0]
        Tcy += dot[1]
    Tcx = Tcx / len(log)
    Tcy = Tcy / len(log)
    
    # subtract Tcx and Tcy from each dot in log
    for dot in log:
        dot[0] -= Tcx
        dot[1] -= Tcy
        
    # marking max x and max y coordinate for scaling
    mx = 0.0
    my = 0.0
    m = 0.0
    for dot in log:
        mx = max(abs(dot[0]), mx)
        my = max(abs(dot[1]), my)
    m = max(mx, my)
    
    # scale all coordinates to [-1, 1]
    for dot in log:
        dot[0] /= m
        dot[1] /= m
   
    # calculate total length of translated and scaled drawing
    D = 0.0
    prev = None
    distances = []
    for dot in log:
        if prev:
            D += numpy.sqrt( (dot[1]-prev[1])**2 + (dot[0]-prev[0])**2 )
            distances.append(D)
        prev = dot
        
    # number of representative dots
    M = int(sys.argv[1])
    k_length = lambda k: k * D / (M+1)
    
    for i in range(M):
        k_distance = k_length(i)
        closest = min(distances, key = lambda x: abs(x-k_distance))      
        final.append(log[distances.index(closest)])
              
    x = []
    y = []
    logfile = open(sys.argv[2], "w")
    for dot in final:            
        logfile.write(str(dot[0]) + " " + str(dot[1]) + "\n")
        x.append(dot[0])
        y.append(dot[1])
    logfile.close()
    plt.plot(x,y, 'o')
    plt.show()
    exit(0)
    #log = []
    #final = []
c.bind("<Button-1>", startlog)
c.bind('<ButtonRelease-1>', stoplog)
root.bind('<Motion>', motion)
root.mainloop()
