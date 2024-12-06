__all__ = ['Condition', 'Parameter', 'Specification']
from enum import Enum
from typing import List, Union
import typing
import prosuite.utils as utils

import prosuite.generated.shared_qa_pb2 as shared_qa

class Parameter:
    """
    A parameter configures a quality condition. Parameters can represent Datasets (dataset parameter) or scalar values
    (scalar parameters). Parameters have a name and a value.

    Dataset parameters: value is of type dataset. the parameter can retrieve the workspace id (model name) and the where
    clause (filter expression) of the dataset.

    Scalar parameters: value is a simple type (number, string, bool).
    """
    def __init__(self, name: str, value):
        self.contains_list_of_datasets = False
        if self._value_type_is_dataset(value):
            self.dataset = value
        else:
            self.dataset = None

        self.name: str = name
        self.value = value

    def get_string_value(self) -> str:
        if self.dataset:
            if self.contains_list_of_datasets:
                return self.dataset[0].name
            else:
                return self.dataset.name
        else:
            if self.value is None:
                return ""
            else:
                return str(self.value)

    def is_dataset_parameter(self) -> bool:
        if self.dataset:
            return True
        else:
            return False

    def get_workspace_id(self):
        if not self.dataset:
            return ""
        return self.dataset.model.name

    def get_where_clause(self):
        if not self.dataset:
            return ""
        if self.contains_list_of_datasets:
            return self.dataset[0].filter_expression
        else:
            return self.dataset.filter_expression

    @staticmethod
    def value_is_list_of_datasets(value):
        from prosuite.data_model import Dataset
        if isinstance(value, list):
            if all(isinstance(x, Dataset) for x in value):
                return True
        return False

    def _value_type_is_dataset(self, value):
        from prosuite.data_model import BaseDataset
        if Parameter.value_is_list_of_datasets(value):
            self.contains_list_of_datasets = True
            return True
        if isinstance(value, BaseDataset):
            return True
        return False

class IssueFilter():

    def __init__(self, issue_filter_descriptor: str, name: str = "", expression: str = ""):

        #:
        self.name = name
        """
        The unique name of the issue filter.
        """
        #:
        self.issue_filter_descriptor = issue_filter_descriptor
        """
        The issue filter descriptor, i.e. the algorithm used to filter the issues.
        """

        self.parameters: List[Parameter] = []
        """
        The list of parameters. Typically the parameters are specified in the factory method used to create the
        issue filter (see :py:mod:`prosuite.factories.issue_filters`) and do not need to be changed
        through this list.
        """

        self.expression = expression


    def generate_name(self):
        """
        Generates a technical name using the dataset name(s) and the test descriptor. This is the default name of 
        a condition if it was created by the standard factory method from :py:mod:`prosuite.factories.quality_conditions`.
        """
        descriptor = self.issue_filter_descriptor
        params = self.parameters

        self.name = create_name(descriptor, params)


class Condition:
    """
    Defines a quality condition, i.e. the configuration of a test algorithm for one or more datasets. 
    Conditions must be created with the factory methods from :py:mod:`prosuite.factories.quality_conditions` 
    """

    def __init__(self, test_descriptor: str, name: str = ""):

        #:
        self.name = name
        """
        The unique name of the quality condition.
        """
        #:
        self.test_descriptor = test_descriptor
        """
        The test descriptor, i.e. the algorithm used to verify this condition.
        """
        
        # New doc: The type/severity of the quality issues identified by this quality condition. Quality conditions with 
        # “Issue Type = Warning” are considered “soft” conditions, for which exceptions (“Allowed Issues”) may be defined.
        self.allow_errors: bool = IssueType == IssueType.Warning
        # Change by MBR 16/12/23
        #self.allow_errors: bool = self.issue_type == IssueType.Warning
        """
        For internal use only.
        """
        
        # NOTE: Issue type is not processed in the service, because on the server it is called allowed_errors (see above).
        self.issue_type: IssueType = IssueType.Error
        """
        Defines if a failing test returns a warning or an error issue. Quality conditions with 
        Issue Type = Warning are considered “soft” conditions, for which exceptions (“Allowed Issues”) may be defined.
        """

        #:
        self.category: str = ""
        """
        The name of the category, if this issue is assigned to a category.
        """
        #:
        self.stop_on_error: bool = False
        """
        Indicates if the occurrence of an error for an object should stop any further testing of the same object. 
        This can be used to prevent further tests on a feature after a serious geometry error (e.g. incorrectly 
        oriented rings) was detected for the feature.
        The used Test Descriptor provides a standard value for this property. It can optionally be overridden here.
        """
        #:
        self.description: str = ""
        """
        Freely definable description of the Quality Condition. This description can be displayed when viewing 
        issues in the issue navigator, and may contain explanations to the Quality Condition and instructions for 
        correcting the issues.
        """
        #:
        self.url: str = ""
        """
        Optional URL to a website providing additional information for this Quality Condition.
        Certain Quality Conditions require more detailed information about the test logic and/or the correction 
        guidelines than the field “Description” can provide. This information can for example be assembled in a 
        wiki, and the URL may be provided here. When viewing issues in the issue navigator, the corresponding web 
        page can be opened. In the HTML verification reports these URLs are used to render the names of the 
        Quality Conditions as links.
        """
        #:
        self.parameters: List[Parameter] = []
        """
        The list of parameters. Typically the parameters are specified in the factory method used to create the
        quality condition (see :py:mod:`prosuite.factories.quality_conditions`) and do not need to be changed
        through this list.
        """
        #:
        self.issue_filters: List[IssueFilter] = []
        """
        Reserved for future use.
        """
        #:
        self.issue_filter_expression: str
        """
        Reserved for future use.
        """

    def generate_name(self):
        """
        Generates a technical name using the dataset name(s) and the test descriptor. This is the default name of 
        a condition if it was created by the standard factory method from :py:mod:`prosuite.factories.quality_conditions`.
        """
        descriptor = self.test_descriptor
        params = self.parameters

        self.name = create_name(descriptor, params)

# Static method:
# TODO: Extract Parameter class and utils methods such as this one to core.py module
    # to avoid circular dependencies. core.py can then be referencedboth from 
    # data_model (TransformedDataset) and quality (Condition)
def create_name(descriptor, params) -> str:
    first_dataset_parameter = next(
        (p for p in params if p.is_dataset_parameter()), None)
    if first_dataset_parameter:
        ds_param: Parameter = first_dataset_parameter
        if ds_param.contains_list_of_datasets:
            dataset_list: List[str] = [ds.name for ds in ds_param.dataset]
            dataset_names = "_".join(dataset_list)
            
            return f"{descriptor} {dataset_names}"
        else:
            return f"{descriptor} {ds_param.dataset.name}"
            
class Specification:
    def __init__(self, name: str = 'Custom Specification', description: str = ''):
        """
        CustomSpecification stores conditions.
        :param name: specification name
        :type name: str
        :param description: specification description
        :type description: str
        """
        self._conditions: typing.List[Condition] = []
        self.name = name
        self.description = description

    def add_condition(self, condition: Condition):
        """
        Adds conditions to the specification
        """
        self._conditions.append(condition)

    def get_conditions(self) -> typing.List[Condition]:
        """
        Returns the List of conditions
        """
        return self._conditions

class XmlSpecification:
    """
    Represents a specification defined in the xml specification schema:

    :param specification_file: path to the xml specification file
    :type specification_file: str
    :param specification_name: name of the specification (in the xml file) that should be executed. If not defined in the constructor, it needs to be defined later.
    :type specification_name: str
    :param data_source_replacements: a list containing a list with two string elements. these represent a workspace id, and the path to the workspace
    :type data_source_replacements: [[str]] example: [["TLM_Production", "C:/temp/user@topgist.sde"]]
    """

    def __init__(self, specification_file: str, specification_name: str = None,
                 data_source_replacements: List[List[str]] = None):

        self.specification_name: str = None
        self.data_source_replacements = XmlSpecification._parse_datasource_replacements(data_source_replacements)
        self._specification_msg = None
        self.xml_string = XmlSpecification._read_file_as_string(specification_file)
        self.specification_file = specification_file
        self.specification_name = specification_name

    @staticmethod
    def _read_file_as_string(file_path) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
            return data

    @staticmethod
    def _parse_datasource_replacements(data_source_replacements: List[List[str]]):
        result = []
        for pair in data_source_replacements:
            result.append(f"{pair[0]}|{pair[1]}")
        return result

    @staticmethod
    def get_specification_names(specification_file: str) -> typing.List[str]:
        """
        Returns a list of the specification names of all specifications in all categories of the xml-specifications doc.

        :param specification_file: path of xml specification file.
        :type specification_file: str
        :return: List of specification names
        :rtype: [str]
        """
        specification_names = []
        xml = utils.objectify_xml(specification_file)
        for cat in xml.Categories:
            for qs in cat.Category.QualitySpecifications:
                name = utils.try_get_lxml_attrib(qs.QualitySpecification, 'name')
                if name:
                    specification_names.append(name)
        return specification_names

class DdxSpecification:
    # TODO: Datasource replacements are not yet used. Consider converting them to some kind of work context
    #       (GDB version name, FGDB checkout).
    """
    Represents a specification defined in the DDX:

    :param ddx_id: id of the ddx specification
    :type ddx_id: int
    :param project_short_name: short name of the project (e.g. "TLM")
    :type project_short_name: str
    :param data_source_replacements: a list containing a list with two string elements. these represent a workspace id, and the path to the workspace
    :type data_source_replacements: [[str]] example: [["TLM_Production", "C:/temp/user@topgist.sde"]]
    """

    def __init__(self, ddx_id: int, project_short_name: str):
        self.ddx_id = ddx_id
        self.project_short_name = project_short_name  # To be used in the WorkContextMsg
        #self.name = name

    @staticmethod
    def _parse_datasource_replacements(data_source_replacements: List[List[str]]):
        if data_source_replacements is None:
            return []  # Return an empty list if replacements are not provided
        result = []
        for pair in data_source_replacements:
            result.append(f"{pair[0]}|{pair[1]}")
        return result

# Separate Funktion für get_specification_names & ids aus DDX?

class IssueType(Enum): 
    Warning = 0
    Error = 1
