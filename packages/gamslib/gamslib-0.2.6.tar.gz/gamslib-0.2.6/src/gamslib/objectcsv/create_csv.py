"""Create object.csv and datastreams.csv files.

This module creates the object.csv and datastreams.csv files for one or many given
object folder. It uses data from the DC.xml file and the project configuration 
to fill in the metadata. When not enough information is available, some fields 
will be left blank or filled with default values.
"""

import logging
import mimetypes
import re
from pathlib import Path

from gamslib.projectconfiguration import Configuration

from .objectcsv import DSData, ObjectCSV, ObjectData
from .dublincore import DublinCore
from .utils import find_object_folders

logger = logging.getLogger()

DEFAULT_RIGHTS = (
    "Creative Commons Attribution-NonCommercial 4.0 "
    "(https://creativecommons.org/licenses/by-nc/4.0/)"
)
DEFAULT_SOURCE = "local"
DEFAULT_OBJECT_TYPE = "text"

NAMESPACES = {
    "dc": "http://purl.org/dc/elements/1.1/",
}


def get_rights(config: Configuration, dc: DublinCore) -> str:
    """Get the rights from various sources.

    Lookup in this ortder:

      1. Check if set in dublin core
      2. Check if set in the configuration
      3. Use a default value.
    """
    rights = dc.get_element_as_str("rights", default="")
    if not rights:  # empty string is a valid value
        if config.metadata.rights:
            rights = config.metadata.rights
        else:
            rights = DEFAULT_RIGHTS
    return rights


def extract_dsid(datastream: Path | str, keep_extension=True) -> str:
    """Extract and validate the datastream id from a datastream path.

    If remove_extension is True, the file extension is removed from the PID.
    """
    if isinstance(datastream, str):
        datastream = Path(datastream)

    pid = datastream.name

    if not keep_extension:
        # not everything after the last dot is an extension :-(
        mtype = mimetypes.guess_type(datastream)[0]
        if mtype is None:
            known_extensions = []
        else:
            known_extensions = mimetypes.guess_all_extensions(mtype)
        if datastream.suffix in known_extensions:
            pid = pid.removesuffix(datastream.suffix)
            logger.debug("Removed extension '%s' for ID: %s", datastream.suffix, pid)
        else:
            parts = pid.split(".")
            if re.match(r"^[a-zA-Z]+\w?$", parts[-1]):
                pid = ".".join(parts[:-1])
                logger.debug("Removed extension for ID: %s", parts[0])
            else:
                logger.warning(
                    "'%s' does not look like an extension. Keeping it in PID.", pid[-1]
                )

    if re.match(r"^[a-zA-Z0-9]+[-.%_a-zA-Z0-9]+[a-zA-Z0-9]+$", pid) is None:
        raise ValueError(f"Invalid PID: '{pid}'")

    logger.debug(
        "Extracted PID: %s from %s (keep_extension=%s)", pid, datastream, keep_extension
    )
    return pid


def collect_object_data(pid: str, config: Configuration, dc: DublinCore) -> ObjectData:
    """Find data for the object.csv by examining dc file and configuration.

    This is the place to change the resolving order for data from other sources.
    """

    title = "; ".join(dc.get_element("title", default=pid))
    description = "; ".join(dc.get_element("description", default=""))

    return ObjectData(
        recid=pid,
        title=title,
        project=config.metadata.project_id,
        description=description,
        creator=config.metadata.creator,
        rights=get_rights(config, dc),
        source=DEFAULT_SOURCE,
        objectType=DEFAULT_OBJECT_TYPE,
    )


def collect_datastream_data(
    ds_file: Path, config: Configuration, dc: DublinCore
) -> DSData:
    """Collect data for a single datastream."""
    dsid = extract_dsid(ds_file, config.general.dsid_keep_extension)

    # I think it's not possible to derive a ds title or description from the DC file
    # title = "; ".join(dc.get_element("title", default=dsid)) # ??
    # description = "; ".join(dc.get_element("description", default="")) #??

    return DSData(
        dspath=str(ds_file.relative_to(ds_file.parents[1])),  # objectsdir
        dsid=dsid,
        title="",
        description="",
        mimetype=mimetypes.guess_type(ds_file)[0] or "",
        creator=config.metadata.creator,
        rights=get_rights(config, dc),
    )


def create_csv(
    object_directory: Path, configuration: Configuration
) -> ObjectCSV | None:
    """Generate the csv file containing the preliminary metadata for a single object."""
    objectcsv = ObjectCSV(object_directory)

    # Avoid that existing (and potentially already edited) metadata is replaced
    if not objectcsv.is_new():
        logger.info(
            "CSV files for object '%s' already exist. Will not be re-created.",
            objectcsv.object_id,
        )
        return None

    dc = DublinCore(object_directory / "DC.xml")
    objectcsv.add_objectdata(
        collect_object_data(objectcsv.object_id, configuration, dc)
    )
    for ds_file in object_directory.glob("*"):
        if ds_file.is_file() and ds_file.name not in ("object.csv", "datastreams.csv"):
            objectcsv.add_datastream(
                # collect_datastream_data(ds_file, objectcsv.object_id, configuration, dc)
                collect_datastream_data(ds_file, configuration, dc)
            )
    objectcsv.write()
    return objectcsv


def create_csv_files(root_folder: Path, config: Configuration) -> list[ObjectCSV]:
    """Create the CSV files for all objects below root_folder."""
    extended_objects: list[ObjectCSV] = []
    for path in find_object_folders(root_folder):
        extended_obj = create_csv(path, config)

        if extended_obj is not None:
            extended_objects.append(extended_obj)
    return extended_objects
