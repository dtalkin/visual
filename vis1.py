#!/usr/bin/python

"""
A program to create the illusion of motion by modulating contrast and color.

See:  https://journals.sagepub.com/doi/full/10.1177/2041669518815708
"""
#
#
# Copyright 2019 David Talkin.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import math
import time
import threading
import Tkinter as tk
from adjuster import ParSpec, Adjuster

__author__ = 'dtalkin@gmail.com (David Talkin)'


class Ill_1(object):
    def __init__(self, rate=2.0, height=600, width=600, fill_factor=0.7,
                 modulated_rgb=[200, 128, 128], static_rgb=[0, 96, 96],
                 depth=0.3, border_width=2):
        self.root = tk.Tk()
        self.root.title('Perpetual Diamond')
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame, height=height, width=width,
                                background='grey')
        self.canvas.pack()
        self.width = width
        self.height = height
        self.fill_factor = fill_factor
        self.modulated_rgb = modulated_rgb
        self.static_rgb = static_rgb
        self.depth = depth
        self.border_width = border_width
        self.rate = rate
        self.poly = self.CreatePoly(self.Num2Color(self.static_rgb))
        self.s1_phase = -90.0
        self.s2_phase = 90.0
        self.s3_phase = 90.0
        self.s4_phase = -90.0
        self.side1 = None
        self.side2 = None
        self.side3 = None
        self.side4 = None
        self.t0 = time.time()
        self.running = False
        self.CreateAdjuster()

    def SetS1(self, val):
        self.s1_phase = val * math.pi / 180.0
        
    def SetS2(self, val):
        self.s2_phase = val * math.pi / 180.0
        
    def SetS3(self, val):
        self.s3_phase = val * math.pi / 180.0
        
    def SetS4(self, val):
        self.s4_phase = val * math.pi / 180.0

    def SetRate(self, val):
        self.rate = val
        
    def SetDepth(self, val):
        self.depth = val

    def SetStatR(self, val):
        self.static_rgb[0] = val
        self.UpdatePoly()

    def SetStatG(self, val):
        self.static_rgb[1] = val
        self.UpdatePoly()

    def SetStatB(self, val):
        self.static_rgb[2] = val
        self.UpdatePoly()

    def SetModR(self, val):
        self.modulated_rgb[0] = val

    def SetModG(self, val):
        self.modulated_rgb[1] = val

    def SetModB(self, val):
        self.modulated_rgb[2] = val

    def SetBorderWidth(self, val):
        self.border_width = int(val)

    def UpdatePoly(self):
        self.canvas.delete(self.poly)
        self.poly = self.CreatePoly(self.Num2Color(self.static_rgb))
        
    def CreateAdjuster(self):
        pars = [ParSpec('Side 1', 'float', -90, 90, callback=self.SetS1,
                        initial_value=self.s1_phase),
                ParSpec('Side 2', 'float', -90, 90, callback=self.SetS2,
                        initial_value=self.s2_phase),
                ParSpec('Side 3', 'float', -90, 90, callback=self.SetS3,
                        initial_value=self.s3_phase),
                ParSpec('Side 4', 'float', -90, 90, callback=self.SetS4,
                        initial_value=self.s4_phase),
                ParSpec('Rate (Hz)', 'float', 0.5, 4.0, callback=self.SetRate,
                        initial_value=self.rate),
                ParSpec('Contrast', 'float', 0.0, 1.0, callback=self.SetDepth,
                        initial_value=self.depth),
                ParSpec('Static Red', 'float', 0.0, 255.0,
                        callback=self.SetStatR,
                        initial_value=self.static_rgb[0]),
                ParSpec('Static Green', 'float', 0.0, 255.0,
                        callback=self.SetStatG,
                        initial_value=self.static_rgb[1]),
                ParSpec('Static Blue', 'float', 0.0, 255.0,
                        callback=self.SetStatB,
                        initial_value=self.static_rgb[2]),
                ParSpec('Dynamic Red', 'float', 0.0, 255.0,
                        callback=self.SetModR,
                        initial_value=self.modulated_rgb[0]),
                ParSpec('Dynamic Green', 'float', 0.0, 255.0,
                        callback=self.SetModG,
                        initial_value=self.modulated_rgb[1]),
                ParSpec('Dynamic Blue', 'float', 0.0, 255.0,
                        callback=self.SetModB,
                        initial_value=self.modulated_rgb[2]),
                ParSpec('Border Width', 'float', 0, 10,
                        callback=self.SetBorderWidth,
                        initial_value=self.border_width),
        ]
        self.adjuster = Adjuster(tk.Toplevel(), pars, tk.HORIZONTAL, 400,
                                 'Display Parameters', 10)
                
    def CreatePoly(self, color):
        x1,x2,x3,y1,y2,y3 = self.CreateVertices()
        return self.canvas.create_polygon(x1, y2, x2, y1, x3, y2, x2, y3,
                                       fill=color)
    
    def CreateVertices(self):
        x1 = int(0.5 + (self.width * (1.0 - self.fill_factor)))
        x2 = int(0.5 + (self.width * 0.5))
        x3 = int(0.5 + (self.width * self.fill_factor))
        y1 = int(0.5 + (self.height * (1.0 - self.fill_factor)))
        y2 = int(0.5 + (0.5 * self.height))
        y3 = int(0.5 + (self.height * self.fill_factor))
        return x1,x2,x3,y1,y2,y3
        
    def Num2Color(self, num):
        n = [min(255, int(0.5 + a)) for a in num]
        return ('#%2x%2x%2x' % (n[0],n[1],n[2])).replace(' ','0')
    
    def Run(self):
        x1,x2,x3,y1,y2,y3 = self.CreateVertices()
        while self.running:
            t1 = time.time()
            arg = self.rate * 2.0 * math.pi * (t1 - self.t0)
            fact = 0.5 - (0.5 * self.depth * math.cos(arg))
            rgb = [c * fact for c in self.modulated_rgb]
            color = self.Num2Color(rgb)
            self.canvas.configure(background=color)
            w = self.border_width  # border width in pixels
            if w <= 0:
                if self.side1:
                    self.canvas.delete(self.side1, self.side2, self.side3,
                                       self.side4)
                    self.side1 = self.side2 = self.side3 = self.side4 = None
            else:
                fact = 0.5 - (0.5 * self.depth * math.cos(arg + self.s1_phase))
                rgb = [c * fact for c in self.modulated_rgb]
                color = self.Num2Color(rgb)
                self.canvas.delete(self.side1)
                self.side1 = self.canvas.create_line(x1, y2, x2, y1, fill=color,
                                                     width=w)
                fact = 0.5 - (0.5 * self.depth * math.cos(arg + self.s2_phase))
                rgb = [c * fact for c in self.modulated_rgb]
                color = self.Num2Color(rgb)
                self.canvas.delete(self.side2)
                self.side2 = self.canvas.create_line(x2, y1, x3, y2, fill=color,
                                                     width=w)
                fact = 0.5 - (0.5 * self.depth * math.cos(arg + self.s3_phase))
                rgb = [c * fact for c in self.modulated_rgb]
                color = self.Num2Color(rgb)
                self.canvas.delete(self.side3)
                self.side3 = self.canvas.create_line(x3, y2, x2, y3, fill=color,
                                                     width=w)
                fact = 0.5 - (0.5 * self.depth * math.cos(arg + self.s4_phase))
                rgb = [c * fact for c in self.modulated_rgb]
                color = self.Num2Color(rgb)
                self.canvas.delete(self.side4)
                self.side4 = self.canvas.create_line(x2, y3, x1, y2, fill=color,
                                                     width=w)
            elapsed = time.time() - t1
            if 0.04 - elapsed > 0:  # 0.04 produces 25 frames per second.
                time.sleep(0.04 - elapsed)
            
    def Start(self):
        self.thread = threading.Thread(group=None, target=self.Run)
        self.thread.daemon = True
        self.running = True
        self.thread.start()
        

def Main(unused_arg):
    ill = Ill_1()
    ill.Start()
    tk.mainloop()


if __name__ == '__main__':
    Main(sys.argv)
