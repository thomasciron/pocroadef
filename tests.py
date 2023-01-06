import unittest
import main

"""
Fichier de tests unitaires
Se compile comme n'importe quel programme Python
"""

class TestTruckMethods(unittest.TestCase):
    def test_object_fit_1(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v = main.Volume(t.length, t.width)
        i = main.Item(-1,-1,2800,2000, t.code, 0)
        self.assertEqual(False, main.doesObjectFit(i,v), "TEST01 : the item fits but it shouldn't !")

    def test_object_fit_2(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v = main.Volume(t.length, t.width)
        i = main.Item(-1,-1,2800,2000, t.code, 0)
        i.flip()
        self.assertEqual(True, main.doesObjectFit(i,v), "TEST02 : the flipped item doesn't fit but it should !")
    
    def test_place_object_1(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v = main.Volume(t.length, t.width)
        i = main.Item(-1,-1,2800,2000, t.code, 0)
        i.flip()
        t.residualVolumes.append(v)
        t.items.append(i)
        t.placeObject(i, v, 0)
        self.assertNotEqual(-1, t.placedItems[0].insertion_point[0], "TEST11 : y assertion point not updated !")

    def test_merge_residual_spaces_1(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v1 = main.ResidualVolume(13500,1440)
        v2 = main.ResidualVolume(13500,2440)
        t.residualVolumes.append(v1)
        t.residualVolumes.append(v2)
        t.mergeResidualSpaces()
        self.assertEqual(1, len(t.residualVolumes), "TEST 21 : length merged failed.")

    def test_merge_residual_spaces_2(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v1 = main.ResidualVolume(13500,1440)
        v2 = main.ResidualVolume(13500,2440)
        t.residualVolumes.append(v1)
        t.residualVolumes.append(v2)
        t.mergeResidualSpaces()
        self.assertEqual(13500, t.residualVolumes[0].length, "TEST 22 : length merged failed.")

    def test_merge_residual_spaces_3(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v1 = main.ResidualVolume(13500,1440)
        v2 = main.ResidualVolume(13500,2440)
        t.residualVolumes.append(v1)
        t.residualVolumes.append(v2)
        t.mergeResidualSpaces()
        self.assertEqual(3880, t.residualVolumes[0].width, "TEST 23 : length merged failed.")

    def test_merge_residual_spaces_4(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v1 = main.ResidualVolume(1440,13500)
        v2 = main.ResidualVolume(2440,13500)
        t.residualVolumes.append(v1)
        t.residualVolumes.append(v2)
        t.mergeResidualSpaces()
        self.assertEqual(1, len(t.residualVolumes), "TEST 24 : width merged failed.")

    def test_merge_residual_spaces_5(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v1 = main.ResidualVolume(1440,13500)
        v2 = main.ResidualVolume(2440,13500)
        t.residualVolumes.append(v1)
        t.residualVolumes.append(v2)
        t.mergeResidualSpaces()
        self.assertEqual(13500, t.residualVolumes[0].width, "TEST 25 : width merged failed.")

    def test_merge_residual_spaces_6(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v1 = main.ResidualVolume(1440,13500)
        v2 = main.ResidualVolume(2440,13500)
        t.residualVolumes.append(v1)
        t.residualVolumes.append(v2)
        t.mergeResidualSpaces()
        self.assertEqual(3880, t.residualVolumes[0].length, "TEST 26 : width merged failed.")

    def test_place_object_1(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v = main.Volume(t.length, t.width)
        i = main.Item(-1,-1,2800,2000, t.code, 0)
        i.flip()
        t.residualVolumes.append(v)
        t.items.append(i)
        t.placeObject(i, v, 0)
        self.assertEqual(2, len(t.residualVolumes), "TEST 31 : not enough residual volumes created.")

    def test_place_object_2(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v = main.Volume(t.length, t.width)
        i = main.Item(-1,-1,2800,2000, t.code, 0)
        i.flip()
        t.residualVolumes.append(v)
        t.items.append(i)
        t.placeObject(i, v, 0)
        self.assertEqual(11500, t.residualVolumes[0].length, "TEST 32 : length first residual volumes not correct.")

    def test_place_object_2(self):
        t = main.Truck()
        t.code = "test1"
        t.width = 2440
        t.length = 13500
        v = main.Volume(t.length, t.width)
        i = main.Item(-1,-1,2800,2000, t.code, 0)
        i.flip()
        t.residualVolumes.append(v)
        t.items.append(i)
        t.placeObject(i, v, 0)
        self.assertEqual(2440, t.residualVolumes[0].width, "TEST 33 : width first residual volumes not correct.")

        



if __name__=="__main__":
    unittest.main()