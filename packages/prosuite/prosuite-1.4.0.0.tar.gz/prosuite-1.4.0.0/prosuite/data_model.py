class Model:
    """
    The Model represents the data model in a workspace (file-gdb or enterprise-gdb)

    catalog_path examples:
        c:/data.gdb
        c:/enterprise_gdb.sde
    """

    def __init__(self, name, catalog_path):

        #:
        self.name: str = name
        """
        The unique name of the model.
        """
        #:
        self.catalog_path: str = catalog_path
        """
        The catalog path of the associated workspace.
        """

class BaseDataset():
    """
    The base class for datasets representing tabular data. It is either a :class:`.Dataset` or, in the future, a :class:`.TransformedDataset`
    """
    def __init__(self, name: str, filter_expression: str = ""):
        self.name: str = name
        self.filter_expression: str = filter_expression
        pass


class Dataset(BaseDataset):
    """
    A dataset represents data from a table or feature class in a workspace, optionally filtered by an SQL expression.

    :param name: table or featureclass name
    :type name: str
    :param model: The :class:`prosuite.data_model.Model` this dataset belongs to.
    :type model: class:`prosuite.data_model.Model`
    :param filter_expression: A where clause that filters the table. The syntax of the where clause is defined in
        the document SQLSyntax_en.pdf
    :type filter_expression: str, optional
    """

    def __init__(self, name: str, model: Model, filter_expression: str = ""):
        super().__init__(name, filter_expression)
        self.model: Model = model


class TransformedDataset(BaseDataset):

    def __init__(self, transformer_descriptor: str, name: str = "", filter_expression: str = ""):
        from prosuite.quality import Parameter
        from typing import List
        super().__init__(name, filter_expression)

        #:
        self.name = name
        """
        The unique name of the transformed dataset.
        """
        #:
        self.transformer_descriptor = transformer_descriptor
        """
        The transformer descriptor, i.e. the algorithm used to generate this dataset.
        """

        self.parameters: List[Parameter] = []
        """
        The list of parameters. Typically the parameters are specified in the factory method used to create the
        transformed dataset (see :py:mod:`prosuite.factories.transformers`) and do not need to be changed
        through this list.
        """

    def generate_name(self):
        """
        Generates a technical name using the dataset name(s) and the test descriptor. This is the default name of 
        a condition if it was created by the standard factory method from :py:mod:`prosuite.factories.quality_conditions`.
        """
        descriptor = self.transformer_descriptor
        params = self.parameters

        self.name = create_name(descriptor, params)

# Static method (copy from quality condition)
# TODO: Extract Parameter class and utils methods such as this one to core.py module
    # to avoid circular dependencies. core.py can then be referencedboth from 
    # data_model (TransformedDataset) and quality (Condition)
def create_name(descriptor, params) -> str:
    from typing import List
    from prosuite.quality import Parameter

    first_dataset_parameter = next(
        (p for p in params if p.is_dataset_parameter), None)
    if first_dataset_parameter:
        ds_param: Parameter = first_dataset_parameter
        if ds_param.contains_list_of_datasets:
            dataset_list: List[str] = [ds.name for ds in ds_param.dataset]
            dataset_names = "_".join(dataset_list)
            
            return f"{descriptor} {dataset_names}"
        else:
            return f"{descriptor} {ds_param.dataset.name}"