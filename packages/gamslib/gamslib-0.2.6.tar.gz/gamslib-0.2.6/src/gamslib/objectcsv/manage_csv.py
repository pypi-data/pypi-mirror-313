"""Function do collect and update csv files."""

import logging
from pathlib import Path

from gamslib.objectcsv.objectcsv import ObjectCSV

from .utils import find_object_folders

logger = logging.getLogger()


def collect_csv_data(
    object_root_dir: Path,
    output_dir: Path | None = None,
    object_filename: str | None = None,
    datastream_filename: str | None = None,
) -> ObjectCSV:
    """Collect csv data from all object folders below object_root_dir.

    This function collects all data from all object.csv and all datastream.csv files
    below root_dir.
    The collected data is stored in two files: object.csv_file and ds_file. These files
    are created in object_root_dir if no other output directory is se
    via output_dir.

    Returns the Path to all_objects.csv and all_datastreams.csv as tuple of Path objects.
    """
    # This is were we put all collected data
    all_objects_csv = ObjectCSV(output_dir or object_root_dir)
    for objectfolder in find_object_folders(object_root_dir):
        obj_csv = ObjectCSV(objectfolder)

        for objmeta in obj_csv.get_objectdata():
            all_objects_csv.add_objectdata(objmeta)
        for dsmeta in obj_csv.get_datastreamdata():
            all_objects_csv.add_datastream(dsmeta)

    if object_filename is None:
        object_filename = "all_objects.csv"
    if datastream_filename is None:
        datastream_filename = "all_datastreams.csv"
    all_objects_csv.write(
        all_objects_csv.object_dir, object_filename, datastream_filename
    )
    return all_objects_csv


def update_csv_files(
    object_root_dir: Path,
    collected_csv_dir: Path | None = None,
    object_csv: str = "all_objects.csv",
    ds_csv: str = "all_datastreams.csv",
) -> tuple[int, int]:
    """Update csv metadata files with data from the combined csv data.

    If collected_csv_dir is None, we assume that the directory
    containing the combined csv data is object_root. This is
    where collect_csv_data() stores the data by default.

    In other words: this function updates all object and datatstream
    metadata with data changed in the central csv files.

    Returns a a tuple of ints: number of updated objects and number of updated datastreams.
    """
    num_of_changed_objects = 0
    num_of_changed_datastreams = 0

    if collected_csv_dir is None:
        collected_csv_dir = object_root_dir
    all_objects_csv = ObjectCSV(collected_csv_dir, object_csv, ds_csv)

    for objectfolder in find_object_folders(object_root_dir):
        obj_csv = ObjectCSV(objectfolder)
        obj_csv.clear()
        for obj_data in all_objects_csv.get_objectdata(obj_csv.object_id):
            obj_csv.add_objectdata(obj_data)
            num_of_changed_objects += 1

        for ds_data in all_objects_csv.get_datastreamdata(obj_csv.object_id):
            obj_csv.add_datastream(ds_data)
            num_of_changed_datastreams += 1
        obj_csv.write()

    return num_of_changed_objects, num_of_changed_datastreams
