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
This module containts all classes that contribute to Paraqus models,
i.e. not just the model class itself but also repositories for nodes,
elements and fields.

"""
import itertools
import warnings
from abc import ABCMeta, abstractmethod

import numpy as np

from paraqus import constants
from paraqus.constants import USER, NODES, ELEMENTS, SCALAR, VECTOR, TENSOR


class ParaqusModel(object):
    """
    Paraqus representation of a finite element model.

    The Paraqus model can be used to manipulate and export any finite
    element model as a set of VTK files.

    Parameters
    ----------
    element_tags : Sequence[int]
        Tags of all elements being part of the model. Tags have to be
        unique.
    connectivity : Sequence[Sequence[int]]
        Connectivity list in the order defined for the element tags. The
        respective nodes have to be in order as defined for VTK cells.
    element_types : Sequence[int]
        The VTK cell types for all elements in the order defined for the
        element tags.
    node_tags : Sequence[int]
        Tags of all nodes being part of the model. Tags have to be
        unique.
    node_coords : Sequence[Sequence[float]]
        Nodal coordinates in the order defined for the node tags. The
        coordinates can be defined in 1d-, 2d- or 3d-space as an array
        of shape (number of nodes, number of dimensions).
    model_name : str, optional
        Name of the main model. In case of multiple frames or parts
        every Paraqus model should have the same model name. Default:
        ``'MODEL NAME'``.
    part_name : str, optional
        Name of the part instance. Default: ``'PART NAME'``.
    step_name : str, optional
        Name of the load step. Default: ``'STEP NAME'``.
    frame_time : float, optional
        Current frame time. Default: ``0.0``.
    source : ParaqusConstant, optional
        This is just for informational purpose and defines the source
        of the model, e.g. ``ABAQUS``. Default: ``USER``.

    Attributes
    ----------
    model_name : str
        Name of the main model.
    part_name : str
        Name of the part instance.
    step_name : str
        Name of the load step.
    frame_time : float
        Current frame time of the model frame.
    source : ParaqusConstant
        This is a constant for informational purpose and describes the
        source of the model, e.g. ``ABAQUS`` or ``USER``.
    elements : ElementRepository
        A repository storing all information on elements, e.g. tags and
        element types.
    nodes : NodeRepository
        Repository storing all information on nodes, e.g. tags and
        coordinates.
    node_fields : NodeFieldRepository
        Repository storing all node fields.
    element_fields : ElementFieldRepository
        Repository sotring all element fields.

    Example
    -------
    >>> import numpy as np
    >>> from paraqus import ParaqusModel, BinaryWriter
    >>>
    >>> # Define the model parameters
    >>> element_tags = np.array([1,2])
    >>> connectivity = [np.array([1,2,3,4]),np.array([4,3,5])]
    >>> element_types = np.array([9,5])
    >>> node_tags = np.array([1,2,3,4,5])
    >>> node_coords = np.array([[0,0],[1,0],[1,1],[0,1],[0.5,1.5]])
    >>>
    >>> # Create a new model
    >>> model = ParaqusModel(element_tags,
    >>>                      connectivity,
    >>>                      element_types,
    >>>                      node_tags,
    >>>                      node_coords,
    >>>                      model_name="foo",
    >>>                      part_name="bar",
    >>>                      step_name="foobar",
    >>>                      frame_time=0.1)
    >>>
    >>> # Export model as VTK
    >>> writer = BinaryWriter()
    >>> writer.write(model)

    """

    def __init__(self,
                 element_tags,
                 connectivity,
                 element_types,
                 node_tags,
                 node_coords,
                 **kwargs):

        # Check keyword arguments
        self._model_name = kwargs.pop("model_name", "MODEL NAME")
        self._part_name = kwargs.pop("part_name", "PART NAME")
        self._step_name = kwargs.pop("step_name", "STEP NAME")
        self._frame_time = kwargs.pop("frame_time", 0.0)
        self._source = kwargs.pop("source", USER)

        # Check for unrecognized kwargs
        if len(kwargs) > 0:
            err_msg = "Unrecognized kwarg: '{}'.".format(
                str(kwargs.keys()[0]))
            raise ValueError(err_msg)

        # Create model geometry
        self._elements = ElementRepository(element_tags, connectivity,
                                           element_types)
        self._nodes = NodeRepository(node_tags, node_coords)

        # Add field repositories
        self._node_fields = NodeFieldRepository()
        self._element_fields = ElementFieldRepository()

    @property
    def model_name(self):
        """The name of the main model."""
        return self._model_name

    @model_name.setter
    def model_name(self, model_name):
        self._model_name = model_name

    @property
    def part_name(self):
        """The name of the part instance."""
        return self._part_name

    @part_name.setter
    def part_name(self, part_name):
        self._part_name = part_name

    @property
    def step_name(self):
        """The name of the load step."""
        return self._step_name

    @step_name.setter
    def step_name(self, step_name):
        self._step_name = step_name

    @property
    def frame_time(self):
        """Current frame time of the model frame."""
        return self._frame_time

    @property
    def source(self):
        """Source of the model, e.g. ``ABAQUS`` or ``USER``."""
        return self._source

    @property
    def elements(self):
        """The ElementRepository of the model."""
        return self._elements

    @property
    def nodes(self):
        """The NodeRepository of the model."""
        return self._nodes

    @property
    def node_fields(self):
        """The repository storing the node fields."""
        return self._node_fields

    @property
    def element_fields(self):
        """The repository storing the element field."""
        return self._element_fields

    def __str__(self):
        """String representation of the model."""
        description = ("ParaqusModel\n"
                       + "  model_name: '" + self.model_name + "'\n"
                       + "  part_name:  '" + self.part_name + "'\n"
                       + "  step_name:  '" + self.step_name + "'\n")

        return description

    def add_field(self, field_name, field_tags, field_values,
                  field_position, field_type):
        """
        Add a field to the model.

        The field will also be part of any exported VTK model.

        Parameters
        ----------
        field_name : str
            Name of the field.
        field_tags : Sequence[int]
            Tags of the nodes or elements at which the field is stored.
        field_values : Sequence[Sequence[float]]
            Values of the field in the order defined for the field tags.
            At nodes or elements that are not part of the field tags,
            the values will be set to ``NaN`` automatically.
        field_position : ParaqusConstant
            A constant defining the storage position of the field, i.e.
            ``NODES`` or ``ELEMENTS``.
        field_type : ParaqusConstant
            A constant defining the field type, i.e. ``SCALAR``,
            ``VECTOR`` or ``TENSOR``.

        Returns
        -------
        None.

        """
        field_values = np.asarray(field_values, dtype=float)

        # Add a node field
        if field_position == NODES:

            if len(self.nodes.tags) < len(field_tags):
                msg = ("Values array '{}'".format(field_name)
                       + " has more entries than the amount of the model"
                       + " nodes.")
                raise ValueError(msg)

            # Always call pad method so that values will be sorted
            # regarding the order of node tags
            field_values = self._pad_field_values(field_tags, field_values,
                                                  self.nodes.tags)

            field = Field(field_name, field_values,
                          field_position, field_type)
            self.node_fields.add_field(field)

        # Add an element field
        elif field_position == ELEMENTS:

            if len(self.elements.tags) < len(field_tags):
                msg = ("Values array '{}'".format(field_name)
                       + " has more entries than the amount of model"
                       + " elements.")
                raise ValueError(msg)

            # Always call pad method so that values will be sorted
            # regarding the order of element tags
            field_values = self._pad_field_values(field_tags, field_values,
                                                  self.elements.tags)

            field = Field(field_name, field_values,
                          field_position, field_type)
            self.element_fields.add_field(field)

        else:
            msg = "Invalid field position: {}.".format(field_position)
            raise ValueError(msg)

    def add_node_group(self, group_name, node_tags):
        """
        Add a node group to the model.

        The nodes must have been added beforehand, this method just
        stores the information that they form a named group.

        Parameters
        ----------
        group_name : str
            Name of the group. Must be unique.
        node_tags : Sequence[int]
            Integer tags of the nodes in the group.

        Returns
        -------
        None.

        """
        self.nodes.add_group(group_name, node_tags)

    def add_element_group(self, group_name, element_tags):
        """
        Add an element group to the model.

        The elements must have been added beforehand, this method just
        stores the information that the elements form a named group.

        Parameters
        ----------
        group_name : str
            Name of the group. Must be unique.
        element_tags : Sequence[int]
            Integer tags of the elements in the group.

        Returns
        -------
        None.

        """
        self.elements.add_group(group_name, element_tags)

    def split_model(self, number_of_pieces):
        """
        Split the model into ``number_of_pieces`` different parts.

        The split is performed based on element numbers, so that the
        resulting model pieces are not necessarily continuous (i.e. they
        might have holes etc.).

        Parameters
        ----------
        number_of_pieces : int
            Number of parts the model will be split into.

        Yields
        ------
        piece : ParaqusModel
            The resulting submodel for one piece including all fields
            and groups.

        """
        # Split list of element tags regarding the number of pieces
        element_tags_per_piece = np.array_split(self.elements.tags,
                                                number_of_pieces)

        for piece_element_tags in element_tags_per_piece:
            # Create the piece
            if number_of_pieces > 1:
                piece = self._extract_submodel_by_elements(
                    piece_element_tags)
            else:
                piece = self

            yield piece

    def _extract_submodel_by_elements(self, element_tags):
        """
        Extract a submodel based on element tags.

        Parameters
        ----------
        element_tags : Sequence[int]
            List of tags of the elements that will be part of the
            submodel.

        Returns
        -------
        submodel : ParaqusModel
            The resulting submodel including all fields and groups.

        """
        # Get nodes and elements of the current piece
        sub_element_repo = self.elements.get_subset(*element_tags)
        node_tags = sub_element_repo.get_node_tags()
        sub_node_repo = self.nodes.get_subset(*node_tags)

        # Create a new paraqus model representing the submodel
        submodel = ParaqusModel(sub_element_repo.tags,
                                sub_element_repo.connectivity,
                                sub_element_repo.types,
                                sub_node_repo.tags,
                                sub_node_repo.coordinates,
                                model_name=self.model_name,
                                part_name=self.part_name,
                                step_name=self.step_name,
                                frame_time=self.frame_time,
                                source=self.source)

        # Add field to the submodel
        for nf in self.node_fields.get_subset(sub_node_repo):
            submodel.node_fields.add_field(nf)

        for ef in self.element_fields.get_subset(sub_element_repo):
            submodel.element_fields.add_field(ef)

        # Add groups to the submodel
        for group_name, group_elements in sub_element_repo.groups.items():
            submodel.add_element_group(group_name, group_elements)

        for group_name, group_nodes in sub_node_repo.groups.items():
            submodel.add_node_group(group_name, group_nodes)

        return submodel

    def get_fields_by_type(self, field_type, field_position):
        """
        Return all fields of a specific type, e.g. of type ``SCALAR``.

        Fields stored at nodes as well as fields stored at elements can
        be returned.

        Parameters
        ----------
        field_type : ParaqusConstant
            Type of the field, i.e. ``TENSOR``, ``VECTOR`` or
            ``SCALAR``.
        field_position : ParaqusConstant
            Position of the field, i.e. ``NODES`` or ``ELEMENTS``.

        Returns
        -------
        list[Field]
            All fields that match the requested type and position.

        """
        if field_position == NODES:
            return self.node_fields.get_fields_by_type(field_type)

        if field_position == ELEMENTS:
            return self.element_fields.get_fields_by_type(field_type)

        msg = "Invalid field position: {}".format(field_position)
        raise ValueError(msg)

    def get_node_field(self, field_name):
        """
        Request a node field of a given name.

        If there is no field found, None will be returned.

        Parameters
        ----------
        field_name : str
            Name of the requested node field.

        Returns
        -------
        Field
            The requested field.

        """
        return self.node_fields[field_name]

    def get_element_field(self, field_name):
        """
        Request an element field of a given name.

        If there is no field found, None will be returned.

        Parameters
        ----------
        field_name : str
            Name of the requested element field.

        Returns
        -------
        Field
            The requested field.

        """
        return self.element_fields[field_name]

    def _pad_field_values(self, field_tags, field_values, pad_tags):
        """Extend a field value array with nan values for unset tags."""
        field_values = field_values.reshape(len(field_values), -1)

        # Make sure the padded tags contain all of the field tags
        if not all(np.in1d(field_tags, pad_tags)):
            raise ValueError(
                "Cannot pad values: not all tags are found.")

        # Indices of the field_tags in pad_tags
        sorter = np.argsort(pad_tags)
        indices_sorted = sorter[np.searchsorted(pad_tags, field_tags)]
        indices_original = sorter[indices_sorted]

        # New array pre-filled with nans
        shape = (len(pad_tags), field_values.shape[1])

        new_field_values = np.empty(shape, dtype=field_values.dtype)
        new_field_values[:, :] = np.nan

        # Fill in the old values
        new_field_values[indices_original, :] = field_values

        return new_field_values


class MeshRepositoryBaseClass(object):
    """
    Base class for mesh repositories such as nodes or elements.

    Parameters
    ----------
    tags : Sequence[int]
        Tags of all nodes or elements that will be stored in the
        repository.

    Attributes
    ----------
    tags : numpy.ndarray[int]
        Tags of the nodes or elements.
    groups : dict[str, numpy.ndarray[int]]
        Mapping group name -> tags.

    """

    __metaclass__ = ABCMeta

    def __init__(self, tags):
        self._tags = np.asarray(tags, dtype=int).reshape(-1)
        self._groups = {}

    @property
    def tags(self):
        """The node or element tags."""
        return self._tags

    @property
    def groups(self):
        """The node or element groups."""
        return self._groups

    def __iter__(self):
        """Repository iterator."""
        for i in range(len(self)):
            yield self.tags[i]

    def __len__(self):
        """Repository size."""
        return len(self.tags)

    def add_group(self, group_name, tags):
        """
        Add a node or element group to the repository.

        The nodes or elements must have been added beforehand, this
        method just stores the information that the nodes or elements
        form a named group.

        Parameters
        ----------
        group_name : str
            Name of the group. Must be unique.
        tags : Sequence[int]
            Integer tags of the nodes or elements in the group.

        Returns
        -------
        None.

        """
        assert group_name not in self.groups, \
            "Group '{}' already exists.".format(group_name)

        assert set(tags) <= set(self.tags), \
            "Some element tags in the set are not in the model."

        tags = np.asarray(tags, dtype=int)
        tags.sort()
        self._groups[group_name] = tags


class ElementRepository(MeshRepositoryBaseClass):
    """
    Repository to store a set of elements.

    Parameters
    ----------
    element_tags : Sequence[int]
        Tags of all elements that will be stored in the repository.
    connectivity : Sequence[Sequence[int]]
        Connectivity of all elements in the order defined for the
        element tags.
    element_types : Sequence[int]
        Type of all elements in the order defined for the element tags.

    Attributes
    ----------
    tags : numpy.ndarray[int]
        Tags of all elements stored in the repository.
    connectivity : list[numpy.ndarray[int]]
        Connectivity list of all elements in the same order as the tags.
    types : numpy.ndarray[int]
        Types of all elements in the same order as the tags.
    index_mapper : dict[int, int]
        Mapping element tag -> index in list of tags.
    groups : dict[str, numpy.ndarray[int]]
        Mapping group name -> element tags.

    """

    def __init__(self,
                 element_tags,
                 connectivity,
                 element_types):

        assert len(element_tags) == len(connectivity) == len(element_types), \
            ("The amounts of element tags, element types and connectivity"
             + "entries do not match.")

        # The connectivity cannot be stored as one array in case of
        # elements with different numbers of element nodes
        super(ElementRepository, self).__init__(element_tags)
        self.index_mapper = dict(
            zip(element_tags, range(len(element_tags))))
        self._connectivity = [np.asarray(c, dtype=int).reshape(-1)
                              for c in connectivity]
        self._types = np.asarray(
            element_types, dtype=np.uint8).reshape(-1)

    @property
    def connectivity(self):
        """The connectivity list."""
        return self._connectivity

    @property
    def types(self):
        """The element types."""
        return self._types

    def __getitem__(self, key):
        """Index-based access."""
        if key > len(self) - 1:
            raise IndexError("Index out of bounds: {}.".format(key))

        return (self.tags[key], self.connectivity[key],
                self.types[key], self.index_mapper[self.tags[key]])

    def get_subset(self, *element_tags):
        """
        Create a new ElementRepositroy for a subset of elements by tags.

        Parameters
        ----------
        *element_tags : Sequence[int]
            Elements that will be contained in the new repository.

        Returns
        -------
        ElementRepository
            Repository containing the elements of the subset.

        """
        # If there is in anvalid element tag, an error will be raised
        # by the index mapper, thus there is no need to check for valid
        # inputs here
        indices = np.asarray([self.index_mapper[e]
                              for e in element_tags], dtype=int)

        tags = self.tags[indices]
        connectivity = [self.connectivity[i] for i in indices]
        types = self.types[indices]

        # Generate a new element repository to return
        return_repo = ElementRepository(tags, connectivity, types)

        # Make sure the indices are coherent with the original model
        return_repo.index_mapper = dict(zip(tags, indices))

        # Extract group elements that are present in the subset
        for group_name, group_tags in self.groups.items():
            new_group_tags = np.intersect1d(group_tags, element_tags)
            return_repo.add_group(group_name, new_group_tags)

        return return_repo

    def get_subset_by_type(self, *element_types):
        """
        Create a new ElementRepositroy for a subset of elements by type.

        Parameters
        ----------
        *element_types : Sequence[int]
            Types of the elements that will be part of the repository.
            The element types must follow the VTK type convention.

        Returns
        -------
        ElementRepository
            Repository containing the elements of the subset.

        """
        indices = []
        for element_type in element_types:
            indices.append(np.asarray(self.types == element_type)
                           .nonzero()[0])

        # Flatten the list of indices
        indices = np.concatenate(indices)

        # Return None in case nothing was found
        if len(indices) == 0:
            return None

        # Build the new repo
        tags = self.tags[indices]
        connectivity = [self.connectivity[i] for i in indices]
        types = self.types[indices]

        return_repo = ElementRepository(tags, connectivity, types)
        return_repo.index_mapper = dict(zip(tags, indices))

        return return_repo

    def get_node_tags(self):
        """
        Get the node tags of the elements in the ElementRepository.

        Returns
        -------
        tags : numpy.ndarray[int]
            Sorted node tags.

        """
        tags = np.unique(list(itertools.chain(*self.connectivity)))
        tags.sort()
        return tags


class NodeRepository(MeshRepositoryBaseClass):
    """
    Repository to store a set of nodes.

    Parameters
    ----------
    node_tags : Sequence[int]
        Tags of all nodes that will be stored in the repository.
    node_coords : Sequence[Sequence[float]]
        Nodal coordinates in the order defined for the node tags. The
        coordinates can be defined in 1d-, 2d- or 3d-space as an array
        of shape (number of nodes, number of dimensions).

    Attributes
    ----------
    tags : numpy.ndarray[int]
        Tags of all nodes stored in the repository.
    coordinates : numpy.ndarray[float]
        Coordinates of all nodes in the order defined for the node tags.
    index_mapper : dict[int, int]
        Mapping node tag -> index in list of tags.
    groups : dict[str, numpy.ndarray[int]]
        Mapping group name -> node tags.

    """

    def __init__(self,
                 node_tags,
                 node_coords):

        assert len(node_tags) == len(node_coords), \
            ("The amounts of node tags and coordinate entries do not match.")

        super(NodeRepository, self).__init__(node_tags)
        self.index_mapper = dict(zip(node_tags, range(len(node_tags))))

        node_coords = np.asarray(node_coords, dtype=float).reshape(
            (len(self._tags), -1))
        _, columns = node_coords.shape
        if columns not in (1, 2, 3):
            msg = "Invalid nodal coordinates."
            raise ValueError(msg)

        self._coordinates = node_coords

    @property
    def coordinates(self):
        """The nodal coordinates."""
        return self._coordinates

    def __getitem__(self, key):
        """Index-based access."""
        return (self.tags[key], self.coordinates[key],
                self.index_mapper[self.tags[key]])

    def get_subset(self, *node_tags):
        """
        Create a new NodeRepository for a subset of nodes by tags.

        Parameters
        ----------
        *node_tags : Sequence[int]
            Nodes that will be contained in the new repository.

        Returns
        -------
        NodeRepository
            Repository containing the nodes of the subset.

        """
        # If there is in anvalid element tag, an error will be raised
        # by the index mapper, thus there is no need to check for valid
        # inputs here
        indices = np.array([self.index_mapper[n] for n in node_tags])

        tags = self.tags[indices]
        coords = self.coordinates[indices]

        # Generate a new element repository to return
        return_repo = NodeRepository(tags, coords)

        # Make sure the indices are coherent with the original model
        return_repo.index_mapper = dict(zip(tags, indices))

        # Extract group elements that are present in the subset
        for group_name, group_tags in self.groups.items():
            new_group_tags = np.intersect1d(group_tags, node_tags)
            return_repo.add_group(group_name, new_group_tags)

        return return_repo


class FieldRepositoryBaseClass(object):
    """
    Base class for field repositories.

    Attributes
    ----------
    fields : dict[str, Field]
        Mapping field name -> field.

    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self._fields = {}

    @property
    def fields(self):
        """The mapping field name -> field."""
        return self._fields

    def __getitem__(self, field_name):
        """Key-based access."""
        return self.fields[field_name]

    def __iter__(self):
        """Repository iterator."""
        return self.fields.values().__iter__()

    def __len__(self):
        """Repository size."""
        return len(self.fields)

    def __delitem__(self, key):
        del self.fields[key]

    def keys(self):
        """Repository keys."""
        return self.fields.keys()

    def get_fields_by_type(self, field_type):
        """
        Export fields based on a requested field type.

        Parameters
        ----------
        field_type : ParaqusConstant
            Type of the field, i.e. ``TENSOR``, ``VECTOR`` or
            ``SCALAR``.

        Returns
        -------
        list[Field]
            Fields that match the requested type.

        """
        return [f for f in self.fields.values() if f.field_type == field_type]

    @abstractmethod
    def add_field(self, field):
        """Add a new node or element field to the repository."""
        return

    @abstractmethod
    def get_subset(self, repository):
        """Export node or element fields for a subset."""
        return


class NodeFieldRepository(FieldRepositoryBaseClass):
    """
    Repository to stored nodal fields.

    Attributes
    ----------
    fields : dict[str, Field]
        Mapping field name -> Field.

    """

    def __init__(self):
        super(NodeFieldRepository, self).__init__()

    def add_field(self, field):
        """
        Add a new node field to the repository.

        Parameters
        ----------
        field : Field
            The field with position ``NODES`` to add to the
            repository.

        Returns
        -------
        None.

        """
        if field.field_position == NODES:

            if self.fields.get(field.field_name) is not None:
                msg = ("Node field '{}'".format(field.field_name)
                       + " has already been stored and will be overwritten.")
                warnings.warn(msg)

            self.fields[field.field_name] = field

        else:
            msg = ("Provided field's position is '{}' and not '{}'."
                   .format(field.field_position, NODES))
            raise ValueError(msg)

    def get_subset(self, repository):
        """
        Export node fields for a subset of nodes.

        The nodes are specified by a NodeRepository, which should be
        derived from a common main model by model.nodes.get_subset()
        to ensure coherent indexing.

        Parameters
        ----------
        repository : NodeRepository
            Node repository containing the subset of nodes.

        Returns
        -------
        sub_fields : list[Field]
            The fields matching the subset of nodes.

        """
        tags = repository.tags
        index_mapper = repository.index_mapper
        indices = np.array([index_mapper[i] for i in tags])

        sub_fields = [Field(f.field_name,
                            f.field_values[indices],
                            f.field_position,
                            f.field_type) for f in self.fields.values()]

        return sub_fields


class ElementFieldRepository(FieldRepositoryBaseClass):
    """
    Repository to stored elemental fields.

    Attributes
    ----------
    fields : dict[str, Field]
        Mapping field name -> Field.


    """

    def __init__(self):
        super(ElementFieldRepository, self).__init__()

    def add_field(self, field):
        """
        Add a new element field to the repository.

        Parameters
        ----------
        field : Field
            The field with position ``ELEMENTS`` to add to the
            repository.

        Returns
        -------
        None.

        """
        if field.field_position == ELEMENTS:

            if self.fields.get(field.field_name, None) is not None:
                msg = ("Element field '{}'".format(field.field_name)
                       + " has already been stored and will be overwritten.")
                warnings.warn(msg)

            self.fields[field.field_name] = field

        else:
            msg = ("Provided field's position is '{}' and not '{}'."
                   .format(field.field_position, ELEMENTS))
            raise ValueError(msg)

    def get_subset(self, repository):
        """
        Export element fields for a subset of elements.

        The elements are specified by an ElementRepository, which should
        be derived from a common model via
        ``model.elements.get_subset()`` to ensure coherent indexing.

        Parameters
        ----------
        repository : ElementRepository
            Element repository containing the subset of elements.

        Returns
        -------
        sub_fields : list[Field]
            The fields matching the subset of elements.

        """
        tags = repository.tags
        index_mapper = repository.index_mapper
        indices = np.array([index_mapper[i] for i in tags])

        sub_fields = [Field(f.field_name,
                            f.field_values[indices],
                            f.field_position,
                            f.field_type) for f in self.fields.values()]

        return sub_fields


class Field(object):
    """
    Definition of nodal or elemental fields.

    Parameters
    ----------
    field_name : str
        Name of the field.
    field_values : Sequence[Sequence[float]]
        Values of the field. In case the field will be added to a model,
        the values must be in the order defined for the respective node
        or element tags.
    field_position : ParaqusConstant
        Position of the field, i.e. ``NODES`` or ELEMENTS``.
    field_type : ParaqusConstant
        Type of the field, i.e. ``TENSOR``, ``VECTOR`` or ``SCALAR``.

    Attributes
    ----------
    field_name : str
        Name of the field.
    field_position : ParaqusConstant
        Position of the field, i.e. ``NODES`` or ``ELEMENTS``.
    field_type : ParaqusConstant
        Type of the field, i.e. ``TENSOR``, ``VECTOR`` or ``SCALAR``.
    field_values : numpy.ndarray[float]
        Field values of the field.

    """

    def __init__(self,
                 field_name,
                 field_values,
                 field_position,
                 field_type):

        self._field_name = field_name

        # Add position
        if field_position not in (NODES, ELEMENTS):
            msg = "Invalid field position: {}".format(field_position)
            raise ValueError(msg)
        self._field_position = getattr(
            constants, str(field_position).upper())

        # Add type
        if field_type not in (SCALAR, VECTOR, TENSOR):
            msg = "Invalid field type: {}".format(field_type)
            raise ValueError(msg)
        self._field_type = getattr(constants, str(field_type).upper())

        # Add values
        field_values = np.asarray(field_values, dtype=float)
        if self._field_type == SCALAR:
            if np.squeeze(field_values).ndim > 1:
                msg = "Data for scalar field is not 1d."
                raise ValueError(msg)
            self._field_values = field_values.reshape((-1, 1))
        else:
            self._field_values = field_values

    @property
    def field_name(self):
        """The name of the field."""
        return self._field_name

    @property
    def field_values(self):
        """The values of the field."""
        return self._field_values

    @property
    def field_position(self):
        """The position of the field, e.g. ``NODES`` or ``ELEMENTS``."""
        return self._field_position

    @property
    def field_type(self):
        """The field type, e.g. ``SCALAR`` or ``VECTOR``."""
        return self._field_type

    def __repr__(self):
        descr = "Field '{}' of type '{}' at position '{}'".format(
            self.field_name, self.field_type, self.field_position)
        return descr

    def __len__(self):
        return len(self.field_values)

    def get_3d_field_values(self):
        """
        Get a copy of the field values in 3d representation.

        Vectors are in order (x, y, z) and tensors are in order
        (xx, yy, zz, xy, yz, xz). Non-symmetric tensors are not
        supported.

        Returns
        -------
        numpy.ndarray[float]
            The 3d representation of the field values.

        """
        if self.field_type == SCALAR:
            return self.field_values

        if self.field_type == VECTOR:
            nvals, ndim = self.field_values.shape
            if ndim < 3:
                return np.hstack((self.field_values, np.zeros((nvals,
                                                               3 - ndim))))
            return self.field_values

        # case field_type == TENSOR
        nvals, ndim = self.field_values.shape
        if ndim < 6:
            return np.hstack((self.field_values, np.zeros((nvals, 6 - ndim))))
        return self.field_values
