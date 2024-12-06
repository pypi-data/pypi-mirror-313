v0.18.0 (2024-12-04)
====================

Features
--------

- Improve preserving relative scaling of slitbeams in final gain image. See Science Changelog for more information. (`#50 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/50>`__)


Misc
----

- Update "solar gain as science" local trial workflow to support polarimetric input/output data. (`#49 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/49>`__)
- Pin `sphinx-autoapi` to v3.3.3 to avoid `this issue <https://github.com/readthedocs/sphinx-autoapi/issues/505>`_ until it is fixed. (`#51 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/51>`__)


Documentation
-------------

- Add individual online documentation pages for important pipeline steps.
  These pages are found `here <https://docs.dkist.nso.edu/projects/dl-nirsp/en/latest/>`_. (`#46 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/46>`__)
- Make all private methods public so they (and their docstrings) are shown on online documentation. (`#47 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/47>`__)


v0.17.4 (2024-11-26)
====================

Misc
----

- Bumping dkist-fits-specification to v4.10.0 and dkist-processing-common to v10.5.3 (`#48 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/48>`__)
- Write the CNAMEn keywords to the instrument headers. (`#48 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/48>`__)


v0.17.3 (2024-11-21)
====================

Bugfixes
--------

- Update dkist-inventory and dkist-processing-common to fix a bug in producing dataset inventory from the SPECLN* keys


v0.17.2 (2024-11-20)
====================

Bugfixes
--------

- Update dkist-processing-common to constrain asdf < 4.0.0


v0.17.1 (2024-11-20)
====================

Misc
----

- Update dkist-processing-common to manage breaking API changes in asdf and moviepy.


v0.17.0 (2024-11-14)
====================

Misc
----

- Replace `TransferDlnirspTrialData` with `TransferTrialData` from dkist-processing-common. (`#44 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/44>`__)


v0.16.0 (2024-10-30)
====================

Features
--------

- Add ability to determine order of X/Y mosaic step loops.
  Understanding the loop order is crucial for correctly slicing the mosaic when observations were aborted. (`#45 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/45>`__)


v0.15.1 (2024-10-22)
====================

Bugfixes
--------

- Don't require the presence of DARK task frames with an exposure time matching that of the POLCAL task frames.
  POLCAL frames are corrected with their own darks that are taken as part of the polcal sequence and are given the POLCAL task type. (`#43 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/43>`__)


v0.15.0 (2024-10-15)
====================

Features
--------

- Compute demodulation matrices separately for each spatial pixel and then fit the demodulation matrices as a function
  of spatial pixel within each group. (`#39 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/39>`__)
- Allow groups that border the edges of the array to have their area changed by IFU drifts. (`#40 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/40>`__)


v0.14.3 (2024-10-14)
====================

Misc
----

- Switch from setup.cfg to pyproject.toml for build configuration (`#41 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/41>`__)
- Make and publish wheels at code push in build pipeline (`#41 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/41>`__)


v0.14.2 (2024-10-07)
====================

Misc
----

- Bump dkist-fits-specifications to v4.7.0. This adjusted the TTBLTRCK allowed values, adjusted CRSP_051 and CRSP_052 to accommodate blocking filters,adjusted CRSP_073 to include a new grating, and added a new allowed value to CAM__044. (`#47 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/47>`__)


v0.14.1 (2024-10-01)
====================

Bugfixes
--------

- Make `IfuDriftCalibration` a workflow dependency of the `InstrumentPolarizationCalibration` task. (`#38 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/38>`__)


v0.14.0 (2024-10-01)
====================

Features
--------

- Account for the slow drift over time of the IFU in the FOV by measuring the offset between stored IFU metrology arrays,
  which are used during calibration, and the dataset currently being processed. (`#36 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/36>`__)


v0.13.0 (2024-10-01)
====================

Features
--------

- Add support for "dither" mode where each full mosaic is repeated a second time with a slight offset. (`#31 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/31>`__)


v0.12.1 (2024-09-27)
====================

Misc
----

- Bump `dkist-processing-common` to v10.2.1. This fixes a documentation build bug in Airflow.


v0.12.0 (2024-09-27)
====================

Misc
----

- Bump `dkist-processing-common` to v10.2.0. This includes upgrading to the latest version of Airflow (2.10.2).


v0.11.2 (2024-09-26)
====================

Misc
----

- Bump `dkist-processing-common` to v10.1.0. This enables the usage of the `NearFloatBud` and `TaskNearFloatBud` in parsing.


v0.11.1 (2024-09-24)
====================

Misc
----

- Bump `dkist-processing-common` to v10.0.1. This fixes a bug in the reported FRAMEVOL key in L1 headers. (`#37 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/37>`__)


v0.11.0 (2024-09-23)
====================

Features
--------

- Reorder task dependencies in workflows. Movie and L1 quality tasks are no longer dependent on the presence of OUTPUT
  frames and thus can be run in parallel with the `WriteL1` task. (`#34 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/34>`__)


Misc
----

- Use CALIBRATED instead of OUTPUT frames in post-science movie and quality tasks. This doesn't change their output at all
  (the arrays are the same), but it's necessary for `dkist-processing-common >= 10.0.0` that will break using OUTPUT frames. (`#34 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/34>`__)


v0.10.1 (2024-09-19)
====================

Misc
----

- Bump `dkist-quality` to v1.1.1. This fixes raincloud plot rendering in trial workflows. (`#35 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/35>`__)


v0.10.0 (2024-09-11)
====================

Misc
----

- Accommodate changes to the GraphQL API associated with refactoring the quality database (`#33 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/33>`__)


v0.9.1 (2024-09-09)
===================

Misc
----

- Use High Memory worker for `InsturmentPolarizationCalibration` task.
  Writing the VIS demodulation matrices to disk is causing some memory issues on STAGE. (`#32 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/32>`__)


v0.9.0 (2024-09-09)
===================

Bugfixes
--------

- Perform Calibration Unit (CU) and demodulation matrix fits separately for each of the two polarized beams (instead of a
  single CU fit with the average of both beams). (`#30 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/30>`__)


v0.8.0 (2024-09-04)
===================

Features
--------

- Add support for multiple coadds in linearization task. (`#28 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/28>`__)
- Add camera-sample-sequence-based checks of ramp validity during linearization task. (`#29 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/29>`__)


v0.7.1 (2024-08-21)
===================

Misc
----

- Update some Quality related tasks and methods for the new API in `dkist-processing-common` v9.0.0. (`#27 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/27>`__)


Documentation
-------------

- Description of polcal bins in quality report no longer needs to include a dummy dimension. (`#27 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/27>`__)


v0.7.0 (2024-08-19)
===================

Features
--------

- Update linearity correction to average initial bias frames if more than one is found. Uses the last read NDR as opposed to the last NDR, which may be a bias NDR. (`#22 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/22>`__)


v0.6.4 (2024-08-15)
===================

Misc
----

- Move to version 4.6.0 of `dkist-fits-specifications` to correct allowed values of the TTBLTRCK header keyword.


v0.6.3 (2024-08-12)
===================

Misc
----

- Move to version 4.5.0 of `dkist-fits-specifications` which includes `PV1_nA` keys for non linear dispersion.


v0.6.2 (2024-08-05)
===================

Documentation
-------------

- Add pre-commit hook for documentation and edit README.rst. (`#18 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/18>`__)


v0.6.1 (2024-08-01)
===================

Misc
----

- Remove the loops from linear interpolation in remapping the ifu cube in order to speed up the code. (`#17 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/17>`__)


v0.6.0 (2024-07-30)
===================

Features
--------

- Update solar gain algorithm to compute a single characteristic spectrum across *all* slitbeams. This helps mitigate
  strong spectral gain feautres that exist across the entire spatial extent of a single slitbeam. (`#25 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/25>`__)


Bugfixes
--------

- Update "Avg Noise" QA metric computation to avoid errors caused by infinity values in the data. (`#16 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/16>`__)
- Calibrated L1 data no longer have large regions of all-NaN data at start and end of wavelength axis. This was fixed by
  constraining the reference "wavelength" axis to exclude regions with a large fraction of NaN values (the specific fraction is a parameter). (`#19 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/19>`__)
- Correctly parse the number of X/Y_tiles in cases where aborts lead to only a single complete mosaic/X_tile.
  This was very unlikely to happen in practice, but does come up in some of our tests. (`#20 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/20>`__)
- IFU cubes now have the correct spatial axis ordering. Previously the difference between numpy and cartesian ordering
  had caused the output spatial axes to be swapped. (`#21 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/21>`__)
- Preserve slitbeam scale differences in final solar gain image. This ensures that these real differences are corrected
  when the solar gain is applied to science data. (`#25 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/25>`__)


Misc
----

- Add DEBUG output to Science task that contains the stack slit spectra just prior to IFU remapping (called "SLIT_STACKED"). (`#25 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/25>`__)


v0.5.3 (2024-07-26)
===================

Misc
----

- Update dkist-processing-common to v8.2.2 to fix some warning messages. (`#24 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/24>`__)


v0.5.2 (2024-07-19)
===================

Misc
----

- Move to version 4.4.2 of `dkist-fits-specifications` which includes the `PVi_j` keywords.


v0.5.1 (2024-07-15)
===================

Bugfixes
--------

- Use `TrialTeardown` task in trial workflow. This task sets the recipe run status to TRIALSUCCESS. (`#15 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/15>`__)


v0.5.0 (2024-07-15)
===================

Features
--------

- L1 output files are now fully remapped IFU cubes! (`#8 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/8>`__)
- Add trial workflow for processing data without activating downstream Data Center services. This is useful for
  making "official" L1 data for assessing the performance of the pipeline. (`#10 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/10>`__)
- Add the `TransferDlnirspTrialData` task. This task is used to collect a set of file produced during a pipeline run
  and move them to a permanent location outside of the local (and ephemeral) scratch. (`#10 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/10>`__)


Misc
----

- Build and upload the Manual Processing Worker (mpw) notebooks as part of the Bitbucket release pipeline. (`#11 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/11>`__)
- Local trial workflows that don't depend on OBSERVE frames (solar-gain-as-science and polcal-as-science) now produce
  the full set of L1 outputs (except the inventory ASDF). (`#12 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/12>`__)
- Bump `dkist-quality` to version 1.1.0. (`#14 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/14>`__)


v0.4.0 (2024-07-12)
===================

Bugfixes
--------

- Correctly mock/populate OBS_IP_START_TIME in local trial workflows that don't use Observe frames. (`#9 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/9>`__)


Misc
----

- Move to version 8.2.1 of `dkist-processing-common` which includes the publication of select private methods for documentation purposes. (`#13 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/13>`__)


v0.3.0 (2024-07-01)
===================

Misc
----

- Move to version 8.1.0 of `dkist-processing-common` which includes an upgrade to airflow 2.9.2. (`#7 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/7>`__)


v0.2.1 (2024-06-25)
===================

Misc
----

- Remove High Memory Worker requirement from `InstrumentPolarizationCalibration` task. (Should have been part of `PR #4 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/4>`__)
- Pin `twine` to non-breaking version in BitBucket pipeline

v0.2.0 (2024-06-25)
===================

Features
--------

- Greatly reduce memory requirements of `InstrumentPolarizationCalibration` task (and speed it up a little bit, too). (`#4 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/4>`__)


Misc
----

- Use `nd_left_matrix_multiply` from `dkist-processing-math` and remove the local Mixin that had this method. (`#1 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/1>`__)
- Don't initialize a `parameters` object `DlnirspLinearityTaskBase`; we don't use parameters in Linearization. (`#1 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/1>`__)
- Update for new usage of `_find_most_recent_past_value` now requiring `obs_ip_start_time` or explicit time.
- Use `asdf` codecs from `dkist-processing-common` instead of locally defined codecs (they were the same). (`#1 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/1>`__)
- Use `ParameterArmIdMixin` and `_load_param_value_from_fits` from `dkist-processing-common` (they're identical). (`#1 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/1>`__)
- Update all non-DKIST dependencies (and `dkist-processing-pac`) to current versions. (`#2 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/2>`__)
- Remove crufty "build_docs" and "upload_docs" from setup.cfg. (`#2 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/2>`__)
- Put `GroupIdMixin` on `DlnirspTaskBase` instead of using it separately for each Task class. This also helps
  soften the dependencies of the `CorrectionsMixin` on `GroupIdMixin` because now the presence of the `group_id_*` methods
  is guaranteed. (`#3 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/3>`__)
- Use pre-defined `*Tag.task_FOO()` tags and controlled `TaskName.foo` values, when available. (`#5 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/5>`__)


v0.1.1 (2024-06-12)
===================

Misc
----

- Bump `dkist-fits-specifications` to v4.3.0. We need this in DL-NIRSP so some dither-related keywords are no longer required.
  (They are only present if dithering is used). (`#6 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/6>`__)


v0.1.0 (2024-06-06)
===================

- Initial release. Mostly for first release to DC stacks (i.e., not "production" quality).
