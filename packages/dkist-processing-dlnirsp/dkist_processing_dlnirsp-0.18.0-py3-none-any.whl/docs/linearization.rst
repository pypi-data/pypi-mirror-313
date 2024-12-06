Linearization
=============

Introduction
------------

Two of the DLNIRSP cameras (arms 2 and 3) use infrared (IR) H2RG detectors, which have non-linear response to light with increasing exposure time.
Because of this non-linear response, the count values at the final exposure do not accurately represent the light falling on the chip and therefore need to be corrected.
This correction is performed very early in the pipeline by the `~dkist_processing_dlnirsp.tasks.linearity_correction` task.

IR cameras make multiple readouts over the course of a single exposure and these readouts do not clear charge from the detector.
Because these reads are non-destructive they are referred to as Non-Destructive Readouts (NDRs).
The set of NDRs from the same exposure is called a ramp and typically the NDRs are evenly spaced over the full exposure time.
The linearization task uses all NDRs associated with a single ramp to compute what the final count values at the desired exposure time would be if the response of the detector was linear.
Thus, a single ramp (i.e., set of NDRs) is processed to produce a single "linearized" frame.

Linearization Algorithms
------------------------

The IR cameras on DLNIRSP currently only operate in a single readout mode, but others are technically possible.
This page will be updated as new modes are commissioned.

UpTheRamp
^^^^^^^^^

In this mode a ramp consists of 1 or more "bias" or "line" NDRs followed by a sequence of "read" NDRs.
The line NDRs serve to reset the camera and the read NDRs are used to acquire data.
A single set of line-then-read NDRs is called a "coadd" and a single ramp may contain multiple coadds to achieve higher signal-to-noise while keeping the exposure time of a single coadd low enough to avoid saturation.

Each coadd is linearized by subtracting the average of all line NDRs from the last read NDR; i.e., the average bias signal is subtracted from the most-exposed read NDR.
If a ramp contains multiple coadds then they are averaged together to produce the linearized frame.
