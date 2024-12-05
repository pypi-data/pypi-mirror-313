"""Facility with operations for system testing case 0001."""

### standard library imports

from pathlib import Path

from zipfile import ZipFile

from ast import literal_eval

from tempfile import mkstemp


### local imports
from ...config import APP_REFS, SYSTEM_TESTING_DATA_DIR



TEMP_FILEPATH = []

FRAME_ASSERTION_MAP = {}


def perform_setup(data):
    """Prepare and reference test data.

    This is done here by:

    - loading and referencing input data
    - copying contents of a .ndz file in a temporary location
    """

    ### load and reference input data

    with ZipFile(
        str(SYSTEM_TESTING_DATA_DIR / 'test_cases' / 'stc0001.zip'),
        mode='r',
    ) as archive:

        with archive.open('input_data.pyl', mode='r') as input_data_file:

            data.input_data = (
                literal_eval(input_data_file.read().decode(encoding='utf-8'))
            )

    ### load contents of a .ndz file

    with ZipFile(
        str(SYSTEM_TESTING_DATA_DIR / 'shared' / 'file_with_objects.zip'),
        mode='r',
    ) as archive:

        with archive.open('file_with_objects.ndz', mode='r') as file_to_load:
            ndz_text = file_to_load.read().decode(encoding='utf-8')

    ### save the contents in a temporary file and reference it

    temporary_filepath = Path(mkstemp(suffix='.ndz', text=True)[1])

    temporary_filepath.write_text(ndz_text, encoding='utf-8')

    data.filepath = temporary_filepath

    ### store the path to the temporary file so we can remove it after the
    ### test finishes
    TEMP_FILEPATH.append(temporary_filepath)


def ensure_collections_are_populated(append_assertion_data):
    """Ensure collections have the expected amount of items.

    Parameters
    ==========
    append_assertion_data (callable)
        Used to store the results of assertions.
    """
    ### confirm 01 text box exists

    ## grab the text blocks
    text_blocks = APP_REFS.gm.text_blocks

    ## 01 item in APP_REFS.gm.text_blocks

    append_assertion_data(

        (

            (
                "The loaded file must contain 01 object"
                " in APP_REFS.gm.text_blocks"
            ),

            len(text_blocks) == 1,

        )

    )

    ### confirm 08 nodes exist

    ## grab the nodes iterable
    nodes = APP_REFS.gm.nodes

    ## the "nodes" iterable must contain 8 items

    append_assertion_data(
        (
            "The loaded file must contain 08 items in APP_REFS.gm.nodes",
            len(nodes) == 8,
        )
    )

FRAME_ASSERTION_MAP[0] = ensure_collections_are_populated


def perform_final_assertions(append_assertion_data):
    """Confirm no objects remain on the loaded file.

    Parameters
    ==========
    append_assertion_data (callable)
        Used to store the results of assertions.
    """
    ### confirm no text boxes exist

    ## grab the text blocks
    text_blocks = APP_REFS.gm.text_blocks

    ## no items in APP_REFS.gm.text_blocks

    append_assertion_data(
        (
            "There must be no objects in APP_REFS.gm.text_blocks",
            len(text_blocks) == 0,
        )
    )


    ### confirm no nodes exist

    ## grab the nodes iterable
    nodes = APP_REFS.gm.nodes

    ## the "nodes" iterable must contain no items

    append_assertion_data(
        (
            "There must be no items in APP_REFS.gm.nodes",
            len(nodes) == 0,
        )
    )


def perform_teardown():
    """Remove temporary path from our list and the file from the disk."""
    TEMP_FILEPATH.pop().unlink()
