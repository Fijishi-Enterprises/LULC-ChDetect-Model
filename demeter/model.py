"""
Class to run Demeter model for all defined steps.

Copyright (c) 2017, Battelle Memorial Institute

Open source under license BSD 2-Clause - see LICENSE and DISCLAIMER

@author:  Chris R. Vernon (chris.vernon@pnnl.gov)
"""

import argparse
import os
import sys
import time
import traceback

from demeter.config_reader import ReadConfig
from demeter.logger import Logger
from demeter.process import ProcessStep
from demeter.staging import Stage


class ValidationException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Demeter(Logger):
    """Run the Demeter model.

    :param root_dir:                        Full path with filename and extension to the directory containing the
                                            directory structure.
    """

    def __init__(self, **kwargs):

        self.params = kwargs


        # self.config_file = kwargs.get('config_file', None)
        #
        # if self.config_file is None:
        #
        #     self.run_dir = kwargs.get('run_dir', None)
        #     self.input_dir = os.path.join(self.run_dir, input_dir)
        #     self.output_dir = os.path.join(self.run_dir, output_dir)
        #
        #     # allocation
        #     self.allocation_dir = os.path.join(self.input_dir, allocation_dir)
        #     self.spatial_allocation_file = os.path.join(self.allocation_dir, spatial_allocation_file)
        #     self.gcam_allocation_file = os.path.join(self.allocation_dir, gcam_allocation_file)
        #     self.kernel_allocation_file = os.path.join(self.allocation_dir, kernel_allocation_file)
        #     self.transition_order_file = os.path.join(self.allocation_dir, transition_order_file)
        #     self.treatment_order_file = os.path.join(self.allocation_dir, treatment_order_file)
        #     self.constraints_file = os.path.join(self.allocation_dir, constraints_file)
        #
        #     # observed
        #     self.observed_dir = os.path.join(self.input_dir, observed_dir)
        #     self.observed_lu_file = os.path.join(self.observed_dir, observed_lu_file)
        #
        #     # projected
        #     self.projected_dir = os.path.join(self.input_dir, projected_dir)
        #     self.projected_lu_file = os.path.join(self.projected_dir, projected_lu_file)
        #
        #     # reference
        #     self.reference_dir = os.path.join(self.input_dir, reference_dir)
        #     self.gcam_region_names_file = os.path.join(self.reference_dir, gcam_region_names_file)
        #     self.gcam_region_coords_file = os.path.join(self.reference_dir, gcam_region_coords_file)
        #     self.gcam_country_coords_file = os.path.join(self.reference_dir, gcam_country_coords_file)
        #
        #     # constraints directory
        #     self.constraints_dir = os.path.join(self.input_dir, constraints_dir)
        #
        #     # output directories
        #     self.diagnostics_output_dir = os.path.join(self.output_dir, diagnostics_output_dir)
        #     self.log_output_dir = os.path.join(self.output_dir, log_output_dir)
        #     self.kernel_maps_output_dir = os.path.join(self.output_dir, kernel_maps_output_dir)
        #     self.transitions_tabular_output_dir = os.path.join(self.output_dir, transitions_tabular_output_dir)
        #     self.transitions_maps_output_dir = os.path.join(self.output_dir, transitions_maps_output_dir)
        #     self.intensification_pass1_output_dir = os.path.join(self.output_dir, intensification_pass1_output_dir)
        #     self.intensification_pass2_output_dir = os.path.join(self.output_dir, intensification_pass2_output_dir)
        #     self.extensification_output_dir = os.path.join(self.output_dir, extensification_output_dir)
        #     self.luc_timestep = os.path.join(self.output_dir, luc_timestep)  # TODO:  depreciate maps functions
        #     self.lu_csv_output_dir = os.path.join(self.output_dir, lu_csv_output_dir)
        #     self.lu_netcdf_output_dir = os.path.join(self.output_dir, lu_netcdf_output_dir)
        #     self.lu_shapefile_output_dir = os.path.join(self.output_dir, lu_shapefile_output_dir)
        #
        #     # diagnostics outputs
        #     self.harmonization_coefficent_array = os.path.join(self.diagnostics_output_dir, harmonization_coefficent_array)
        #     self.intensification_pass1_file = os.path.join(self.diagnostics_output_dir, intensification_pass1_file)
        #     self.intensification_pass2_file = os.path.join(self.diagnostics_output_dir, intensification_pass2_file)
        #     self.extensification_file = os.path.join(self.diagnostics_output_dir, extensification_file)
        #
        #     # run parameters
        #     self.model = model
        #     self.metric = metric
        #     self.scenario = scenario
        #     self.run_desc = run_desc
        #     self.agg_level = agg_level
        #     self.observed_id_field = observed_id_field
        #     self.start_year = start_year
        #     self.end_year = end_year
        #     self.use_constraints = use_constraints
        #     self.spatial_resolution = spatial_resolution
        #     self.errortol = errortol
        #     self.timestep = timestep
        #     self.proj_factor = proj_factor
        #     self.diagnostic = diagnostic
        #     self.intensification_ratio = intensification_ratio
        #     self.stochastic_expansion = stochastic_expansion
        #     self.selection_threshold = selection_threshold
        #     self.kernel_distance = kernel_distance
        #     self.map_kernels = map_kernels
        #     self.map_luc_pft = map_luc_pft
        #     self.map_luc_steps = map_luc_steps
        #     self.map_transitions = map_transitions
        #     self.target_years_output = target_years_output
        #     self.save_tabular = save_tabular
        #     self.tabular_units = tabular_units
        #     self.save_transitions = save_transitions
        #     self.save_shapefile = save_shapefile
        #     self.save_netcdf_yr = save_netcdf_yr
        #     self.save_netcdf_lc = save_netcdf_lc
        #     self.save_ascii_max = save_ascii_max
        #
        # else:
        #     self.config_file = config_file
        #     self.run_dir = run_dir

        self.c = None
        self.s = None
        self.process_step = None
        self.rg = None
        self.f = None

    @staticmethod
    def log_config(c, log):
        """
        Log validated configuration options.
        """
        for i in dir(c):

            # create configuration object from string
            x = eval('c.{0}'.format(i))

            # ignore magic objects
            if type(x) == str and i[:2] != '__':

                # log result
                log.debug('CONFIG: [PARAMETER] {0} -- [VALUE] {1}'.format(i, x))

    def make_logfile(self):
        """Make log file.

        :return                               log file object

        """
        # create logfile path and name
        self.f = os.path.join(self.c.run_dir, '{0}/logfile_{1}_{2}.log'.format(self.c.log_output_dir, self.c.scenario, self.c.dt))

        # parameterize logger
        self.log = Logger(self.f, self.c.scenario).make_log()

    def setup(self):
        """Setup model."""
        # instantiate config
        self.c = ReadConfig(self.params)

        # instantiate log file
        self.make_logfile()

        # create log header
        self.log.info('START')

        # log validated configuration
        self.log_config(self.c, self.log)

        # prepare data for processing
        self.s = Stage(self.c, self.log)

    def execute(self):
        """
        Execute main downscaling routine.
        """
        # set start time
        t0 = time.time()

        try:

            # set up pre time step
            self.setup()

            # run for each time step
            for idx, step in enumerate(self.s.user_years):

                ProcessStep(self.c, self.log, self.s, idx, step)

        except:

            # catch all exceptions and their traceback
            e = sys.exc_info()[0]
            t = traceback.format_exc()

            # log exception and traceback as error
            try:
                self.log.error(e)
                self.log.error(t)

                # close all open log handlers
                Logger(self.f, self.c.scenario).close_logger(self.log)

            except AttributeError:
                print(e)
                print(t)

        finally:

            try:
                self.log.info('PERFORMANCE:  Model completed in {0} minutes'.format((time.time() - t0) / 60))
                self.log.info('END')
                self.log = None

            except AttributeError:
                pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run Demeter.')

    parser.add_argument('--config', dest='config', action='store', type=str, help='Full path with file name and extension to the input configuration INI file')
    parser.add_argument('--run_dir', dest='run_dir', action='store', type=str, help='Full path to the directory containing the input and output directories')

    args = parser.parse_args()

    if os.path.isfile is False:
        print('ERROR:  Config file not found.')
        print('You entered:  {0}'.format(args.config))
        print('Please enter a full path file name with extension to config file and retry.')
        raise ValidationException

    # instantiate and run demeter
    dm = Demeter(config_file=args.config, run_dir=args.run_dir)
    dm.execute()
