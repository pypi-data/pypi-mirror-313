from typing import List, Optional, Union

from pydantic.v1 import BaseModel

from fiddler.constants.model import DataType


class Column(BaseModel):
    """A model column representation"""

    name: str
    """Column name provided by the customer"""

    data_type: DataType
    """Data type of the column"""

    min: Optional[Union[int, float]] = None
    """Min value of integer/float column"""

    max: Optional[Union[int, float]] = None
    """Max value of integer/float column"""

    categories: Optional[List] = None
    """List of unique values of a categorical column"""

    bins: Optional[List[Union[int, float]]] = None
    """Bins of integer/float column"""

    replace_with_nulls: Optional[List] = None
    """Replace the list of given values to NULL if found in the events data"""

    n_dimensions: Optional[int] = None
    """Number of dimensions of a vector column"""

    class Config:
        smart_union = True


class ModelSchema(BaseModel):
    """Model schema with the details of each column"""

    schema_version: int = 1
    """Schema version"""

    columns: List[Column]
    """List of columns"""

    def _col_index_from_name(self, name: str) -> int:
        """Look up the index of the column by name"""
        for i, col in enumerate(self.columns):
            if col.name == name:
                return i
        raise KeyError(name)

    def __getitem__(self, item: str) -> Column:
        """Get column by name"""
        return self.columns[self._col_index_from_name(item)]

    def __setitem__(self, key: str, value: Column) -> None:
        """Set column by name"""
        try:
            index = self._col_index_from_name(key)
            self.columns[index] = value
        except KeyError:
            self.columns.append(value)

    def __delitem__(self, key: str) -> None:
        """Delete column by name"""
        self.columns.pop(self._col_index_from_name(key))
