"""Test the objectcsv.create_csv module.
"""
# pylint: disable=W0212 # access to ._data
import csv
from dataclasses import fields
from pathlib import Path

import pytest

from pytest import fixture

from gamslib.objectcsv import ObjectData
from gamslib.objectcsv.create_csv import (
    DEFAULT_RIGHTS,
    create_csv,
    create_csv_files,
    extract_dsid,
    get_rights,
)
from gamslib.objectcsv.dublincore import DublinCore
from gamslib.objectcsv.objectcsv import DSData
from gamslib.projectconfiguration.configuration import Configuration



@fixture(name="test_config")
def config_fixture(datadir):
    "Return a conguration object."
    return Configuration.from_toml(datadir / "project.toml")


@fixture(name="test_dc")
def dc_fixture(datadir):
    "Return a DublinCore object."
    return DublinCore(datadir / "objects" / "obj1" / "DC.xml")


def test_get_rights(test_config, test_dc):
    """Test the get_rights function."""
    # If set in dc file, this value should be returned.
    assert get_rights(test_config, test_dc) == "Rights from DC.xml"

    # if not set in DC, use the value from the project configuration
    test_dc._data["rights"] = {"unspecified": [""]}
    assert get_rights(test_config, test_dc) == "Rights from project.toml"

    # if not set in configuration either, use the default value
    test_config.metadata.rights = ""
    assert get_rights(test_config, test_dc) == DEFAULT_RIGHTS


def test_create_csv(datadir, test_config):
    """Test the create_csv function."""
    object_dir = datadir / "objects" / "obj1"
    create_csv(object_dir, test_config)

    # check contents of the newly created object.csv file
    obj_csv = object_dir / "object.csv"
    with open(obj_csv, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == [field.name for field in fields(ObjectData)]
        assert list(reader)[0]["project"] == "Test Project"

    # check contents of the newly datastreams.csv file
    ds_csv = object_dir / "datastreams.csv"
    with open(ds_csv, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == [field.name for field in fields(DSData)]
        data = list(reader)
        assert len(data) == 2
        assert data[0]["dsid"] == "DC.xml"
        assert data[1]["dsid"] == "SOURCE.xml"


def test_create_csv_files_existing_csvs(datadir, test_config):
    """If the csv files already exist, they should not be overwritten."""
    object_dir = datadir / "objects"
    (object_dir / "obj1" / "object.csv").touch()
    (object_dir / "obj2" / "datastreams.csv").touch()

    assert len(create_csv_files(object_dir, test_config)) == 0


def test_create_csv_files(datadir, test_config):
    """The create_csv_files function should create the csv files for all objects."""
    objects_root_dir = datadir / "objects"
    processed_folders = create_csv_files(objects_root_dir, test_config)
    assert len(processed_folders) == 2

    # Check if all csv files have been created
    assert (objects_root_dir / "obj1" / "object.csv").exists()
    assert (objects_root_dir / "obj1" / "datastreams.csv").exists()
    assert (objects_root_dir / "obj2" / "object.csv").exists()
    assert (objects_root_dir / "obj2" / "datastreams.csv").exists()


def test_extract_dsid():
    """Test the extract_dsid function."""
    # normal cases
    assert extract_dsid(Path("test.jpeg"), True) == "test.jpeg"
    assert extract_dsid(Path("test.jpeg"), False) == "test"
    assert extract_dsid(Path("test.jpeg"), True) == "test.jpeg"

    # str instead of Path
    assert extract_dsid("test.jpeg", True) == "test.jpeg"

    # invalid pid
    with pytest.raises(ValueError):
        extract_dsid(Path("täst"))

    # remove extension with suffix unknown to mimetypes
    assert extract_dsid(Path("test.unknown"), False) == "test"

    # if it does not seem to be an extension, keep it
    assert extract_dsid(Path("test.1234"), False) == "test.1234"
    assert extract_dsid(Path("test.a1234"), False) == "test.a1234"
