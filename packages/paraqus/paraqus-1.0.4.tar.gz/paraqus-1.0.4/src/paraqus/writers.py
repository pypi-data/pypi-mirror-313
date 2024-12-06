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
This module keeps all writers for the different output format, e.g.
ASCII and binary. Related tools such as VtkFileManager should also be
stored here. Note, that currently only unstructured grids are
supported.

"""
import os
import sys
from os import path
import shutil
import itertools
from abc import ABCMeta, abstractmethod
import struct
import base64

import numpy as np

from paraqus.constants import (BYTE_ORDER_CHAR, ASCII, BINARY, BYTE_ORDER,
                               BASE64, RAW, UINT64, NODES, ELEMENTS)

# Version string for the vtk version that is supported
VTK_VERSION_MAJOR = 1
VTK_VERSION_MINOR = 0
VTK_VERSION_STRING = str(VTK_VERSION_MAJOR) + \
    "." + str(VTK_VERSION_MINOR)

# Mapper for data types used in vtk files
VTK_TYPE_MAPPER = {"int8":    "Int8",
                   "uint8":   "UInt8",
                   "int16":   "Int16",
                   "uint16":  "UInt16",
                   "int32":   "Int32",
                   "uint32":  "UInt32",
                   "int64":   "Int64",
                   "uint64":  "UInt64",
                   "float32": "Float32",
                   "float64": "Float64",
                   }

# Mapper for binary data types
BINARY_TYPE_MAPPER = {"int8": "b",
                      "uint8": "B",
                      "int16": "h",
                      "uint16": "H",
                      "int32": "i",
                      "uint32": "I",
                      "int64": "q",
                      "uint64": "Q",
                      "float32": "f",
                      "float64": "d",
                      }

# Mapper for the header size in case of packed binary data
BINARY_HEADER_SIZE_MAPPER = {"uint32": 4,
                             "uint64": 8}


class VtkFileManager(object):
    r"""
    Context manager for VTK file reading and writing.

    Can handle all kinds of supported VTK files, i.e. .vtu, .pvtu and
    .pvd files. Files can only be opened in write mode.

    Parameters
    ----------
    file_name : str
        The name of the VTK file that will be written.
    fmt : ParaqusConstant
        Constant defining the output format of array data, i.e.
        ``ASCII`` or ``BINARY``.

    Attributes
    ----------
    file_path : str
        The absolute path to the VTK file.
    fmt : ParaqusConstant
        Constant defining the output format of array data, i.e.
        ``ASCII`` or ``BINARY``.

    Example
    -------
    >>> from paraqus.constants import BINARY
    >>> with VtkFileManager("my_file.vtu", BINARY) as vtu_file:
    >>>     vtu_file.write("<VTKFile>\n")
    >>>     vtu_file.write("<UnstructuredGrid>\n")
    >>>     vtu_file.write("</UnstructuredGrid>\n")
    >>>     vtu_file.write("</VTKFile>\n")

    """

    def __init__(self, file_name, fmt):

        extension = path.splitext(file_name)[1]
        if extension not in (".vtu", ".pvtu", ".pvd"):
            raise ValueError(
                "File format '{}' is not a supported VTK file format."
                .format(extension))

        self._file_path = path.abspath(file_name)
        self._fmt = fmt
        self._file = None

    @property
    def file_path(self):
        """The absolute path to the VTK file."""
        return self._file_path

    @property
    def fmt(self):
        """The output format for array data."""
        return self._fmt

    def __enter__(self):
        """Open the file, in binary mode if needed."""
        # In Python 2.7 it seems to make no difference whether one is
        # writing pure string via a binary file stream or an ascii file
        # stream, thus just keep this as it is without checking the
        # version
        if self.fmt == ASCII:
            self._file = open(self.file_path, "w")
        elif self.fmt == BINARY:
            self._file = open(self.file_path, "wb")
        else:
            raise ValueError(
                "Format '{}' not supported.".format(self.fmt))

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close the file."""
        self._file.close()

    def write(self, output):
        """
        Write ASCII or binary data into the corresponding VTK file.

        Parameters
        ----------
        output : str or bytes
            The output that will be written into the file.

        Returns
        -------
        None.

        """
        # In Python 2.7 struct.pack returns a string, that somehow
        # can not be converted to a binary string but it makes no
        # difference anyway (see comment in methode __enter__). In
        # Python 3 binary string are obligatory
        if sys.version_info >= (3,):
            if isinstance(output, str) and self.fmt is BINARY:
                self._file.write((output).encode("ascii"))
            elif isinstance(output, str) and self.fmt is ASCII:
                self._file.write(output)
            else:
                self._file.write(output)

        else:
            self._file.write(output)


class WriterBaseClass(object):
    """
    Base class for VTK writers.

    All writers must be derived from this class. The class contains
    methods that do not depend on the output format and, thus, will
    be the same for all writers.

    Parameters
    ----------
    fmt : ParaqusConstant
        Format of the writer. Can be ``ASCII`` or ``BINARY``.
    output_dir : str, optional
        Directory, where all exported VTK files will be stored. Default:
        ``'vtk_files'``.
    clear_output_dir : bool, optional
        If ``True``, the output directory will be cleared before
        exporting any files. Default: ``False``.
    number_of_pieces : int, optional
        Number of pieces each model will be split into. Default: ``1``.

    Attributes
    ----------
    number_of_pieces : int
        Number of pieces each model will be split into.
    output_dir : str
        The path to the folder where all VTK files will be stored.
    fmt : ParaqusConstant
        A constant defining the type of writer, i.e. ``ASCII`` or
        ``BINARY``. This is only for informational purposes.

    """

    __metaclass__ = ABCMeta

    def __init__(self,
                 fmt,
                 output_dir="vtk_files",
                 clear_output_dir=False,
                 number_of_pieces=1):

        if fmt not in (ASCII, BINARY):
            raise ValueError(
                "Writer format not supported: {}.".format(fmt))

        self.number_of_pieces = number_of_pieces
        self.output_dir = os.path.abspath(output_dir)
        self._part_frame_counter = {}
        self._header_type = None
        self._encoding = None
        self._byte_offset = 0
        self._fmt = fmt

        # Delete the output folder if requested
        if clear_output_dir and path.isdir(self.output_dir):

            # Deleting the current work directory does not make sense
            if path.abspath(self.output_dir) == os.getcwd():
                raise RuntimeError(
                    "Deleting the current directory not permitted.")

            # Catch any errors while removing the directory (e.g. open files)
            try:
                shutil.rmtree(self.output_dir)
            except PermissionError:
                raise PermissionError(
                    "Could not remove directory '{}'.".format(self.output_dir))

    @property
    def fmt(self):
        """The type of the writer."""
        return self._fmt

    @property
    def number_of_pieces(self):
        """Number of pieces each model will be split into."""
        return self._number_of_pieces

    @number_of_pieces.setter
    def number_of_pieces(self, number_of_pieces):
        if number_of_pieces < 1:
            raise ValueError("Number of pieces must be positive.")
        self._number_of_pieces = number_of_pieces

    @abstractmethod
    def _write_vtu_file(self, piece, piece_tag=0):
        """
        Write a .vtu file to disk.

        The method will deliver the respective strings and array data to
        the context manager so that a .vtu file is created.

        """
        return

    def _update_byte_offset(self, array):
        """
        Update the byte offset of data arrays. This method is only
        needed for RAW binary file formats.

        Parameters
        ----------
        array : numpy.ndarray[int or float]
            The data array.

        Returns
        -------
        None.

        """
        self._byte_offset += (array.dtype.itemsize*array.size
                              + BINARY_HEADER_SIZE_MAPPER[str(
                                  self._header_type).lower()])

    def _get_special_xml_attributes(self):
        """
        Get special attributes for XML elements.

        Returns
        -------
        dict[str, str or int]
            A dictionary mapping attribute names to attribute values.

        """
        if self._encoding == BASE64:
            return {"format": "binary"}
        if self._encoding == RAW:
            return {"format": "appended", "offset": self._byte_offset}
        return {"format": "ascii"}

    def _create_folder(self, folder):
        """
        Create a new folder in case it does not exist already.

        Parameters
        ----------
        folder : str
            Path to the folder that will be created.

        Returns
        -------
        None.

        """
        abs_path = path.abspath(folder)
        if not path.isdir(abs_path):
            os.makedirs(abs_path)

    def write(self, model):
        """
        Write .vtu and .pvtu files for the model to disk.

        Export a paraqus model to .vtu file format. In case the model
        shall be split into multiple pieces, aditionally, a .pvtu file
        is created. The file names are set automatically in dependence
        on the model parameters.

        Parameters
        ----------
        model : ParaqusModel
            The model that will be exported.

        Returns
        -------
        file_path : str
            If the model is exported as one piece, this is the file path
            of the .vtu file. If there are multiple pieces, it is the
            path to the corresponding .pvtu file.

        """
        # Create pieces and write them to file
        vtu_files = []

        # Generator for submodels
        pieces = model.split_model(self.number_of_pieces)

        # Loop over the submodels
        for piece_tag, piece in enumerate(pieces):

            # Dump to disk
            vtu_file_path = self._write_vtu_file(piece, piece_tag)
            vtu_files.append(vtu_file_path)

        # Reset byte offset
        self._byte_offset = 0

        if self.number_of_pieces == 1:
            return vtu_file_path

        # Connect different pieces in a pvtu file
        pvtu_file_path = self._write_pvtu_file(model, vtu_files)
        return pvtu_file_path

    def _add_field_data_to_pvtu_file(self, model, xml, field_position):
        """
        Add node or element field data to the .pvtu file.

        Parameters
        ----------
        model : ParaqusModel
            The main model the .pvtu file is referring to.
        xml : XmlFactory
            The factory writing the .pvtu file in XML format.
        field_position : ParaqusConstant
            Position of the field values, i.e. ``NODES`` or
            ``ELEMENTS``.

        Returns
        -------
        None.

        """
        if field_position == NODES:
            fields = model.node_fields
            groups = model.nodes.groups
            xml_element_name = "PPointData"
            tags_name = "_node_tags"
        elif field_position == ELEMENTS:
            fields = model.element_fields
            groups = model.elements.groups
            xml_element_name = "PCellData"
            tags_name = "_element_tags"
        else:
            msg = "Invalid field position: {}.".format(field_position)
            raise ValueError(msg)

        xml.add_element(xml_element_name)
        for f in fields:
            name = f.field_name
            values = f.get_3d_field_values()
            components = len(values[0])
            dtype = values.dtype.name
            xml.add_and_finish_element("PDataArray",
                                       type=VTK_TYPE_MAPPER[dtype],
                                       Name=name,
                                       NumberOfComponents=components)

        for group_name in groups:
            dtype = "uint8"
            xml.add_and_finish_element("PDataArray",
                                       type=VTK_TYPE_MAPPER[dtype],
                                       Name="_group " + group_name,
                                       NumberOfComponents=1)

        dtype = model.nodes.tags.dtype.name
        xml.add_and_finish_element("PDataArray",
                                   type=VTK_TYPE_MAPPER[dtype],
                                   Name=tags_name,
                                   NumberOfComponents=1)

        xml.finish_element()

    def _add_points_to_pvtu_file(self, model, xml):
        """
        Add information on node points to the .pvtu file.

        Parameters
        ----------
        model : ParaqusModel
            The main model the .pvtu file is referring to.
        xml : XmlFactory
            The factory writing the .pvtu file in XML format.

        Returns
        -------
        None.

        """
        xml.add_element("PPoints")
        coordinates = model.nodes.coordinates
        dtype = coordinates.dtype.name
        xml.add_and_finish_element("PDataArray",
                                   type=VTK_TYPE_MAPPER[dtype],
                                   NumberOfComponents=3)
        xml.finish_element()

    def _write_pvtu_file(self, model, vtu_files):
        """
        Write the .pvtu and .vtu files for multiple model pieces.

        Combine different submodels or pieces to the main model they
        are referring to by writing a .pvtu file.

        Parameters
        ----------
        model : ParaqusModel
            The main model the different pieces are referring to.
        vtu_files : list[str]
            The paths to all exported .vtu files of the submodels.

        Returns
        -------
        file_path : str
            Path to the generated .pvtu file.

        """
        if len(vtu_files) <= 1:
            raise ValueError("Less than two vtu files available.")

        # Check input
        for f in vtu_files:

            if not path.splitext(f)[1] == ".vtu":
                raise ValueError(
                    "File '{}' is not a .vtu file.".format(f))

            if not path.isfile(path.join(
                    path.dirname(vtu_files[0]), path.basename(f))):
                raise ValueError(
                    "Vtu files not stored in the same folder.")

        # Create file name
        folder_name = path.dirname(vtu_files[0])
        virtual_frame = self._part_frame_counter[(model.model_name,
                                                 model.part_name, 0)]

        pvtu_file_name = model.part_name + \
            "_{}.pvtu".format(virtual_frame - 1)
        file_path = path.join(folder_name, pvtu_file_name)

        # Since no array data will be written into the pvtu file
        # ascii format is completely fine here
        with VtkFileManager(file_path, ASCII) as pvtu_file:

            xml = XmlFactory(pvtu_file)

            # File header
            xml.add_element("VTKFile", type="PUnstructuredGrid",
                            version=VTK_VERSION_STRING, byte_order=BYTE_ORDER)
            xml.add_element("PUnstructuredGrid")

            # Add fields
            self._add_field_data_to_pvtu_file(model, xml, NODES)
            self._add_field_data_to_pvtu_file(model, xml, ELEMENTS)

            # Add nodes
            self._add_points_to_pvtu_file(model, xml)

            # Add pieces
            for piece_file in vtu_files:
                src = path.basename(piece_file)
                xml.add_and_finish_element("Piece", Source=src)
            xml.finish_all_elements()

        return file_path

    def _prepare_to_write_vtu_file(self, piece, piece_tag):
        """
        Prepare a ParaqusModel for the .vtu export.

        Parameters
        ----------
        piece : ParaqusModel
            The model or model piece to prepare for the export.
        piece_tag : int
            The piece identifier tag.

        Returns
        -------
        file_path : str
            The path to the resulting .vtu file.

        """
        # Create a storage folder if there isn't one already
        folder_name = path.join(self.output_dir,
                                piece.model_name,
                                "vtu")
        self._create_folder(folder_name)

        # Generate a virtual frame number, so that frames are
        # consecutive
        key = (piece.model_name, piece.part_name, piece_tag)
        virtual_frame = self._part_frame_counter.get(key, 0)

        # Define a name for the vtu file
        file_path = path.join(folder_name,
                              (piece.part_name
                               + "_{}_{}.vtu".format(piece_tag, virtual_frame))
                              )

        # Update the virtual frame
        self._part_frame_counter.update({key: virtual_frame + 1})

        return file_path

    def _get_piece_mesh_information(self, piece):
        """
        Get the mesh information needed to write a .vtu file.

        Parameters
        ----------
        piece : ParaqusModel
            The model or model piece to prepare for the export.

        Returns
        -------
        nel : int
            Number of elements.
        nnp : int
            Number of node points.
        element_tags : numpy.ndarray[int]
            The original element tags.
        node_tags : numpy.ndarray[int]
            The original node tags.
        node_coords : numpy.ndarray[float]
            Nodal coordinates in shape (number of nodes, 3).
        element_types : numpy.ndarray[int]
            The VTK cell types.
        element_offsets : numpy.ndarray[int]
            The offsets between the elements regarding the node points
            in order of the element types.
        connectivity : list[numpy.ndarray[int]]
            The connectivity list in order of the element types.

        """
        # Extract some relevant arrays for the vtu output
        element_tags = piece.elements.tags
        node_tags = piece.nodes.tags
        node_coords = piece.nodes.coordinates
        tag_based_conn = piece.elements.connectivity
        element_types = piece.elements.types
        element_offsets = np.cumsum([len(c) for c in tag_based_conn],
                                    dtype=tag_based_conn[0].dtype)

        # Make 3d nodal coordinates
        rows, columns = node_coords.shape
        if columns == 2:
            node_coords = np.hstack((node_coords, np.zeros((rows, 1))))
        elif columns == 1:
            node_coords = np.hstack((node_coords, np.zeros((rows, 2))))

        # Create connectivity expressed in terms of the node indices
        node_index_mapper = piece.nodes.index_mapper
        connectivity = []
        for conn in tag_based_conn:
            connectivity.append(np.array([node_index_mapper[i] for i in conn],
                                         dtype=tag_based_conn[0].dtype))

        return (element_tags, node_tags, node_coords, element_types,
                element_offsets, connectivity)

    def _add_array_data_to_vtu_file(self, xml, array):
        """
        Add array data for e.g. fields or mesh information to the .vtu
        file.

        Parameters
        ----------
        xml : XmlFactory
            The factory writing the .vtu file in XML format.
        array : numpy.ndarray[int or float]
            The array data to add.

        Returns
        -------
        None.

        """
        special_attributes = self._get_special_xml_attributes()
        if special_attributes.get("format") == "appended":
            self._update_byte_offset(array)
            return
        xml.add_array_data_to_element(array)

    def _add_time_data_to_vtu_file(self, piece, xml):
        """
        Add time data to the .vtu file.

        Parameters
        ----------
        piece : ParaqusModel
            The piece or submodel to export.
        xml : XmlFactory
            The factory writing the .vtu file in XML format.

        Returns
        -------
        None.

        """
        time_array = np.array([piece.frame_time])
        xml.add_element("FieldData")
        xml.add_element("DataArray",
                        Name="TimeValue",
                        NumberOfTuples=1,
                        type=VTK_TYPE_MAPPER[time_array.dtype.name],
                        **self._get_special_xml_attributes())
        self._add_array_data_to_vtu_file(xml, time_array)
        xml.finish_element()
        xml.finish_element()  # Finish FieldData

    def _add_mesh_data_to_vtu_file(self, piece, xml):
        """
        Add all relevant mesh data to the .vtu file.

        Parameters
        ----------
        piece : ParaqusModel
            The piece or submodel to export.
        xml : XmlFactory
            The factory writing the .vtu file in XML format.

        Returns
        -------
        None.

        """
        (_,
         _,
         node_coords,
         element_types,
         element_offsets,
         connectivity) = self._get_piece_mesh_information(piece)

        # The connectivity is needed as one flattened array that is
        # expressed in terms of the node indices. One big 1d array
        # will be fine for binary output
        if self.fmt == BINARY:
            connectivity = np.array(list(itertools.chain(*connectivity)),
                                    dtype=piece.elements.connectivity[0].dtype)

        # Add nodes
        xml.add_element("Points")
        xml.add_element("DataArray",
                        type=VTK_TYPE_MAPPER[node_coords.dtype.name],
                        Name="nodes", NumberOfComponents=3,
                        **self._get_special_xml_attributes())
        self._add_array_data_to_vtu_file(xml, node_coords)
        xml.finish_element()
        xml.finish_element()  # Finish Points

        # Add connectivity
        xml.add_element("Cells")
        dtype = (connectivity.dtype.name if self.fmt == BINARY
                 else connectivity[0].dtype.name)
        xml.add_element("DataArray",
                        type=VTK_TYPE_MAPPER[dtype],
                        Name="connectivity",
                        **self._get_special_xml_attributes())
        self._add_array_data_to_vtu_file(xml, connectivity)
        xml.finish_element()

        # Add element offsets
        xml.add_element("DataArray",
                        type=VTK_TYPE_MAPPER[element_offsets.dtype.name],
                        Name="offsets",
                        **self._get_special_xml_attributes())
        self._add_array_data_to_vtu_file(xml, element_offsets)
        xml.finish_element()

        # Add element types
        xml.add_element("DataArray",
                        type=VTK_TYPE_MAPPER[element_types.dtype.name],
                        Name="types",
                        **self._get_special_xml_attributes())
        self._add_array_data_to_vtu_file(xml, element_types)
        xml.finish_element()

        xml.finish_element()  # Finish Cells

    def _add_field_data_to_vtu_file(self, piece, xml, field_position):
        """
        Add field data for node or element fields to the .vtu file.

        Parameters
        ----------
        piece : ParaqusModel
            The piece or submodel to export.
        xml : XmlFactory
            The factory writing the .vtu file in XML format.
        field_position : ParaqusConstant
            Position of the field values, i.e. ``NODES`` or
            ``ELEMENTS``.

        Returns
        -------
        None.

        """
        if field_position == NODES:
            fields = piece.node_fields
            groups = piece.nodes.groups
            xml_element_name = "PointData"
            tags_name = "_node_tags"
            tags = piece.nodes.tags
        elif field_position == ELEMENTS:
            fields = piece.element_fields
            groups = piece.elements.groups
            xml_element_name = "CellData"
            tags_name = "_element_tags"
            tags = piece.elements.tags
        else:
            msg = "Invalid field position: {}.".format(field_position)
            raise ValueError(msg)

        # Add fields
        xml.add_element(xml_element_name)
        for f in fields:
            field_vals = f.get_3d_field_values()
            components = len(field_vals[0])
            xml.add_element("DataArray",
                            Name=f.field_name,
                            NumberOfComponents=components,
                            type=VTK_TYPE_MAPPER[field_vals.dtype.name],
                            **self._get_special_xml_attributes())
            self._add_array_data_to_vtu_file(xml, field_vals)
            xml.finish_element()

        # Add fields based on groups
        for group_name, group_tags in groups.items():
            field_vals = np.in1d(tags,
                                 group_tags).astype(np.uint8)
            xml.add_element("DataArray",
                            Name="_group " + group_name,
                            NumberOfComponents=1,
                            type=VTK_TYPE_MAPPER[field_vals.dtype.name],
                            **self._get_special_xml_attributes())
            self._add_array_data_to_vtu_file(xml, field_vals)
            xml.finish_element()

        # Add node or element tags as field
        xml.add_element("DataArray",
                        Name=tags_name,
                        NumberOfComponents=1,
                        type=VTK_TYPE_MAPPER[tags.dtype.name],
                        **self._get_special_xml_attributes())
        self._add_array_data_to_vtu_file(xml, tags)
        xml.finish_element()

        xml.finish_element()  # Finish PointData or CellData


class BinaryWriter(WriterBaseClass):
    """
    Writer for the export of paraqus models to binary .vtu file format.

    Parameters
    ----------
    output_dir : str, optional
        Directory, where all exported VTK files will be stored. Default:
        ``'vtk_files'``.
    clear_output_dir : bool, optional
        If ``True``, the output directory will be cleared before
        exporting any files. Default: ``False``.
    number_of_pieces : int, optional
        Number of pieces each model will be split into. Default: ``1``.
    encoding : ParaqusConstant, optional
        The binary encoding used for data arrays. Currently supported
        are ``RAW`` and ``BASE64``. Default: ``BASE64``.
    header_type : ParaqusConstant, optional
        The data type used for the headers of the binary data blocks.
        Currently supported are ``UINT32`` and ``UINT64``. Default:
        ``UINT64``.

    Attributes
    ----------
    number_of_pieces : int
        Number of pieces each model will be split into.
    output_dir : str
        The path to the folder where all VTK files will be stored.
    encoding : ParaqusConstant
        The binary encoding used for data arrays.
    header_type : ParaqusConstant
        The data type used for the headers of the binary data blocks.
    FORMAT : ParaqusConstant
        This is a constant with value BINARY and is only used for
        informational purposes.

    Example
    -------
    >>> from paraqus import BinaryWriter
    >>> from paraqus.constants import RAW
    >>> writer = BinaryWriter(number_of_pieces=2, encoding=RAW)
    >>> writer.write(random_paraqus_model)

    """

    # References:
    # https://mathema.tician.de/what-they-dont-tell-you-about-vtk-xml-binary-formats/
    # https://public.kitware.com/pipermail/paraview/2005-April/001391.html
    # https://github.com/paulo-herrera/PyEVTK
    # https://docs.python.org/2.7/library/struct.html

    def __init__(self,
                 output_dir="vtk_files",
                 clear_output_dir=False,
                 number_of_pieces=1,
                 encoding=BASE64,
                 header_type=UINT64):

        super(BinaryWriter, self).__init__(BINARY,
                                           output_dir,
                                           clear_output_dir,
                                           number_of_pieces)
        self.header_type = header_type
        self.encoding = encoding

    @property
    def header_type(self):
        """The data type used for the headers of binary data blocks."""
        return self._header_type

    @header_type.setter
    def header_type(self, header_type):
        self._header_type = str(header_type).lower()

    @property
    def encoding(self):
        """The binary encoding used for data arrays."""
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        if encoding not in (BASE64, RAW):
            raise ValueError("Invalid binary encoding.")
        self._encoding = encoding

    def _append_raw_mesh_data(self, piece, xml):
        """
        Append the data for the mesh to the .vtu file.

        Parameters
        ----------
        piece : ParaqusModel
            The piece or submodel to export.
        xml : XmlFactory
            The factory writing the .vtu file in XML format.

        Returns
        -------
        None.

        """
        (_, _, node_coords, element_types, element_offsets,
         connectivity) = self._get_piece_mesh_information(piece)

        # The connectivity is needed as one flattened array that is
        # expressed in terms of the node indices. One big 1d array
        # will be fine for binary output
        connectivity = np.array(list(itertools.chain(*connectivity)),
                                dtype=piece.elements.connectivity[0].dtype)

        for array in [node_coords, connectivity, element_offsets,
                      element_types]:
            xml.add_array_data_to_element(array, break_line=False)

    def _append_raw_field_data(self, piece, xml, field_position):
        """
        Append the data for node and element fields to the .vtu file.

        Parameters
        ----------
        piece : ParaqusModel
            The piece or submodel to export.
        xml : XmlFactory
            The factory writing the .vtu file in XML format.
        field_position : ParaqusConstant
            Position of the field values, i.e. `NODES` or `ELEMENTS`.

        Returns
        -------
        None.

        """
        if field_position == NODES:
            fields = piece.node_fields
            groups = piece.nodes.groups
            tags = piece.nodes.tags
        elif field_position == ELEMENTS:
            fields = piece.element_fields
            groups = piece.elements.groups
            tags = piece.elements.tags
        else:
            msg = "Invalid field position: {}.".format(field_position)
            raise ValueError(msg)

        # Append field data
        for f in fields:
            field_vals = f.get_3d_field_values()
            xml.add_array_data_to_element(field_vals, break_line=False)

        # Append group data
        for _, group_tags in groups.items():
            field_vals = np.in1d(tags, group_tags).astype(np.uint8)
            xml.add_array_data_to_element(field_vals, break_line=False)

        # Append tags field
        xml.add_array_data_to_element(tags, break_line=False)

    def _append_raw_model_data(self, piece, xml):
        """
        Append all data to the .vtu file (time, mesh and field data).

        Parameters
        ----------
        piece : ParaqusModel
            The piece or submodel to export.
        xml : XmlFactory
            The factory writing the .vtu file in XML format.

        Returns
        -------
        None.

        """
        xml.add_element("AppendedData", encoding="raw")
        xml.add_content_to_element("_", False)
        time_array = time_array = np.array([piece.frame_time])
        xml.add_array_data_to_element(time_array, break_line=False)
        self._append_raw_mesh_data(piece, xml)
        self._append_raw_field_data(piece, xml, NODES)
        self._append_raw_field_data(piece, xml, ELEMENTS)
        xml.finish_element()  # Finish AppendedData

    def _write_vtu_file(self, piece, piece_tag=0):
        """
        Write a .vtu file for a piece or submodel of a paraqus model.

        Parameters
        ----------
        piece : ParaqusModel
            The piece or submodel to export.
        piece_tag : int, optional
            The identifier of the currently processed piece. Default:
            ``0``.

        Returns
        -------
        file_path : str
            The path to the exported .vtu file.

        """
        file_path = self._prepare_to_write_vtu_file(piece, piece_tag)

        # Write the file
        with VtkFileManager(file_path, BINARY) as vtu_file:
            xml = XmlFactory(vtu_file, self.encoding, self.header_type)

            # Initialize file
            xml.add_element("VTKFile", type="UnstructuredGrid",
                            version=VTK_VERSION_STRING,
                            byte_order=BYTE_ORDER,
                            header_type=VTK_TYPE_MAPPER[self.header_type])
            xml.add_element("UnstructuredGrid")

            # Add time data
            self._add_time_data_to_vtu_file(piece, xml)

            # Initialize model geometry
            nnp, nel = len(piece.nodes.tags), len(piece.elements.tags)
            xml.add_element("Piece", NumberOfPoints=nnp,
                            NumberOfCells=nel)

            # Add nodes and elements
            self._add_mesh_data_to_vtu_file(piece, xml)

            # Add node and element fields
            self._add_field_data_to_vtu_file(piece, xml, NODES)
            self._add_field_data_to_vtu_file(piece, xml, ELEMENTS)

            xml.finish_element()  # Finish Piece
            xml.finish_element()  # Finish UnstructuredGrid

            # Append data in case of raw encoding
            if self.encoding == RAW:
                self._append_raw_model_data(piece, xml)

            xml.finish_element()  # Finish VTKFile

        return file_path


class AsciiWriter(WriterBaseClass):
    """
    Writer for the export of paraqus models to ASCII .vtu file format.

    Parameters
    ----------
    output_dir : str, optional
        Directory, where all exported VTK files will be stored. Default:
        ``'vtk_files'``.
    clear_output_dir : bool, optional
        If ``True``, the output directory will be cleared before
        exporting any files. Default: ``False``.
    number_of_pieces : int, optional
        Number of pieces each model will be split into. The default
        is ``1``.

    Attributes
    ----------
    number_of_pieces : int
        Number of pieces each model will be split into.
    output_dir : str
        The path to the folder where all VTK files will be stored.
    FORMAT : ParaqusConstant
        This is a constant with value ``ASCII`` and is only used for
        informational purposes.

    Example
    -------
    >>> from paraqus import AsciiWriter
    >>> writer = AsciiWriter(number_of_pieces=2)
    >>> writer.write(random_paraqus_model)

    """

    def __init__(self,
                 output_dir="vtk_files",
                 clear_output_dir=False,
                 number_of_pieces=1):

        super(AsciiWriter, self).__init__(ASCII,
                                          output_dir,
                                          clear_output_dir,
                                          number_of_pieces)

    def _write_vtu_file(self, piece, piece_tag=0):
        """
        Write a .vtu file for a piece or submodel of a paraqus model.

        Parameters
        ----------
        piece : ParaqusModel
            The piece or submodel to export.
        piece_tag : int, optional
            The identifier of the currently processed piece. Default:
            ``0``.

        Returns
        -------
        file_path : str
            The path to the exported .vtu file.

        """
        file_path = self._prepare_to_write_vtu_file(piece, piece_tag)
        with VtkFileManager(file_path, ASCII) as vtu_file:
            xml = XmlFactory(vtu_file)

            # Initialize file
            xml.add_element("VTKFile", type="UnstructuredGrid",
                            version=VTK_VERSION_STRING, byte_order=BYTE_ORDER)
            xml.add_element("UnstructuredGrid")

            # Add time data
            self._add_time_data_to_vtu_file(piece, xml)

            # Initialize model geometry
            nnp, nel = len(piece.nodes.tags), len(piece.elements.tags)
            xml.add_element("Piece", NumberOfPoints=nnp,
                            NumberOfCells=nel)

            # Add nodes and elements
            self._add_mesh_data_to_vtu_file(piece, xml)

            # Add node and element fields
            self._add_field_data_to_vtu_file(piece, xml, NODES)
            self._add_field_data_to_vtu_file(piece, xml, ELEMENTS)

            xml.finish_element()  # Finish Piece
            xml.finish_element()  # Finish UnstructuredGrid
            xml.finish_element()  # Finish VTKFile

        return file_path


class CollectionWriter(object):
    """
    Writer for the export of a collection of .pvtu or .vtu files.

    This writer can be used as a context manager to generate a .pvd
    file.

    Parameters
    ----------
    writer : BinaryWriter or AsciiWriter
        The writer that is used to generate .pvtu and .vtu files.
    collection_name : str
        The name of the collection. This is used for the name of the
        .pvd file.

    Attributes
    ----------
    writer : BinaryWriter or AsciiWriter
        The writer that is used the generate .pvtu and .vtu files.
    collection_name : str
        The name of the collection.

    Example
    -------
    >>> from paraqus import BinaryWriter, CollectionWriter
    >>> vtu_writer = BinaryWriter()
    >>> with CollectionWriter(vtu_writer, "my_collection") as writer:
    >>>     writer.write(random_paraqus_model_frame_1)
    >>>     writer.write(random_paraqus_model_frame_2)
    >>>     writer.write(random_paraqus_model_frame_3)

    """

    def __init__(self, writer, collection_name):
        self.writer = writer
        self.collection_name = collection_name
        self._collection_items = None

    def __enter__(self):
        self._initialize_collection()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._finalize_collection()

    def write(self, model):
        """
        Write a ParaqusModel to a VTK file using the underlying writer.

        Parameters
        ----------
        model : ParaqusModel
            The model that will be converted to a VTK file.

        Returns
        -------
        None.

        """
        old_model_name = model.model_name
        model.model_name = self.collection_name

        vtu_file_path = self.writer.write(model)
        self._add_to_collection(model, vtu_file_path)

        model.model_name = old_model_name

    def _initialize_collection(self):
        """
        Initialize a new collection of ParaqusModels.

        A .pvd file that combines multiple .vtu or .pvtu files is
        generated from the collection when ``finalize_collection()``
        is called.

        Returns
        -------
        None.

        """
        self._collection_items = {}

    def _finalize_collection(self):
        """
        Export the .pvd file for the current collection and clear it.

        Returns
        -------
        None.

        """
        if len(self._collection_items) == 0:
            return

        self._write_pvd_file()
        self._collection_items = None

    def _add_to_collection(self, model, file_path):
        """
        Add a model to the current collection.

        Models do not need to be added in the correct order since the
        frame time is stored as a model attribute.

        Parameters
        ----------
        model : ParaqusModel
            The model that will be added to the collection.
        file_path : str
            The path to the .vtu or .pvtu file of the model to add.

        Returns
        -------
        None.

        """
        abspath = path.abspath(file_path)

        if self._collection_items is None:
            raise RuntimeError("Collection has not been initialized.")

        # Some input checking
        if path.splitext(file_path)[1] not in [".vtu", ".pvtu"]:
            raise ValueError(
                "File is neither a .vtu file nor a .pvtu file.")
        if not path.isfile(abspath):
            raise ValueError(
                "File '{}' does not exist.".format(abspath))

        # For each part, repo is a list of (time, file_path) tuples
        repo = self._collection_items.get(model.part_name)
        if repo is None:
            repo = self._collection_items[model.part_name] = []
        repo.append((model.frame_time, abspath))

    def _write_pvd_file(self):
        """
        Export a collection of multiple .vtu or .pvtu files.

        Returns
        -------
        None.

        """
        # Pvd files will be written into basedir/modelname/
        pvd_file_path = path.join(self.writer.output_dir,
                                  self.collection_name,
                                  self.collection_name + ".pvd")
        pvd_file_path = path.abspath(pvd_file_path)

        # Since no array data will be written into the pvd file ascii
        # format is completely fine here
        with VtkFileManager(pvd_file_path, ASCII) as pvd_file:

            xml = XmlFactory(pvd_file)

            xml.add_element("VTKFile", type="Collection",
                            version=VTK_VERSION_STRING, byte_order=BYTE_ORDER)
            xml.add_element("Collection")

            for i, part_name in enumerate(self._collection_items.keys()):

                for frame_time, file in self._collection_items[part_name]:

                    rel_path = path.relpath(
                        file, path.dirname(pvd_file_path))
                    xml.add_and_finish_element("DataSet", timestep=frame_time,
                                               part=i, file=rel_path)

            xml.finish_all_elements()


class XmlFactory(object):
    """
    Factory to produce properly formatted XML files.

    Parameters
    ----------
    stream : VtkFileManager
        The output stream of the file that is written.
    encoding : ParaqusConstant, optional
        The binary encoding used for data arrays. Currently supported
        are ``RAW`` and ``BASE64``. This is not needed in case of
        writing VTK ASCII files. Default: ``None``.
    header_type : ParaqusConstant, optional
        The data type used for the headers of the binary data blocks.
        Currently supported are ``UINT32`` and ``UINT64``. This is not
        needed in case of writing VTK ASCII files. Default: ``None``.

    """

    def __init__(self, stream, encoding=None, header_type=None):

        assert isinstance(stream, VtkFileManager), \
            "Stream is not a VtkFileManager object."

        if stream.fmt == BINARY:
            assert encoding is not None, "Binary ending is None."
            assert header_type is not None, "Binary data header is None."

        self._stream = stream
        self._lvl = 0
        self._add_tabs = True
        self._elements = []
        self._active_element = None
        self._header_type = header_type
        self._encoding = encoding

    def add_element(self, name, break_line=True, **attributes):
        """
        Add a new element section to the XML file.

        Parameters
        ----------
        name : str
            Name of the element section.
        break_line : bool, optional
            If ``True``, a linebreak will be inserted after the element
            section has been added. Default: ``True``.
        **attributes : str or int or float
            Attributes of the element section. The key will be the
            name of the attribute, the value will be the value of the
            attribute.

        Returns
        -------
        None.

        """
        to_write = '<{}'.format(name)

        # We need to guarantee a certain order here for testing
        keys = sorted(list(attributes.keys()))
        for key in keys:
            val = attributes[key]
            to_write += ' {}="{}"'.format(key, val)
        to_write += '>'

        if break_line:
            to_write += '\n'

        if self._add_tabs:
            to_write = self._lvl * '    ' + to_write
        self._stream.write(to_write)

        self._elements.append(name)
        self._active_element = name
        self._lvl += 1 if break_line else 0
        self._add_tabs = break_line

    def finish_element(self, break_line=True):
        """
        Close the active element section in the XML file.

        In case there is no active element section, nothing happens.

        Parameters
        ----------
        break_line : bool, optional
            If ``True``, a linebreak will be inserted after the element
            section has been closed. Default: ``True``.

        Returns
        -------
        None.

        """
        if self._active_element is None:
            return

        to_write = '</{}>'.format(self._elements.pop())

        if break_line:
            to_write += '\n'

        if self._add_tabs:
            to_write = (self._lvl - 1) * '    ' + to_write
        self._stream.write(to_write)

        self._lvl -= 1 if break_line else 0
        self._add_tabs = break_line

        if len(self._elements) > 0:
            self._active_element = self._elements[-1]
        else:
            self._active_element = None

    def finish_all_elements(self, break_line=True):
        """
        Close and finish all open element sections.

        Parameters
        ----------
        break_line : bool, optional
            If ``True``, a linebreak will be inserted after each closed
            element section. Default: ``True``.

        Returns
        -------
        None.

        """
        while len(self._elements) > 0:
            self.finish_element(break_line=break_line)

    def add_and_finish_element(self, name, break_line=True, **attributes):
        """
        Add an element section and close it immediately.

        Parameters
        ----------
        name : str
            Name of the element section.
        break_line : bool, optional
            If ``True``, a linebreak will be inserted after each element
            section. Default: ``True``.
        **attributes : str or int or float
            Attributes of the element section. The key will be the
            name of the attribute, the value will be the value of the
            attribute.

        Returns
        -------
        None.

        """
        to_write = '<{}'.format(name)

        # We need to guarantee a defined order here for testing
        keys = sorted(list(attributes.keys()))
        for key in keys:
            val = attributes[key]
            to_write += ' {}="{}"'.format(key, val)
        to_write += '/>'

        if break_line:
            to_write += '\n'

        if self._add_tabs:
            to_write = self._lvl * '    ' + to_write
        self._stream.write(to_write)

    def add_content_to_element(self, content, break_line=True):
        """
        Add any content that is not a array-shaped to the XML file.

        Parameters
        ----------
        content : str or int or float
            The content to add.
        break_line : bool, optional
            If ``True``, a linebreak will be inserted after the content
            has been written. Default: ``True``.

        Returns
        -------
        None.

        """
        if self._active_element is None:
            raise RuntimeError("No XML element is open.")

        if break_line:
            content += '\n'

        if self._add_tabs:
            content = self._lvl * '    ' + content
        self._stream.write(content)

    def add_array_data_to_element(self, array, break_line=True):
        """
        Add array data to the XML file.

        Parameters
        ----------
        array : ArrayLike[int or float]
            The array data to add.
        break_line : bool, optional
            If ``True``, a linebreak will be inserted after the array
            data. Default: ``True``.

        Returns
        -------
        None.

        """
        if self._active_element is None:
            raise RuntimeError("No XML element is open.")

        if self._stream.fmt == BINARY:
            self._write_binary_array_data(array, break_line)

        elif self._stream.fmt == ASCII:
            self._write_ascii_array_data(array, break_line)

    def _write_binary_array_data(self, array, break_line=True):
        """
        Add binary encoded array data to the XML file.

        Parameters
        ----------
        array : ArrayLike[int or float]
            The array to add to the output file.
        break_line : bool, optional
            If ``True``, a linebreak will be inserted after the array
            data has been written. Default: ``True``.

        Returns
        -------
        None.

        """
        # Somehow references are writing about vtk expecting fortran
        # array order in binary format, but in my tests this did not
        # work and c-type arrays yield the expected results. Maybe this
        # has been updated over time since the references are quite old.
        # binary_data = struct.pack(format_string, *np.ravel(array,
        #                                                    order="F"))

        # Create a 32 or 64 bit length indicator of type unsigned int
        # for the header and create the header
        length_indicator = (BYTE_ORDER_CHAR
                            + BINARY_TYPE_MAPPER[self._header_type])
        block_size = array.dtype.itemsize*array.size
        header = struct.pack(length_indicator, block_size)

        # Creat a format string pack the array data
        format_string = (BYTE_ORDER_CHAR
                         + array.size
                         + BINARY_TYPE_MAPPER[array.dtype.name])
        data = struct.pack(format_string, *array.flatten())

        if self._encoding == BASE64:
            # Convert to base64
            b64_header = base64.b64encode(header)
            b64_data = base64.b64encode(data)

            if self._add_tabs:
                self._stream.write(self._lvl * '    ')
            self._stream.write(b64_header)
            self._stream.write(b64_data)

        elif self._encoding == RAW:
            self._stream.write(header)
            self._stream.write(data)

        if break_line:
            self._stream.write("\n")

        self._add_tabs = break_line

    def _write_ascii_array_data(self, array, break_line=True):
        """
        Add array data in ASCII format to the XML file.

        Parameters
        ----------
        array : ArrayLike[int or float]
            The array to add to the output file.
        line_break : bool, optional
            If ``True``, a line break will be inserted after each line
            of the array. Default: ``True``.

        Returns
        -------
        None.

        """
        # Check if the array is 1d
        # AttributeError must be catched in case of a list as input,
        # e.g. in case of the connectivity
        try:
            if 1 in array.shape or len(array.shape) == 1:
                array = array.reshape(1, -1)
        except AttributeError:
            pass

        for i, line in enumerate(array):

            try:
                data_string = ''.join(
                    str(val) + '    ' for val in line)[0:-4]
            except TypeError:  # In case of only one value per line
                data_string = str(line)

            if break_line:
                data_string += '\n'
            if not break_line and i == len(array):
                data_string += '    '

            if self._add_tabs:
                data_string = self._lvl * '    ' + data_string
            self._stream.write(data_string)

            self._add_tabs = break_line
