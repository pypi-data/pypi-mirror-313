"""
Define some system settings.

.. codeauthor:: Laurent Mertens <laurent.mertens@kuleuven.be>
"""
import os


class Config:
    #: Users system home dir
    HOME_DIR = os.path.expanduser('~')

    #: Parent folder containing the codebase; MAKE SURE TO UPDATE THIS VALUE TO REFLECT YOUR SETUP!
    DIR_CODE = os.path.join(HOME_DIR, 'Path', 'To', 'Repo', 'Folder')
    DIR_DATA = os.path.abspath(os.path.join(DIR_CODE, 'data'))
    # Scraped images
    DIR_IMAGES = os.path.join(DIR_DATA, "AnnImagesProlific")
