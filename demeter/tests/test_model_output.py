"""test_model_outputs.py

Tests to ensure high-level functionality and outputs remain consistent.

@author Chris R. Vernon (chris.vernon@pnnl.gov)
@license BSD 2-Clause

"""

import os
import pkg_resources
import shutil
import unittest

import pandas as pd

from demeter import Demeter


class TestOutputs(unittest.TestCase):
    """Test configuration integrity."""

    RUN_DIR = pkg_resources.resource_filename('demeter', 'tests/data')
    CONFIG_FILE = pkg_resources.resource_filename('demeter', 'tests/data/config.ini')
    COMP_DF = pd.read_csv(pkg_resources.resource_filename('demeter', 'tests/data/comp_data/landcover_2010_timestep.csv'))

    def test_proj_outputs_using_args(self):
        """Test for projection outputs by passing arguments"""

        # run demeter without using configuration file
        run = Demeter(run_dir=TestOutputs.RUN_DIR, target_years_output="2010")
        run.execute()

        # read in run data from rasters to arrays
        output_dir = os.path.split(run.c.output_dir)[-1]
        run_2010 = os.path.join(TestOutputs.RUN_DIR, 'outputs', output_dir, 'spatial_landcover_tabular', 'landcover_2010_timestep.csv')
        run_df = pd.read_csv(run_2010)

        # test equality
        pd.testing.assert_frame_equal(TestOutputs.COMP_DF, run_df)

        # remove run directory
        shutil.rmtree(run.c.output_dir)

    # def test_proj_outputs_using_config(self):
    #     """Test for projection outputs using a config file"""
    #
    #     # run demeter without using configuration file
    #     run = Demeter(config_file=TestOutputs.CONFIG_FILE, run_dir=TestOutputs.RUN_DIR)
    #     run.execute()
    #
    #     # read in run data from rasters to arrays
    #     output_dir = os.path.split(run.c.output_dir)[-1]
    #     run_2010 = os.path.join(TestOutputs.RUN_DIR, 'outputs', output_dir, 'spatial_landcover_tabular', 'landcover_2010_timestep.csv')
    #     run_df = pd.read_csv(run_2010)
    #
    #     # test equality
    #     pd.testing.assert_frame_equal(TestOutputs.COMP_DF, run_df)
    #
    #     # remove run directory
    #     shutil.rmtree(run.c.output_dir)


if __name__ == '__main__':
    unittest.main()
