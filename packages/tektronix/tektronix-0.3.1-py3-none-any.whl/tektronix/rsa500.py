# -*- coding: utf-8 -*-
# Copyright (c) 2013-2024 The tektronix developers. All rights reserved.
# Project site: https://github.com/questrail/tektronix
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Read a CSV file saved by a RSA500 Spectrum Analyzer"""

# Standard module imports
import csv
import logging
import os
import sys

# Data analysis related imports
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO, format=" %(asctime)s -  %(levelname)s - %(message)s"
)


def read_csv_file(filename):
    """Read csv file into a numpy array"""
    header = {}
    infile = open(filename, "r", newline="", encoding="utf8")

    with infile as csvfile:
        reader = csv.reader((line.replace("\0", "") for line in csvfile), delimiter=",")
        header["file"] = os.path.basename(filename)
        temp_row = next(reader)
        if temp_row[0] == "Spectrum":
            ver = 0
        elif temp_row[0] == "Spectrum 1":
            ver = 1
        else:
            logging.error("Unknown csv filetype: %s", temp_row[0])
            sys.exit(1)
        logging.info("RSA500 CSV ver %s", ver)
        header["timestamp"] = temp_row[1]
        if ver == 0:
            temp_row = next(reader)
            temp_row = next(reader)
            header["center_freq"] = float(temp_row[1])
            header["center_freq_units"] = temp_row[2]
            temp_row = next(reader)
            header["ref_level"] = float(temp_row[1])
            header["ref_level_units"] = temp_row[2]
        else:
            # Read until we find the Center Frequency.
            while True:
                temp_row = next(reader)
                if len(temp_row) == 3 and temp_row[0] == "Center Frequency":
                    break
            header["center_freq"] = float(temp_row[1])
            header["center_freq_units"] = temp_row[2]
            temp_row = next(reader)
            header["ref_level"] = float(temp_row[1])
            header["ref_level_units"] = temp_row[2]

        # Read until we find the [Parameters] section.
        while True:
            temp_row = next(reader)
            if len(temp_row) == 1 and temp_row[0] == "[Parameters]":
                break

        temp_row = next(reader)
        header["span_freq"] = float(temp_row[1])
        header["span_freq_units"] = temp_row[2]
        temp_row = next(reader)
        header["resolution_bw"] = float(temp_row[1])
        header["resolution_bw_units"] = temp_row[2]
        temp_row = next(reader)
        header["rbw_window_type"] = temp_row[1]

        # Read until we find the [Traces] section.
        while True:
            temp_row = next(reader)
            if len(temp_row) == 1 and temp_row[0] == "[Traces]":
                break
        temp_row = next(reader)
        temp_row = next(reader)
        temp_row = next(reader)
        num_points = int(temp_row[1])
        header["num_points"] = num_points
        # FIXME(mdr): I need an example file with multiple traces to determine
        # how to parse more than just a single trace.
        num_traces = 1
        header["num_traces"] = num_traces
        temp_row = next(reader)
        header["frequency_unit"] = temp_row[2]
        temp_row = next(reader)

        data_array = []

        for _ in range(num_points):
            temp_row = next(reader)
            data_array.append((float(temp_row[1]), float(temp_row[0])))
            data = np.array(
                data_array,
                dtype={
                    "names": ("frequency", "amplitude"),
                    "formats": ("f8", "f8"),
                },
            )

    return (header, data)
