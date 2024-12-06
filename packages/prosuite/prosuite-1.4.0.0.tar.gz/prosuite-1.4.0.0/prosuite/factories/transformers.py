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
from prosuite.data_model import BaseDataset, TransformedDataset
from prosuite.quality import Parameter
from prosuite.factories.enums import *

class Transformers:
    @classmethod
    def not_yet_implemented(cls, feature_class: BaseDataset, tolerance: float) -> TransformedDataset:
        """
        Stay tuned
        """
        
        result = TransformedDataset("dummy(0)")
        return result

