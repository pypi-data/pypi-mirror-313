"""

.. codeauthor:: Laurent Mertens <laurent.mertens@kuleuven.be>
"""
import os


def read_annotations():
    # Path to the annotations_single.ann file
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(abs_dir, "annotations_single.ann")) as fin:
        data = fin.read()

    return data
