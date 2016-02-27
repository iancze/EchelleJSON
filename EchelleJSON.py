import numpy as np
import json
from astropy.utils.misc import JsonCustomEncoder

order_prefix = "order_"

def read(fname):
    '''
    A simple routine to read a JSON format and return dictionaries of numpy arrays.
    '''

    f = open(fname, 'r')
    echelle_dict = json.load(f)
    f.close()

    # go through each of the orders and convert these from lists to numpy arrays
    order_keys = [key for key in echelle_dict.keys() if "order_" in key]
    for key in order_keys:
        order = echelle_dict[key]
        echelle_dict[key]["wl"] = np.array(order["wl"])
        echelle_dict[key]["fl"] = np.array(order["fl"])

        # If it has sigma, convert it too
        if "sigma" in order.keys():
            echelle_dict[key]["sigma"] = np.array(order["sigma"])

    return echelle_dict


def write(fname, echelle_dict):
    '''
    A simple routine to turn dictionaries of numpy arrays into JSON format.
    '''

    # check that echelle fields are labeled with `order_{name}` (there must be at least one)
    assert type(echelle_dict) is dict, '''You must pass in a dictionary... \n
    echelle_dict = {"order_00":{"wl": [5003.3, ...], "fl": [0.01, ...]}}'''

    # check that each order has at least wl and fl, and that they are the same length
    order_keys = [key for key in echelle_dict.keys() if "order_" in key]
    for key in order_keys:
        order = echelle_dict[key]
        assert "wl" in order.keys(), "Must contain wl as a key."
        assert "fl" in order.keys(), "Must contain fl as a key."

        # Assert wl is strictly increasing and that there are no duplicate wl pixels
        wl = order["wl"]
        assert np.all(np.diff(wl) > 0), "wl for {} must be strictly increasing and contain no duplicate pixels.".format(key)

        assert len(wl) == len(order["fl"]), "wl and fl must be the same length 1-D arrays."

    f = open(fname, 'w')
    # json.dump(echelle_dict, f, cls=encoder)
    json.dump(echelle_dict, f, cls=JsonCustomEncoder, sort_keys=True, indent=2)
    f.close()

# Assume that we are using the module as a command line script.
def main():
    pass

if __name__=="__main__":
    main()
