0.0.6
=====

Packaging
---------
Update packaging to use pyproject.toml over setup.py for installation. The latter was relying on a dependency that contained a function that had been removed from the standard library. This causing an error when trying to install into a python 3.12 environment. There is no change to the installation process. Install a local clone using "pip install ." (#62)


0.0.5
=====

MAST Query
----------

Fixed a bug that was preventing guidestar data from being downloaded. Use the "guidestar" keyword to download guidestar data along with science data. Also added the "guidestar_only_data" keyword, which will remove science data and download only guidestar data. (#55)


Tests
-----

Added some initial regression tests to be sure the behavior with and without the config file is consistent. (#53)


0.0.4
=====

Config File
-----------

Fix a bug that was causing parameters with default values other than None or [] to be set back to the default value after adjusting parameter values based on the contents of the config file. (#51)

Environment
-----------

Add pillow as a dependency in setup.py, so that it is downloaded upon installation of jwst_mast_query. (#49)


0.0.3
=====

Config File
-----------

Fix a bug that was preventing the date_select values in the cfg file from being used. (#39)

Make documentation and default parameter values consistent between the config file and the code. Add missing parameters to the config file (propID, obsnums). (#41)


MAST Query
----------

Fix a bug that was resulting in jwst_mast_query seraching for files across all instruments in cases where the intial
instrument mode search returned an empty string. (#38)

Remove repeated copies of a given filename from the output tables and download list. (#45)


Outputs
-------

Save the product tables into outrootdir, rather than the current working directory. (#40)


0.0.2
=====

Packaging
---------

Add a .gitignore file to the repository (#22)


MAST Query
----------

For some programs with large sets of data products, jwst_mast_query previously timed out. Queries can now be done in batches and
the results combined, preventing the timeout errors. (#30)

MAST recently updated the values in the "instrument_name" column of its database to also contain observation mode names. (e.g.
"NIRCAM/IMAGE" rather than "NIRCAM"). When querying MAST for an instrument name, add a wildcard in order to find new data
that include the mode name, as well as not-yet-reprocessed data that still contain only the instrument name. (#31)

Add "obsmode" as an optional input. Related to #31 above, this new input allows the user to specify which observation modes to
query for. obsmode has been added to the example config file, and can also be specified on the command line. The default is
for obsmode to be empty, in which case jwst_mast_query will search across all modes. (#32)


0.0.1
=====

Initial release.

Includes jwst_query.py and jwst_download.py scripts, and example jwst_query.cfg config file.
