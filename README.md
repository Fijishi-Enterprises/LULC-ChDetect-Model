[![build](https://github.com/JGCRI/demeter/actions/workflows/build.yml/badge.svg)](https://github.com/JGCRI/demeter/actions/workflows/build.yml)
[![DOI](https://zenodo.org/badge/101879773.svg)](https://zenodo.org/badge/latestdoi/101879773)

# Demeter

## A land-use and land-cover disaggregation and change detection model
Demeter is an open source Python package that was built to disaggregate projections of future land allocations generated by an integrated human-Earth systems model.  Projected land allocation from IAMs is traditionally transferred to Earth System Models (ESMs) in a variety of gridded formats and spatial resolutions as inputs for simulating biophysical and biogeochemical fluxes. Existing tools for performing this translation generally require a number of manual steps which introduces error and is inefficient.  Demeter makes this process seamless and repeatable by providing gridded land use and land cover change (LULCC) products derived directly from an IAM—in this case, the Global Change Analysis Model (GCAM)—in a variety of formats and resolutions commonly used by ESMs.  Demeter is publicly available via GitHub and has an extensible output module allowing for future ESM needs to be easily accommodated.    

# Getting Started with Demeter
Set up Demeter using the following steps:
1.  Install Demeter from GitHub using:
    ```bash
    python -m pip install git+https://github.com/JGCRI/demeter.git
    ```
2.  Download the example data using the following in a Python prompt:
    ```python
    import demeter
    
    # the directory that you want to download and extract the example data to
    data_dir = "<my data download location>"
    
    # download and unzip the package data to your local machine
    demeter.get_package_data(data_dir)
    ```
3.  Setup your configuration file (.ini).  Examples are located in the "example" directory that you just downloaded.  Be sure to change the following variables to represent the local path.
4.  To run Demeter:

    ```python
    import demeter
    
    # the path and file name that my example configuration (.ini) file was downloaded to
    config_file = '<path to my example config file>/demeter_config.ini'

    # run all time steps
    demeter.run_model(config_file=config_file,
                      write_outputs=True)
    ```


## Setup
Demeter requires the setup of several input files to begin a run.  Examples of all input files can be found in the ‘examples’ directory and the expected file structure is outlined in the following:

-	Example directory
    -   Inputs directory
        -	Allocation directory
            -	Constraint weighting file
                -	GCAM landclass allocation file
                -	Kernel density weighting file
                -	Spatial landclass allocation file
                -	Transition priority file
                -	Treatment order file
        -	Observed spatial data directory
            -	Observed spatial data file
        -	Constraint data directory
            -	Constraint files
        -	Projected GCAM land allocation directory
            -	GCAM land allocation file

The following describes the requirements and format of each input.

### Observed spatial data:

This file represents the area in square degrees of each land class existing within a grid cell.  The grid cell size is defined by the user.  This file must be presented as a comma-separated values (CSV) file having a header in the first row and must contain the field names and fields described in Table 1.


|   Field	|   Description   |         
| --------- | --------------- |
| fid | Unique integer ID for each grid cell latitude, longitude |
| landclass | Each land class field name (e.g., shrub, grass, etc.).  Field names must not include commas. |
| region_id	| The integer ID of the GCAM region that the grid cell is contained in.  Exact field name spelling required. |
| metric_id	| The integer ID of the GCAM basin that the grid cell is contained in.  Exact field name spelling required. |
| latitude | The geographic latitude value of the grid cell centroid as a signed float.  Exact field name spelling required. |
| longitude	| The geographic longitude value of the grid cell centroid as a signed float.  Exact field name spelling required. |

**Table 1.**  Observed spatial data required fields and their descriptions.

### Projected land allocation data:

This file is the formatted GCAM run output for land allocation projections.  Since the format of this file can vary based on GCAM user preference, the file must be formatted to meet Demeter input requirements as described in Table 2.  The file must be a CSV file having the header in the first row.

| Field	| Description |
| --- | --- |
| region	| The text name of the GCAM region. Exact field name spelling required. |
| landclass | Each land class field name (e.g., shrub, grass, etc.).  Field names must not include commas. |
| year | Each year of the GCAM run as an integer (e.g., 2005, 2010, etc.) |
| metric_id |	The integer ID of the GCAM basin.  Exact field name spelling required. |

**Table 2.** Projected land allocation required fields from GCAM.

### Allocation files:

#### *Constraint weighting:*

A weight for each constraint, with a value ranging from -1.0 to 1.0, can be applied to each land class.  If no constraints are desired, a user should simply provide a header-only file.  For example, for a given land class, the weight for the soil quality constraint with a value of -1 indicates that one land class is fully constrained inversely (e.g., grasslands are opportunistic and grow readily in areas with a low soil quality); a weight of 0 indicates that soil quality exerts no constraint to the land class (e.g., forest, etc.); a weight of 1 for soil quality indicates that high soil quality will highly influence where the type will be spatially allocated (e.g. cropland).  These constraints are developed in separate files as described in the following Constraints section.  See the constraint weighting file in the example inputs for reference.

#### *Kernel density weighting:*

Weight the degree to which land classes subjected to a kernel density filter will be utilized during expansion to each class.  Value from 0.0 to 1.0. See the kernel density weighting file in the example inputs for reference.

#### *Transition Priority:*

This ordering defines the preferential order of final land allocation (e.g., crops expanding into grasslands rather than forests).  See the priority allocation file in the example inputs for reference.  See the priority allocation file in the example inputs for reference.  

#### *Treatment order:*

Defines the order in which final land classes are downscaled.  This will influence the results (e.g., if crops are downscaled first and overtake grassland, grassland will not be available for shrubs to overtake when processing shrub land).  See the treatment order file in the example inputs for reference.

#### *Observational spatial data class allocation:*

This file defines how the land-use and land-cover classes in the OSD will be binned into final land classes for output, which can be defined by the user and serve to place projected land allocation data from GCAM on a common scale with the on-the-ground representation of land-use and land-cover represented in the OSD.  See the Observed spatial data class allocation file in the example inputs for reference.

#### *Projected land class allocation:*

This file defines how the land-use and land-cover classes in the GCAM projected land allocation data will be binned into final classes.  See the projected land class allocation file in the example inputs for reference.   

#### *Constraints (not required):*

As discussed earlier, constraints such as soil quality may be desirable to the user and can be prepared by assigning a weighted value from 0.0 to 1.0 for each grid cell in the OSD. Spatial maps of constraints should be provided by the user for application during the downscaling process. Users should note that constraining a grid cell to 0.0 may impede the ability to be able to achieve a projected land allocation from GCAM since land area is being excluded that GCAM expects.  Each constraint file must have two fields:  fid and weight.  The fid field should correspond to the fid field in the OSD input and the weight field should be the weight of the constraint per the cell corresponding to the OSD input.  Each file should be a CSV with no header.

### Configuration file:

Demeter’s configuration file allows the user to customize each run and define where file inputs are and outputs will be.  The configuration options and hierarchical level are described in Table 3.

| Level | Parameter | Description |
| --- | --- | --- |
|  STRUCTURE |	root_dir | The full path of the root directory where the inputs and outputs directory are stored |
|  STRUCTURE |	in_dir	| The name of the input directory |
|  STRUCTURE |	out_dir	 | The name of the output directory |
| INPUTS | allocation_dir |	The name of the directory that holds the allocation files
| INPUTS | observed_dir	| The name of the directory that holds the observed spatial data file
| INPUTS | constraints_dir | The name of the directory that holds the constraints files
| INPUTS | projected_dir |	The name of the directory that holds the GCAM projected land allocation file
| INPUTS - ALLOCATION |	spatial_allocation	|The file name with extension of the observed spatial data class allocation
| INPUTS - ALLOCATION |	gcam_allocation	|The file name with extension of the projected land class allocation
| INPUTS - ALLOCATION |	kernel_allocation	|The file name with extension of the kernel density weighting
| INPUTS - ALLOCATION |	priority_allocation|	The file name with extension of the priority allocation
| INPUTS - ALLOCATION |	treatment_order	|The file name with extension of the treatment order
| INPUTS - ALLOCATION |	constraints|	The file name with extension of the constraint weighting
| INPUTS - OBSERVED |	observed_lu_data	|The file name with extension of the observational spatial data
| INPUTS - PROJECTED |	projected_lu_data|	The file name with extension of the projected land allocation data from GCAM
| OUTPUTS | diag_dir|	The name of the directory that diagnostics outputs will be kept
| OUTPUTS  |	log_dir|	The name of the directory that the log file outputs will be kept
| OUTPUTS  |	transition_tabular|	The name of the directory that tabular land transition outputs will be kept
| OUTPUTS  |	luc_ts_luc	|The name of the directory that the land use change per time step map outputs will be kept
| OUTPUTS  |	lc_per_step_csv	|The name of the directory that the tabular land change per time step outputs will be kept
| OUTPUTS  |	lc_per_step_nc	|The name of the directory that the NetCDF land change per time step outputs will be kept
| OUTPUTS - DIAGNOSTICS |	harm_coeff|	The file name with extension of the NumPy array that will hold the harmonization coefficient data
| OUTPUTS - DIAGNOSTICS |	intense_pass1_diag|	The file name with extension of the CSV that will hold the land allocation per time step per functional type for the first pass of intensification
| OUTPUTS - DIAGNOSTICS |	intense_pass2_diag	|The file name with extension of the CSV that will hold the land allocation per time step per functional type for the second pass of intensification
| OUTPUTS - DIAGNOSTICS |	expansion_diag	|The file name with extension of the CSV that will hold the land allocation per time step per functional type for the expansion pass
| PARAMS |	model | The model name providing the projected land allocation data (e.g., GCAM)
| PARAMS |	metric	 | Subregion type (either AEZ or BASIN)
| PARAMS |	scenario	 | Scenario name
| PARAMS |	run_desc	 | The description of the current run
| PARAMS |	agg_level	 | 1 if only by metric, 2 if by region and metric
| PARAMS |	observed_id_field	 | Observed spatial data unique field name (e.g. target_fid)
| PARAMS |	start_year | 	First time step to process (e.g., 2005)
| PARAMS |	end_year | 	Last time step to process (e.g., 2100)
| PARAMS |	use_constraints	 | 1 to use constraints, 0 to ignore constraints
| PARAMS |	spatial_resolution | 	Spatial resolution of the observed spatial data in decimal degrees (e.g. 0.25)
| PARAMS |	errortol	 | Allowable error tolerance in square kilometres for non-accomplished change
| PARAMS |	timestep	 | Time step interval (e.g., 5 years) for the output data.  This time step is the increment that Demeter will process when starting with the base year.
| PARAMS |	proj_factor	 | Factor to multiply the projected land allocation by
| PARAMS |	diagnostic	 | 0 to not output diagnostics, 1 to output
| PARAMS |	intensification_ratio | 	Ideal fraction of land change that will occur during intensification.  The remainder will be through expansion.  Value from 0.0 to 1.0.
| PARAMS |	stochastic_expansion	 | 0 to not conduct stochastic expansion of grid cells, 1 to conduct
| PARAMS |	selection_threshold | 	Threshold above which grid cells are selected to receive expansion for a target functional type from the kernel density filter.  Value from 0.0 to 1.0; where 0 lets all land cells receive expansion and 1 only lets only the grid cells with the maximum likelihood expand.
| PARAMS |	kernel_distance | 	Radius in grid cells used to build the kernel density convolution filter used during expansion
| PARAMS |	target_years_output | 	Years to save data for; default is ‘all’; otherwise a semicolon delimited string (e.g., 2005; 2020)
| PARAMS |	save_tabular | 	Save tabular spatial land cover as a CSV; define tabular units in tabular_units param
| PARAMS |	tabular_units | 	Units to output the spatial land cover data in; either ‘sqkm’ or 'fraction'
| PARAMS |	save_transitions | 	0 to not write CSV files for each land transitions per land type, 1 to write
| PARAMS |	save_netcdf_yr | 	0 to not write a NetCDF file for each year of the fraction of land cover of each land class by grid cell; 1 to write

**Table 3.**  Configuration file hierarchy, parameters, and descriptions.
