###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import os
import sys
from pathlib import Path

import pytest
import skhep_testdata as hepdat
import uproot

from LbExec.__main__ import parse_args

LBEXEC_CMD = ["lbexec"]
OPTIONS_FN = str(Path(__file__).parent / "example.yaml")
OPTIONS_FN_COMPRESSION = str(Path(__file__).parent / "example_compression.yaml")
OPTIONS_FN_COMPRESSION_BAD = str(Path(__file__).parent / "example_compresion_bad.yaml")
OPTIONS_FN_SIMPLE_MERGE = str(Path(__file__).parent / "example_simple_merge.yaml")
FUNCTION_SPEC = "LbExec:skim_files"
LBEXEC_EXAMPLE_CMD = LBEXEC_CMD + [FUNCTION_SPEC, OPTIONS_FN]


def getfkeys(rf):
    return [key.split(";")[0] for key in rf.keys()]


if not os.path.exists("tests/tuple1.root"):
    with uproot.open(hepdat.data_path("uproot-HZZ.root")) as rf:
        testtree = rf["events"].arrays(
            [
                "NMuon",
                "NElectron",
                "NPhoton",
                "MET_px",
                "MET_py",
                "MChadronicBottom_px",
                "MChadronicBottom_py",
                "MChadronicBottom_pz",
                "MChadronicWDecayQuark_px",
                "MChadronicWDecayQuark_py",
                "MChadronicWDecayQuark_pz",
                "MClepton_px",
                "MClepton_py",
                "MClepton_pz",
                "MCneutrino_px",
                "MCneutrino_py",
                "MCneutrino_pz",
                "NPrimaryVertices",
                "EventWeight",
            ]
        )
        testlumitree = rf["events"].arrays(
            [
                "EventWeight",
            ]
        )

        f1 = uproot.recreate("tests/tuple1.root")
        f1["events1/DecayTree"] = testtree
        f1["events2/DecayTree"] = testtree
        f1["GetIntegratedLuminosity/LumiTuple"] = testlumitree
        f2 = uproot.recreate("tests/tuple2.root")
        f2["events1/DecayTree"] = testtree
        f2["events2/DecayTree"] = testtree
        f2["GetIntegratedLuminosity/LumiTuple"] = testlumitree


@pytest.mark.parametrize(
    "function_spec,options_spec,extra_args",
    [
        [
            "LbExec:skim_and_merge",
            OPTIONS_FN,
            ["--write", "EVENTS1=events1", "--write", "EVENTS2=events2"],
        ],
        [
            "LbExec:skim_and_merge",
            OPTIONS_FN_COMPRESSION,
            [
                "--write",
                "EVENTS1=events1",
                "--write",
                "EVENTS2=events2",
            ],
        ],
        [
            "LbExec:skim_and_merge",
            OPTIONS_FN,
            ["--write", "_EVENTS2=events2", "--allow-missing"],
        ],
        [
            "LbExec:skim_and_merge",
            OPTIONS_FN_SIMPLE_MERGE,
            [],
        ],
        [
            # duplicates
            "LbExec:skim_and_merge",
            OPTIONS_FN,
            [
                "--write",
                "__EVENTS1=events1",
                "--write",
                "__EVENTS2=events2",
                "--write",
                "__EVENTS22=events2",
                "--allow-duplicates",
            ],
        ],
    ],
)
def test_valid_workflow(capfd, monkeypatch, function_spec, options_spec, extra_args):
    monkeypatch.setattr(
        sys, "argv", LBEXEC_CMD + [function_spec, options_spec] + ["--"] + extra_args
    )

    parse_args()
    captured = capfd.readouterr()

    if "EVENTS1=events1" in extra_args:
        assert "SKIM directory events1" in captured.err
    assert "SKIM directory events2" in captured.err

    if "EVENTS1=events1" in extra_args:
        with uproot.open("tests/output.EVENTS1.root") as rf:
            keys = getfkeys(rf)
            assert "GetIntegratedLuminosity/LumiTuple" in keys
            assert "events1/DecayTree" in keys
            assert "events2/DecayTree" not in keys
    with uproot.open("tests/output.EVENTS2.root") as rf:
        keys = getfkeys(rf)
        assert "GetIntegratedLuminosity/LumiTuple" in keys
        assert "events2/DecayTree" in keys
        assert "events1/DecayTree" not in keys

    if "--allow-duplicates" in extra_args:
        with uproot.open("tests/output.__EVENTS1.root") as rf:
            keys = getfkeys(rf)
            assert "GetIntegratedLuminosity/LumiTuple" in keys
            assert "events2/DecayTree" not in keys
            assert "events1/DecayTree" in keys
        with uproot.open("tests/output.__EVENTS2.root") as rf:
            keys = getfkeys(rf)
            assert "GetIntegratedLuminosity/LumiTuple" in keys
            assert "events2/DecayTree" in keys
            assert "events1/DecayTree" not in keys
        with uproot.open("tests/output.__EVENTS22.root") as rf:
            keys = getfkeys(rf)
            assert "GetIntegratedLuminosity/LumiTuple" in keys
            assert "events2/DecayTree" in keys
            assert "events1/DecayTree" not in keys


@pytest.mark.parametrize(
    "function_spec,options_spec,extra_args",
    [
        [
            # no missing objects
            "LbExec:skim_and_merge",
            OPTIONS_FN,
            ["--write", "_EVENTS2=events2"],
        ],
        [
            # no duplicates
            "LbExec:skim_and_merge",
            OPTIONS_FN,
            [
                "--write",
                "EVENTS1=events1",
                "--write",
                "EVENTS2=events2",
                "--write",
                "EVENTS22=events2",
            ],
        ],
        [  # nonsense algorithm name
            "LbExec:skim_and_merge",
            OPTIONS_FN_COMPRESSION_BAD,
            [
                "--write",
                "EVENTS1=events1",
                "--write",
                "EVENTS2=events2",
            ],
        ],
    ],
)
def test_invalid_workflow(capfd, monkeypatch, function_spec, options_spec, extra_args):
    monkeypatch.setattr(
        sys, "argv", LBEXEC_CMD + [function_spec, options_spec] + ["--"] + extra_args
    )
    with pytest.raises(SystemExit):
        parse_args()
    captured = capfd.readouterr()

    if "EVENTS22=events2" in extra_args:
        assert "Duplicates of directory" in captured.err

    if "_EVENTS22=events2" in extra_args:
        assert (
            "Some directories of the input files would not be copied to any output files"
            in captured.err
        )

    if OPTIONS_FN_COMPRESSION == options_spec:
        assert "Unknown compression algorithm" in captured.err
