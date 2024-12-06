#===============================================================================
# Parameter Grid
#===============================================================================

"""
The PSCAD Parameter Grid Proxy Object
"""

#===============================================================================
# Imports
#===============================================================================

import logging
from typing import Optional, Union

import mhi.common.path

from .remote import requires
from .project import Project
from .component import Component
from .definition import Definition


#===============================================================================
# Logging
#===============================================================================

LOG = logging.getLogger(__name__)


#===============================================================================
# Parameter Grid
#===============================================================================

class ParameterGrid:
    """
    The Parameter Grid interface
    """

    def __init__(self, pscad):
        self._pscad = pscad

    @property
    def main(self):
        """Main PSCAD application reference"""
        return self._pscad.main

    def _param_grid(self, **kwargs):
        self._pscad._param_grid(**kwargs)

    def view(self, subject: Union[Component, Definition, Project]) -> None:
        """
        Load subject into the parameter grid.

        The property grid is able to view and modify several components at
        once.

        If the subject is a component or component definition, all of the
        instances of that component are loaded into the parameter grid.

        If the subject is a project, all of the corresponding project types
        (libraries or cases) are loaded into the parameter grid.
        """
        self._param_grid(source=subject)

    @requires("5.1")
    def view_cases(self) -> None:
        """
        Load all project cases into the parameter grid.
        """
        self._param_grid(kind='Case')

    @requires("5.1")
    def view_libraries(self) -> None:
        """
        Load all libraries into the parameter grid.

        Note: The 'master' library is always omitted.
        """
        self._param_grid(kind='Library')

    def view_simulation_sets(self) -> None:
        """
        Load all simulation sets into the property grid.

        This allows for viewing / editing multiple simulation sets in the
        workspace at once.
        """
        self._param_grid(kind='SimSets')

    def view_simulation_tasks(self) -> None:
        """
        Load all simulation tasks into the property grid.

        This allows for viewing / editing multiple simulation tasks in the
        workspace at once.
        """
        self._param_grid(kind='SimSetTasks')

    def view_simulation_task_overrides(self) -> None:
        """
        Load simulation tasks’ project overrides into the property grid.

        This allows for viewing / editing multiple sets of project overrides
        in the workspace at once.
        """
        self._param_grid(kind='SimSetTaskOverrides')

    def view_simulation_task_layers(self, scope: Union[Project, str]) -> None:
        """
        Load simulation tasks’ layers configurations into the property grid.

        This allows for viewing / editing multiple sets of layers
        configurations in the workspace at once.

        Parameters:
            scope: The project object or a project name
        """

        if isinstance(scope, Project):
            prj = scope
            namespace = prj.name
        elif isinstance(scope, str):
            namespace = scope
        else:
            raise TypeError("Expected project or string")

        self._param_grid(kind='SimSetTaskLayers', namespace=namespace)

    def save(self, filename: str, folder: Optional[str] = None) -> None:
        """
        Write parameter grid to a CSV file.

        Parameters:
            filename (str): Filename of the CSV file to write.
            folder (str): Directory where the CSV file will be stored (optional)
        """

        filename = mhi.common.path.expand_path(filename, abspath=True,
                                               folder=folder)

        LOG.info("%s: Save parameter grid to '%s'", self, filename)

        return self._pscad._param_grid_save(filename)

    def load(self, filename: str, folder: Optional[str] = None) -> None:
        """
        Load parameter grid from a CSV file.

        Parameters:
            filename (str): Filename of the CSV file to read.
            folder (str): Directory to read the CSV file from (optional)
        """

        filename = mhi.common.path.expand_path(filename, abspath=True,
                                               folder=folder)

        LOG.info("%s: Load parameter grid from '%s'", self, filename)

        return self._pscad._param_grid_load(filename)
