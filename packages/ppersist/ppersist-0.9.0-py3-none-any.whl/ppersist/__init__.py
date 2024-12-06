#!/usr/bin/python3


## ppersist - easy saving and reloading of complex data
## Copyright (C) 2024  Daniel A. Wagenaar
## 
## This program is free software: you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""There are many ways to save data from python for future use, but none
are quite as convenient as Matlab and Octave’s “save””:

    save filename.mat variableA variableB ...
    
which saves the named variables directly to a file. The corresponding

    load filename.mat
    
reloads the saved variables and dumps them into the global namespace.

This packages offers the closest pythonic equivalent. With it, you can write

    ppersist.save("filename.pkl", variableA, variableB, ...)
    
to save some variables, and

    data = ppersist.load("filename.pkl")
    
to reload them into a `namedtuple`. """


from .ppersist import *

