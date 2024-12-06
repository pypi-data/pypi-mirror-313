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
## You should have received a copy of the GNU General Public License along
## with this program.  If not, see <https://www.gnu.org/licenses/>.


import numpy as np
import pandas as pd
import pickle
import inspect
import re
import collections
from typing import NamedTuple, Dict, Any


__all__ = ["cansave", "save", "savedict", "load", "loaddict", "mload", "Saver", "fetch", "savedict_ignorewhitelist"]


def cansave(v: Any) -> bool:
    '''CANSAVE - Can a given object be saved by PPERSIST?
    CANSAVE(v) returns True if V can be saved by PPERSIST.

    Currently, PPERSIST can save:

      - None
      - Simple numbers (int, float, complex)
      - Strings
      - Numpy arrays (but not containing object)
      - Pandas dataframes and series (ditto)
      - Lists, tuples, sets, and dicts containing those (even hierarchically).

    Importantly, PPERSIST cannot save objects of arbitrary class or
    function type. 

    PPERSIST will not attempt to load types it cannot save. This is
    intended to protect PPERSIST against the well-documented security
    problems of the underlying pickle module.'''
    if v is None:
        return True
    t = type(v)
    if t==np.ndarray and v.dtype!=object:
        return True
    if t==str:
        return True
    if t==int or t==np.int32 or t==np.int64 \
       or t==float or t==np.float64 or t==np.float32 \
       or t==complex or t==np.complex128 or t==np.complex64 \
       or t==np.bool_ or t==np.intc or t==bool:
        return True
    if t==dict:
        for k,v1 in v.items():
            if not cansave(v1):
                return False
        return True
    if t==list or t==tuple or t==set:
        for v1 in v:
            if not cansave(v1):
                return False
        return True
    if t == pd.DataFrame or t == pd.Series:
        for v1 in v:
            if not cansave(v1):
                return False
        return True

    print(f'Cannot save {t}')
    return False


def save(filename: str, *args: Any) -> None:
    '''SAVE - Save multiple variables in one go as in Octave/Matlab

    SAVE(filename, var1, var2, ..., varN) saves each of the variables
    VAR1...VARN into a single PICKLE file.

    See LOAD, LOADDICT, and MLOAD for how to reload saved data.

    Only variables that can safely be reloaded will be saved.
    Currently, PPERSIST can save:

      - None
      - Simple numbers (int, float, complex)
      - Strings
      - Numpy arrays (but not containing object)
      - Pandas dataframes and series (ditto)
      - Lists, tuples, sets, and dicts containing those (even hierarchically).

    Importantly, PPERSIST will not save objects of arbitrary class or
    function type.

    To check whether a variable is saveable ahead of time, use CANSAVE.
    
    Note that SAVE uses the INSPECT module to determine how it was
    called. That means that VARi must all be simple variables and that
    the FILENAME, if given as a direct string, may not contain commas
    or quotation marks. Variable names must start with a letter and
    may only contain letters, numbers, and underscore.
    
    OK examples:
    
      x = 3
      y = 'Hello'
      z = np.eye(3)
    
      save('/tmp/test.pkl', x, y, z)
    
      filename = '/tmp/test,1.pkl'
      save(filename, x, y, z)
    
    Bad examples:
    
      save('/tmp/test,1.pkl', x, y)
    
      save('/tmp/test.pkl', x + 3)

    '''
    
    frame = inspect.currentframe().f_back
    string = inspect.getframeinfo(frame).code_context[0]
    sol = string.find('(') + 1
    eol = string.find(')')
    names = [a.strip() for a in string[sol:eol].split(',')]
    names.pop(0)
    if len(names) != len(args):
        raise ValueError('Bad call to SAVE')
    nre = re.compile('^[a-zA-Z][a-zA-Z0-9_]*$')
    N = len(args)
    for k in range(N):
        if not nre.match(names[k]):
            raise ValueError('Bad variable name: ' + names[k])
        if not cansave(args[k]):
            raise ValueError('Cannot save variable: ' + names[k])

    dct = {}
    for k in range(N):
        dct[names[k]] = args[k]
    savedict(filename, dct)

    
def savedict(filename: str, dct: Dict[str, Any]) -> None:
    '''SAVEDICT - Save data from a DICT
    
    SAVEDICT(filename, dct), where DCT is a `dict`, saves the data contained
    therein as a PICKLE file.

    See SAVE for the type of content that SAVEDICT can save.

    See LOAD, LOADDICT, and MLOAD for how to reload saved data.
    '''
    nre = re.compile('^[a-zA-Z_][a-zA-Z0-9_]*$')
    for k, v in dct.items():
        if not nre.match(k):
            raise ValueError('Bad variable name: ' + k)
        if not cansave(v):
            raise ValueError('Cannot save variable: ' + k)

    with open(filename, 'wb') as fd:  
        pickle.dump(dct, fd, pickle.HIGHEST_PROTOCOL)

        
def savedict_ignorewhitelist(filename: str, dct: Dict[str, Any]) -> None:
    '''SAVEDICT_IGNOREWHITELIST - Save data from a DICT unconditionally

    Mainly intended for internal testing, this does the same thing as
    SAVEDICT except that it does not check whether reloading the data
    would be safe.

    '''
    with open(filename, 'wb') as fd:  
        pickle.dump(dct, fd, pickle.HIGHEST_PROTOCOL)


_allowed = [
    ("builtins", "complex"),
    ("builtins", "set"),
    ("builtins", "frozenset"),
    ("builtins", "range"),
    ("builtins", "slice"),
    
    ("functools", "partial"),
    
    ("numpy", "ndarray"),
    ("numpy", "dtype"),
    ("numpy.core.multiarray", "scalar"),  
    ("numpy.core.numeric", "_frombuffer"),
    ("numpy.core.multiarray", "_reconstruct"),
    
    ("pandas.core.frame", "DataFrame"),
    ("pandas.core.series", "Series"),
    ("pandas.core.indexes.base", "Index"),
    ("pandas.core.indexes.range", "RangeIndex"),
    ("pandas.core.indexes.base", "_new_Index"),
    ("pandas.core.internals.managers", "SingleBlockManager"),
    ("pandas.core.internals.managers", "BlockManager"),
    ("pandas.core.internals.blocks", "new_block"),
    ("pandas._libs.internals", "_unpickle_block"),
]


class SafeLoader(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in _allowed:
            return super().find_class(module, name)
        else:
            raise pickle.UnpicklingError(f"Not allowed “{module}”: “{name}”")

        
class UnsafeLoader(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) not in _allowed:
            print(f"Caution: Loading “{module}.{name}” from pickle.")
        return super().find_class(module, name)

    
def _load(filename, trusted=False):
    with open(filename, 'rb') as fd:
        if trusted:
            return UnsafeLoader(fd).load()
        else:
            return SafeLoader(fd).load()
    

def loaddict(filename: str, trusted: bool = False) -> Dict[str, Any]:

    '''LOADDICT - Reload data saved with SAVE or SAVEDICT
    
    x = LOADDICT(filename) loads the file named FILENAME, which should
    have been created by SAVE or SAVEDICT. The result is a dictionary
    with the original variable names as keys.
    
    Optional parameter TRUSTED may be used to turn off safety checks
    in the underlying pickle loading. With the default TRUSTED=False, 
    we only allow loading of very specific object types, even when nested
    inside Pandas dataframes or numpy arrays. TRUSTED=True enables loading
    any pickle.

    Important: Only use TRUSTED for files that you actually trust!

    '''
    
    dct = _load(filename, trusted)
    if '__names__' in dct:
        del dct['__names__']
    return dct


def _maketuple(dct):
    names = dct.get('__names__', list(dct.keys()))
    class Tuple(collections.namedtuple('Tuple', names)):
        revmap = { name: num for num, name in enumerate(names) }
        def __getitem__(self, k):
            if type(k)==str:
                if k in Tuple.revmap:
                    k = Tuple.revmap[k]
                else:
                    raise KeyError(k)
            else:
                return super().__getitem__(k)
        def __str__(self):
            hdr = "Tuple with fields:\n  "
            return hdr + "\n  ".join(Tuple.revmap.keys())
        def __repr__(self):
            lst = [f"'{key}'" for key in Tuple.revmap.keys()]
            return "<Tuple(" + ", ".join(lst) + ")>"
        def keys(self):
            return Tuple.revmap.keys()
    lst = []
    for n in names:
        lst.append(dct[n])
    return Tuple(*lst)
    

def load(filename: str, trusted: bool = False) -> NamedTuple:
    '''LOAD - Reload data saved with SAVE or SAVEDICT
    
    x = LOAD(filename) loads the file named FILENAME which should have
    been created by SAVE or SAVEDICT.
    
    The result is a named tuple with the original variable names as keys.

    v1, v2, ..., vn = LOAD(filename) immediately unpacks the tuple.

    Optional parameter TRUSTED may be used to turn off safety checks
    in the underlying pickle loading. With the default TRUSTED=False,
    we only allow loading of very specific object types, even when
    nested inside Pandas dataframes or numpy arrays. TRUSTED=True
    enables loading any pickle.

    Important: Only use TRUSTED for files that you actually trust!

    '''
    
    dct = _load(filename, trusted)
    return _maketuple(dct)


def mload(filename: str, trusted: bool = False) -> None:
    '''MLOAD - Reload data saved with SAVE
    
    MLOAD(filename)  loads the variables saved by SAVE(filename, ...) 
    directly into the caller's namespace.
    
    This is a super ugly Matlab-style hack, but occasionally convenient.
    
    LOAD and LOADDICT are cleaner alternatives.
    
    Optional parameter TRUSTED may be used to turn off safety checks
    in the underlying pickle loading. With the default TRUSTED=False, 
    we only allow loading of very specific object types, even when nested
    inside Pandas dataframes or numpy arrays. TRUSTED=True enables loading
    any pickle.
    
    Important: Only use TRUSTED for files that you actually trust!

'''
    dct = _load(filename, trusted)
    names = dct['__names__'] if '__names__' in dct else list(dct.keys())

    frame = inspect.currentframe().f_back
    # inject directly into calling frame
    for k in names:
        frame.f_locals[k] = dct[k]
    print(f'Loaded the following: {", ".join(names)}.')


class Saver:
    """Object-oriented interface to saving with ppersist.

    This allows the syntax

        with ppersist.Saver(filename) as pp:
            pp.save(var1, var2, ...)

    The main advantage over plain

        ppersist.save(filename, var1, var2, ...)

    is that FILENAME may be an arbitrary expression.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.opened = False

    def __enter__(self):
        self.opened = True
        self.dct = {}
        return self

    def save(self, *args: Any) -> None:
        """Save the named variables into the file

        This uses INSPECT just like `ppersist.save` does.

        Use SAVE multiple times to save additional variables.

        The data are only actually saved once the Saver is closed.
        
        """
        if not self.opened:
            raise ValueError("Cannot save without opening first")
        frame = inspect.currentframe().f_back
        string = inspect.getframeinfo(frame).code_context[0]
        sol = string.find('(') + 1
        eol = string.find(')')
        names = [a.strip() for a in string[sol:eol].split(',')]
        if len(names) != len(args):
            raise ValueError('Bad call to SAVE')
        nre = re.compile('^[a-zA-Z][a-zA-Z0-9_]*$')
        N = len(args)
        for k in range(N):
            if not nre.match(names[k]):
                raise ValueError('Bad variable name: ' + names[k])
            if not cansave(args[k]):
                raise ValueError('Cannot save variable: ' + names[k])

        for k in range(N):
            self.dct[names[k]] = args[k]

    def __exit__(self, *args):
        if not self.opened:
            raise ValueError("Not opened")
        savedict(self.filename, self.dct)
        self.opened = False

    
def fetch(url: str) -> NamedTuple:
    """Fetch a ppersist-saved file from the internet

    fetch(url) behaves just like load(file), except that it retrieves
    the data from the internet. For security, there is no “trusted”
    option on fetch().
    """
    import urllib.request
    with urllib.request.urlopen(url) as fd:
        dct = SafeLoader(fd).load()
        return _maketuple(dct)
    
