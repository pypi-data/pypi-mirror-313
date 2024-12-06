import pytest
import numpy as np
import pandas as pd
import ppersist
import pickle
from tempfile import NamedTemporaryFile

class TempName:
    def __enter__(self):
        self.ntf = NamedTemporaryFile(delete_on_close=False, suffix=".pkl")
        fd = self.ntf.__enter__()
        name = fd.name
        fd.close()
        return name
    
    def __exit__(self, *args):
        self.ntf.__exit__(*args)
        del self.ntf

def test_saveload():
    abool = True
    anint = 12345
    afloat = 3.1415
    alist = [abool, anint, afloat]
    anarray = np.array([[1.1, 1.2, 1.3],
                           [3.1, 3.2, 3.3]])
    adict = {"afloat": afloat,
             "alist": alist}
    with TempName() as name:
        with ppersist.Saver(name) as pp:
            pp.save(abool, anint, afloat)
            pp.save(anarray, adict)
        x = ppersist.load(name)
    assert x.abool == abool
    assert x.anint == anint
    assert x.afloat == afloat
    assert np.all(x.anarray == anarray)
    assert x.adict == adict

    
def test_fetch():
    abool = True
    anint = 12345
    afloat = 3.1415
    alist = [abool, anint, afloat]
    anarray = np.array([[1.1, 1.2, 1.3],
                           [3.1, 3.2, 3.3]])
    adict = {"afloat": afloat,
             "alist": alist}
    x = ppersist.fetch("https://leech.caltech.edu/ppersist/x.pkl")
    assert x.abool == abool
    assert x.anint == anint
    assert x.afloat == afloat
    assert np.all(x.anarray == anarray)
    assert x.adict == adict


def test_pandas():
    aframe = pd.DataFrame({"first": [1, 2, 3], "second": [4, 5, 6]})
    anint = 12345
    afloat = 3.1415
    anarray = np.array([1, 2, 3])
    abool = False
    aseries = pd.Series([anint, afloat, abool])
    with TempName() as name:
        ppersist.save(name, aframe, aseries)
        x = ppersist.load(name)
    assert np.all(x.aframe == aframe)
    assert np.all(x.aseries == aseries)

    
class Evil:
    def __init__(self, x=0):
        if x != 1:
            print("Kaboom!")

            
def test_evilsave():
    evil = Evil(1)
    with TempName() as name:
        with pytest.raises(ValueError):
            ppersist.save(name, evil)


def test_evilload():
    x = {"evil": Evil(1)}
    with TempName() as name:
        ppersist.savedict_ignorewhitelist(name, x)
        with pytest.raises(pickle.UnpicklingError):
            x = ppersist.load(name)


def test_evilpandassave():
    evil = Evil(1)
    aseries = pd.Series([evil])
    with pytest.raises(ValueError):
        ppersist.save("/tmp/x.pkl", aseries)


def test_evilpandasload():
    evil = Evil(1)
    aseries = pd.Series([evil])
    x = {"aseries": aseries}
    with TempName() as name:
        ppersist.savedict_ignorewhitelist(name, x)
        with pytest.raises(pickle.UnpicklingError):
            x = ppersist.load(name)
    
