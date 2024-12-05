import unittest
from gdal2numpy import *


fileshp = "s3://saferplaces.co/packages/gdal2numpy/open/OSM_BUILDINGS_102258.shp"

class TestFeatures(unittest.TestCase):
    """
    Tests for the TestFeatures function
    """

    def test_get_fieldnames(self):
        """
        test_get_fieldnames: test that the function returns the correct field names
        """
        self.assertEqual(GetFieldNames(fileshp), ['value_m2', 'fdamage'])


    def test_get_numeric_fieldnames(self):
        """
        test_get_fieldnames: test that the function returns the correct field names
        """
        self.assertEqual(GetNumericFieldNames(fileshp),  ['value_m2'])


    def test_get_range(self):
        """
        test_get_range: test that the function returns the correct range
        """
        self.assertEqual( GetRange(fileshp, "value_m2"), (1000.0, 1000.0))


    def test_get_features(self):
        """
        test_get_features: test that the function returns the correct features
        """
        features = GetFeatures(fileshp)
        n = GetFeatureCount(fileshp)
        self.assertEqual(len(features), n)


    def test_same_srs(self):
        """
        test_same_srs: test that the function returns the correct features
        """
        self.assertTrue(SameSpatialRef(fileshp, "EPSG:4326"))


    def test_transform(self):
        """
        test_transform: test that the function returns the correct features
        """
        fileout = tempdir() + "/OSM_BUILDINGS_3857.shp"
        Transform(fileshp, "EPSG:3857",fileout=fileout)
        self.assertTrue(SameSpatialRef(fileout, "EPSG:3857"))
        self.assertEqual(GetFeatureCount(fileout), GetFeatureCount(fileshp))
        os.remove(fileout)


if __name__ == '__main__':
    unittest.main()



