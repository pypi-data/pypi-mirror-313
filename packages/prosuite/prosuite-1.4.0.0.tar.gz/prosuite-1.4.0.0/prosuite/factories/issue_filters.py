__author__ = "The ProSuite Authors"
__copyright__ = "Copyright 2021-2023, The ProSuite Authors"
__license__ = "MIT"
__version__ = "1.2.1.1"
__maintainer__ = "Dira GeoSystems"
__email__ = "programmers@dirageosystems.ch"
__date__  = "22.12.2023"
__status__ = "Production"


from datetime import datetime
from typing import List
from prosuite.quality import Parameter
from prosuite.quality import IssueFilter
from prosuite.data_model import BaseDataset
from prosuite.factories.enums import *

class IssueFilters:
    """
    :noindex:

    Your existing documentation goes here.
    """

    @classmethod
    def not_yet_implemented(cls, feature_class: BaseDataset, tolerance: float) -> IssueFilter:
        """
        Stay tuned
        """
        
        result = IssueFilter("dummy(0)")
        return result