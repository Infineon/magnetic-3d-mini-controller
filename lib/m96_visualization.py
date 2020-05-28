# This package uses tk to create a simple graphical
#   output representing the iDrive state

import tkinter as tk
import numpy as np


#  why not use the numpy native? but whatever
def rotate_2D(vector, angle):
    r = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
    return r.dot(vector)


# this class intializes the canvas and all geometrical
#  objets drawn onto it. The method setState simply
#  adjusts the color of the respective objects
class IDriveVisualizer:

    def __init__(self,root):
        self.root = root
        self.state = [0,0]

        cnvs_height = 400
        cnvs_width = 400
        rect_cn = (400,400)
        rect_c = (80,80)

        BG = '#F5F5DC'

        self.cnvs = tk.Canvas(self.root, bg=BG, height=cnvs_height, width=cnvs_width)
        self.cnvs.pack()

        delta = 20.
        x1a,y1a,x2a,y2a,x3a,y3a = 150.0+delta, 150.0, 200.0, 100.0+delta, 250.0-delta, 150.0
        x1b,y1b,x2b,y2b,x3b,y3b = 150.0+delta, 250.0, 250.0-delta, 250.0, 200.0, 300.0-delta
        x1c,y1c,x2c,y2c,x3c,y3c = 250.0, 150.0+delta, 300.0-delta, 200.0, 250.0, 250.0-delta
        x1d,y1d,x2d,y2d,x3d,y3d = 100.0+delta, 200.0, 150.0, 150.0+delta, 150.0, 250.0-delta

        SB1 = '#CCCCCC'
        C0 = '#8B8878'

        self.h_arrow = [
            self.cnvs.create_oval(0,0,0,0,fill='blue'),
            self.cnvs.create_polygon(x1a,y1a,x2a,y2a,x3a,y3a,fill=SB1,outline=C0,width=1),
            self.cnvs.create_polygon(x1b,y1b,x2b,y2b,x3b,y3b,fill=SB1,outline=C0,width=1),
            self.cnvs.create_polygon(x1c,y1c,x2c,y2c,x3c,y3c,fill=SB1,outline=C0,width=1),
            self.cnvs.create_polygon(x1d,y1d,x2d,y2d,x3d,y3d,fill=SB1,outline=C0,width=1),
            self.cnvs.create_oval(200-rect_c[1]/2.,200-rect_c[0]/2.,200+rect_c[1]/2.,200+rect_c[0]/2.,fill=SB1,outline=C0,width=1)]

        r = 120
        d = 16
        self.h_circle = []

        for i in range(0,72):
            x1 = rect_cn[1]/2. + rotate_2D([0,-r], i*2*np.pi/72)[0] - d/2.
            y1 = rect_cn[0]/2. + rotate_2D([0,-r], i*2*np.pi/72)[1] - d/2.
            x2 = rect_cn[1]/2. + rotate_2D([0,-r], i*2*np.pi/72)[0] + d/2.
            y2 = rect_cn[0]/2. + rotate_2D([0,-r], i*2*np.pi/72)[1] + d/2.
            self.h_circle.append(self.cnvs.create_oval(x1, y1, x2, y2, fill=SB1,outline=C0,width=1))


    def setState(self, state):
        SB1 = '#CCCCCC'
        RED = '#FF3030'
        GREEN = '#9acd32'

        if self.state[0] != state[0]:
            self.cnvs.itemconfig(self.h_arrow[self.state[0]],fill = SB1)
            self.cnvs.itemconfig(self.h_arrow[state[0]],fill = GREEN)
            self.state[0] = state[0]

        if self.state[1] != state[1]:
            self.cnvs.itemconfig(self.h_circle[self.state[1]],fill = SB1)
            self.cnvs.itemconfig(self.h_circle[state[1]],fill = RED)
            self.state[1] = state[1]
