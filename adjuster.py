#!/usr/bin/python
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

"""A class collection to provide GUI control of the parameters of a process."""


import sys
import Tkinter as tk

__author__ = 'David Talkin (dtalkin@gmail.com)'


class ParSpec(object):
    """Provides a container for specification of control parameters."""

    def __init__(self, name='', val_type='int', low_limit=0, hi_limit=100,
                 option='', callback=None, initial_value=None):
        self.name = name
        self.val_type = val_type
        self.lo_limit = low_limit
        self.hi_limit = hi_limit
        self.option = option
        self.callback = callback
        self.initial_value = initial_value
        self.scale = None
        if self.val_type == 'int':
            self.var = tk.IntVar()
        else:
            self.var = tk.DoubleVar()


class Adjuster(object):
    """Provides a panel of sliders for control of parameter values."""

    def __init__(self, master=None, par_specs=None, orient=tk.VERTICAL,
                 length=200, title='Parameters', slider_width=15):
        """Instantiates an Adjuster frame and optionaly creates scales.
        """
        if master is not None:
            self.master = master
        else:
            self.master = tk.Tk()
        self.master.title(title)
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.orient = orient
        self.length = length
        self.slider_width = slider_width
        self.par_specs = par_specs
        self.par_dic = {}
        if self.par_specs:
            self.BuildScales(self.par_specs)

    def Respond(self, unused_value, scale=None):
        """Responds to a slider change command (event driven).
        """
        par = self.par_dic[scale]
        if __name__ == '__main__':
            print par.option, par.var.get()
        if par.callback:
            par.callback(par.var.get())

    def BuildScales(self, par_specs):
        """Set up the scales specified,in the par_specs list.
        """
        for par in par_specs:
            res = abs((par.hi_limit - par.lo_limit) / self.length)
            if par.initial_value is None:
                preset = (par.lo_limit + par.hi_limit) / 2.0
            else:
                preset = par.initial_value
            par.var.set(preset)
            par.scale = tk.Scale(self.frame, label=par.name, variable=par.var,
                                 from_=par.lo_limit, to=par.hi_limit,
                                 orient=self.orient, length=self.length,
                                 width=self.slider_width, resolution=res)
            par.scale.configure(command=lambda val, scale=par.scale:
                                self.Respond(val, scale))
            self.par_dic.update({par.scale: par})
            if self.orient == tk.VERTICAL:
                par.scale.pack(side=tk.LEFT)
            else:
                par.scale.pack(side=tk.TOP)


def Junk(val):
    """A dummy callback that is called when a scale slider moves.
    """
    print 'val is:', val


def Main(unused_args):
    """Demonstration test harness for the Adjuster.
    """
    root = tk.Tk()
    pars = [ParSpec('foo', 'int', 400, 0, 'foobar'),
            ParSpec('fie', 'double', 45., 1.5, 'fiebar'),
            ParSpec('bar', 'double', 0.5, 0.1, 'barbar', Junk)]
    unused_ = Adjuster(root, pars, orient=tk.HORIZONTAL)
    root.mainloop()


if __name__ == '__main__':
    Main(sys.argv)
