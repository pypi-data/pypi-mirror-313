"""


Collection Operators
********************

:func:`create`

:func:`export_all`

:func:`exporter_add`

:func:`exporter_export`

:func:`exporter_remove`

:func:`objects_add_active`

:func:`objects_remove`

:func:`objects_remove_active`

:func:`objects_remove_all`

"""

import typing

def create(*args, name: str = 'Collection') -> None:

  """

  Create an object collection from selected objects

  """

  ...

def export_all() -> None:

  """

  Invoke all configured exporters on this collection

  """

  ...

def exporter_add(*args, name: str = '') -> None:

  """

  Add Exporter

  """

  ...

def exporter_export(*args, index: int = 0) -> None:

  """

  Invoke the export operation

  """

  ...

def exporter_remove(*args, index: int = 0) -> None:

  """

  Remove Exporter

  """

  ...

def objects_add_active(*args, collection: str = '') -> None:

  """

  Add the object to an object collection that contains the active object

  """

  ...

def objects_remove(*args, collection: str = '') -> None:

  """

  Remove selected objects from a collection

  """

  ...

def objects_remove_active(*args, collection: str = '') -> None:

  """

  Remove the object from an object collection that contains the active object

  """

  ...

def objects_remove_all() -> None:

  """

  Remove selected objects from all collections

  """

  ...
