import numpy as np
import EchelleJSON as ej

class TestOneOrder:
    def setup_class(self):
        npix = 20
        self.wl = np.linspace(5050., 5070.0, npix)
        self.fl = np.random.uniform(0.2, 0.5, npix)
        self.fname = "test_one_order.json"

    def test_write(self):
        echelle_dict = {"order_00": {"wl": self.wl, "fl":self.fl}}
        ej.write(self.fname, echelle_dict)

    def test_read(self):
        edict = ej.read(self.fname)
        order = edict["order_00"]
        assert np.allclose(self.wl, order["wl"]), "Wavelengths do not match"
        assert np.allclose(self.fl, order["fl"]), "Fluxes do not match"


# Test w/ sigma
class TestSigmaBool:
    def setup_class(self):
        self.order_1 =      {"wl":np.linspace(5050., 5070.0, 20),
                            "fl":np.random.uniform(0.2, 0.5, 20),
                            "sigma":np.random.uniform(0.1, 1.0, 20),
                            "mask":np.ones((20,), dtype="bool")
                            }

        self.order_2 =      {"wl":np.linspace(5050., 5070.0, 10),
                            "fl":np.random.uniform(0.2, 0.5, 10),
                            "sigma":np.random.uniform(0.1, 1.0, 10),
                            "mask":np.ones((10,), dtype="bool")
                            }

        self.fname = "test_sigma_bool.json"

    def test_write(self):
        echelle_dict = {"order_1":self.order_1, "order_2":self.order_2}
        ej.write(self.fname, echelle_dict)

    def test_read(self):
        edict = ej.read(self.fname)

        field_keys = ["wl", "fl", "sigma", "mask"]

        for key in field_keys:
            assert np.allclose(edict["order_1"][key], self.order_1[key]), "order_1 {} does not match".format(key)
            assert np.allclose(edict["order_2"][key], self.order_2[key]), "order_2 {} does not match".format(key)
        
