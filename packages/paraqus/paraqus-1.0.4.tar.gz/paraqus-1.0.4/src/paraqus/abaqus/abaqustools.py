# -*- coding: utf-8 -*-
#
#   Paraqus - A VTK exporter for FEM results.
#
#   Copyright (C) 2022, Furlan, Stollberg and Menzel
#
#    This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.
"""
Helper functions/types to read results from Abaqus ODBs.

All of these can only be executed in Abaqus Python.

"""
import os
import shutil

from abaqus import session


class OdbObject(object):
    """
    Context manager for Abaqus ODB objects.

    Opens an ODB and closes it after we are done with it. If any
    exceptions are raised while the ODB is open, it is still closed
    afterwards.

    Parameters
    ----------
    file_name : str
        Path to the Abaqus .odb file.
    readonly : bool, optional
        If ``True`` writing to the ODB is prohibited. Default is
        ``True``.

    Attributes
    ----------
    file_path : str
        Absolute path to the .odb file.
    readonly : bool
        If ``True`` writing to the ODB is prohibited.
    already_open : bool
        A flag indicating wheter the ODB is already open or not.

    """

    def __init__(self, file_name, readonly=True):
        self.file_path = os.path.abspath(file_name)
        self.readonly = readonly
        self.already_open = False
        self.odb = None

    def __enter__(self):

        # Make sure to compare with absolute paths
        keys = [os.path.abspath(k) for k in session.odbs.keys()]

        # If the odb is already open, just return the odb object
        if self.file_path in keys:
            # ODB is already open
            self.already_open = True
            return session.odbs[self.file_path]

        # Otherwise, open it and return the object
        upgrade_odb(self.file_path)
        odb = session.openOdb(name=self.file_path,
                              readOnly=self.readonly)

        # Deal with silent errors in the readonly status, this happens
        # e.g. when a lock file prevents write access
        assert odb.isReadOnly == self.readonly, \
            "The ODB could not be opened with option readonly={}" \
            .format(self.readonly)

        self.odb = odb

        return odb

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Only close the odb if it was not open before we "opened" it
        if not self.already_open:
            self.odb.close()


def upgrade_odb(odb_file):
    """
    Upgrade an ODB if necessary.

    A subfolder is created for the original ODB files if an upgrade is
    performed.

    Parameters
    ----------
    odb_file : str
        Path to the Abaqus ODB.

    Returns
    -------
    bool
        Whether the ODB was updated.

    """
    upgrade_required = session.isUpgradeRequiredForOdb(odb_file)

    if upgrade_required:
        # Make sure we work with absolute paths
        odb_file = os.path.abspath(odb_file)

        # Create new directory for upgraded files
        new_directory = os.path.join(os.path.dirname(odb_file),
                                     "odbs_before_upgrades")

        if not os.path.isdir(new_directory):
            os.mkdir(new_directory)

        backup_file_name = os.path.basename(odb_file)

        backup_file_path = os.path.join(new_directory, backup_file_name)

        # Move the original odb to the backup folder
        shutil.move(odb_file, backup_file_path)

        # Upgrade the odb file
        session.upgradeOdb(existingOdbPath=backup_file_path,
                           upgradedOdbPath=odb_file)

        print("The ODB file '{}' has been updated.".format(odb_file))
        print("The original file has been stored in the path '{}'"
              .format(backup_file_path))

        return True

    return False
