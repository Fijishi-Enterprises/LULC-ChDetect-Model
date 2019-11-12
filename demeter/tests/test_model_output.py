import unittest
import pkg_resources
import os

import pandas as pd

from demeter.model import Demeter


class TestEqualOutputs(unittest.TestCase):
    """Test that the default outputs do not change."""

    DEFAULT_CONFIG_FILE = pkg_resources.resource_filename('demeter', 'tests/data/config.ini')
    LANDCOVER_2005_CSV = 'landcover_2005_timestep.csv'
    COMP_OUTPUT_2005 = pkg_resources.resource_filename('demeter', 'tests/data/comp_outputs/{}'.format(LANDCOVER_2005_CSV))
    OUTPUT_DIR = pkg_resources.resource_filename('demeter', 'tests/data/outputs/')
    LANDCLASSES = ['water', 'forest', 'shrub', 'grass', 'crops', 'urban', 'snow', 'sparse']

    @classmethod
    def get_output_dir(cls):
        """Get the name of the Demeter generated output directory."""

        root_dir = [i for i in os.listdir(cls.OUTPUT_DIR) if i.split('_')[0] == 'tests'][0]

        return os.path.join(cls.OUTPUT_DIR, root_dir, 'spatial_landcover_tabular')

    def test_outputs(self):
        """Test that Demeter produces correct outputs for the default configuration."""

        # load comp data and set unique key to index
        comp_output_2005 = pd.read_csv(TestEqualOutputs.COMP_OUTPUT_2005)
        comp_output_2005['key'] = comp_output_2005['latitude'].astype(str) + '_' + comp_output_2005['longitude'].astype(str)
        comp_output_2005.set_index('key', inplace=True)

        # set up and run Demeter
        res = Demeter(config=TestEqualOutputs.DEFAULT_CONFIG_FILE)
        res.execute()

        output_dir = self.get_output_dir()

        # extract only US from result to test
        res_output_2005 = pd.read_csv(os.path.join(output_dir, TestEqualOutputs.LANDCOVER_2005_CSV))
        res_output_2005 = res_output_2005.loc[res_output_2005['region_id'] == 1].copy()
        res_output_2005['key'] = res_output_2005['latitude'].astype(str) + '_' + res_output_2005['longitude'].astype(str)
        res_output_2005.set_index('key', inplace=True)

        # test for equality
        pd.testing.assert_frame_equal(comp_output_2005, res_output_2005)


if __name__ == '__main__':
    unittest.main()
