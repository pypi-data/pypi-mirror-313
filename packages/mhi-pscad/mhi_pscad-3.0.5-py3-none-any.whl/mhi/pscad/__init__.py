#===============================================================================
# Manitoba Hydro Internation / Power Technology Center
# mhi.pscad package
#===============================================================================

"""
Connection Methods
==================

The PSCAD Automation Library provides three methods of connecting to the PSCAD
Application:

1. Launching a new instance of PSCAD
2. Connect to an existing PSCAD instance
3. Connect to an existing PSCAD instance if any, or launch a new instance of PSCAD otherwise.


New Instance
------------

To launch and connect to new PSCAD instance, use the following command:

.. autofunction:: mhi.pscad.launch


Existing Instance
-----------------

To connect to already running PSCAD instance, use the following command:

.. autofunction:: mhi.pscad.connect

If multiple instances are running, the Automation Library will connect
to one of them.
If the port which the desired instance of PSCAD is listening on is known,
the ``port=#`` option may be given in ``connect()``::

   pscad = mhi.pscad.connect(port=54321)

If the desired PSCAD instance is running on another machine,
the ``host="..."`` parameter must be given as well::

   pscad = mhi.pscad.connect(host="192.168.0.123", port=54321)

Existing or New
---------------

To connect to any running PSCAD instance,
or launch & connect to a new PSCAD instance if there are no existing instances,
or if running the script from inside PSCAD itself, use the following command:

.. autofunction:: mhi.pscad.application

Product Versions
================

PSCAD
-----

.. autofunction:: mhi.pscad.versions

Fortran & Matlab
----------------

.. note::

    The Automation Library retrieves the list of installed Fortran and Matlab
    versions from the `ProductsList.xml` file.
    When any version of Fortran or Matlab is installed or uninstalled, run the
    `Generate installed products list` command from the Environment Medic
    utility in the PSCAD "Tools" menu.

.. autofunction:: mhi.pscad.fortran_versions
.. autofunction:: mhi.pscad.matlab_versions
"""

#===============================================================================
# Imports
#===============================================================================

import logging
import os
import sys
import warnings

from collections import ChainMap, defaultdict
from pathlib import Path
from typing import cast, Any, Dict, List, Optional, Tuple
from warnings import warn

from xml.etree import ElementTree as _ET

import mhi.common

from mhi.common import config
from mhi.common.path import shell_folder
from mhi.common.remote import Remotable, deprecated, Context
from mhi.common.codec import MapCodec

from .pscad import PSCAD
from .project import Project, Layer, Resource, GlobalSubstitution
from .simset import SimulationSet, SimsetTask, ProjectTask, ExternalTask
from .canvas import Canvas, UserCanvas
from .definition import Definition
from .component import ZComponent, Component, UserCmp
from .component import Wire, StickyWire, Bus, TLine, Cable
from .annotation import Sticky, Divider, GroupBox
from .graph import GraphFrame, GraphPanel, OverlayGraph, PolyGraph, PlotFrame, Curve
from .control import ControlFrame, Control, Button, Switch, Selector, Slider
from .instrument import Instrument, PolyMeter, PhasorMeter, Oscilloscope
from .certificate import Certificate, Feature
from .graphics import GfxCanvas, GfxComponent, Port, Text
from .graphics import GfxBase, Line, Rect, Oval, Arc, Shape

# PSCAD 5.0.0 compatibility:
sys.modules['mhi.pscad.common'] = sys.modules['mhi.common']


#===============================================================================
# Script Version Identifiers
#===============================================================================

_VERSION = (3, 0, 5)

_TYPE = 'f0'

VERSION = '.'.join(map(str, _VERSION))
VERSION_HEX = int.from_bytes((*_VERSION, int(_TYPE, 16)), byteorder='big')


#===============================================================================
# Logging
#===============================================================================

_LOG = logging.getLogger(__name__)


#===============================================================================
# Options
#===============================================================================

OPTIONS: Dict[str, Any] = config.fetch("~/.mhi.pscad.py")


#===============================================================================
# Connection and Application Start
#===============================================================================

def application() -> PSCAD:
    """
    This method will find try to find a currently running PSCAD application,
    and connect to it.  If no running PSCAD application can be found, or
    if it is unable to connect to that application, a new PSCAD application
    will be launched and a connection will be made to it.

    If running inside a Python environment embedded within an PSCAD
    application, the containing application instance is always returned.

    Returns:
        PSCAD: The PSCAD application proxy object

    Example::

        import mhi.pscad
        pscad = mhi.pscad.application()
        pscad.load('myproject.pscx')

    .. versionadded:: 2.0
    """

    app_ = Context._application(connect, launch, 'PSCAD%.exe')
    return cast(PSCAD, app_)


def connect(host: Optional[str] = None, port: int = 0,
            timeout: int = 5) -> PSCAD:
    """
    This method will find try to find a currently running PSCAD application,
    and connect to it.

    Parameters:
        host (str): The host the PSCAD application is running on
            (defaults to the local host)

        port (int): The port to connect to.  Required if running multiple
            PSCAD instances, or attempting to connect to a remote host.

        timeout (int): Seconds to wait for the connection to be accepted.

    Returns:
        PSCAD: The PSCAD application proxy object

    Example::

        import mhi.pscad
        pscad = mhi.pscad.connect()
        pscad.load('myproject.pscx')

    .. versionadded:: 2.0
    """

    # If the port is not specified, we need to find a running PSCAD process on
    # the current machine that is listening for connections on some port.

    if port == 0:

        import socket                  # pylint: disable=import-outside-toplevel
        from mhi.common import process # pylint: disable=import-outside-toplevel

        if host is not None and not process.is_local_host(host):
            raise ValueError(f"Cannot autodetect port on foreign host {host!r}")

        listeners = process.listener_ports_by_name('PSCAD%')
        if not listeners:
            raise ProcessLookupError("No available PSCAD processes")

        if host is not None:
            listeners = list(filter(process.host_filter(host), listeners))
            if not listeners:
                raise ProcessLookupError("No matching PSCAD processes")

        host, port, pid, appname = listeners[0]
        _LOG.info("%s [%d] listening on [%s]:%d", appname, pid, host, port)
        if host in {'0.0.0.0', '::'}:
            host = socket.getfqdn()

    _LOG.info("Connecting to [%s]:%d", host, port)

    app_ = Context._connect(host=host, port=port, timeout=timeout)
    app = cast(PSCAD, app_)

    app._initialize()

    app.wait_for_idle()

    return app


def launch(port=None, silence=True,
           minimize=False, splash=False, timeout=5, version=None, x64=None,
           settings=None, load_user_profile=None, minimum='5.0', maximum=None,
           allow_alpha=None, allow_beta=False, load=None, extra_args=None,
           address=None,
           **options) -> PSCAD:
    """
    Launch a new PSCAD instance and return a connection to it.

    Parameters:
        port (int|range): The port to connect to.  Required if running multiple
            PSCAD instances.

        silence (bool): Suppresses dialogs which can block automation.

        minimize (bool): `True` to minimize PSCAD to an icon.

        splash (bool): `False` to disable the startup splash/logo window.

        timeout (int): Time (seconds) to wait for the connection to be
            accepted.

        version (str): Specific version to launch if multiple versions present.

        x64 (bool): `True` for 64-bit version, `False` for 32-bit version.

        settings (dict): Setting values to set immediately upon startup.

        load_user_profile (bool): Set to False to disable loading user profile.

        minimum (str): Minimum allowed PSCAD version to run (default '5.0')

        maximum (str): Maximum allowed PSCAD version to run (default: unlimited)

        load (list[str]): Projects & libraries, or workspace to load at startup

        extra_args (list[str]): Additional command-line arguments

        address (str): Interface address to bind PSCAD's automation server on

        **options: Additional keyword=value options

    Returns:
        PSCAD: The PSCAD application proxy object

    Example::

        import mhi.pscad
        pscad = mhi.pscad.launch(load='myproject.pscx')

    .. versionchanged:: 2.4
        added `extra_args` parameter.
    .. versionchanged:: 2.8.4
        added `load` parameter.
    .. versionchanged:: 2.9.6
        ``allow_alpha``, ``allow_beta`` parameters are no longer supported.
    .. versionchanged:: 3.0.2
        added `address` parameter.
    .. versionchanged:: 3.0.5
        ``allow_beta`` parameter is supported again.
    """

    if allow_alpha is not None:
        warn("allow_alpha is no longer supported and will be removed",
             DeprecationWarning, stacklevel=2)

    hidden_arg_names = {'debug', 'startup', 'exe', 'edition'}
    unknown = options.keys() - hidden_arg_names
    if unknown:
        raise ValueError(f"Unknown arguments: {', '.join(unknown)}")


    from mhi.common import process # pylint: disable=import-outside-toplevel

    options = ChainMap(options, OPTIONS, {'startup': 'au'}) # type: ignore[assignment]

    args = ["{exe}", "/startup:{startup}", "/port:{port}"]

    if 'edition' in options:
        edition = options['edition']
        if edition not in {'PRO', 'EDU', 'DCLK'}:
            raise ValueError(f"Invalid edition: {edition!r}")
        args.append(edition)

    if address is not None:
        args.append(f"/address:{address}")

    if splash is not None:
        args.append(f"/splash:{str(splash).lower()}")

    if load_user_profile is not None:
        args.append(f"/load-user-profile:{load_user_profile}")

    if silence is not None:
        args.append(f"/silence:{str(silence).lower()}")

    if load:
        if isinstance(load, (Path, str)):
            load = [load]
        args.extend(map(os.path.abspath, load))

    if extra_args:
        if isinstance(extra_args, str):
            extra_args = [extra_args]
        args.extend(extra_args)

    if not options.get('exe', None):
        options['exe'] = process.find_exe('PSCAD', version, x64, minimum,
                                          maximum, allow_beta=allow_beta)
        if not options['exe']:
            raise ValueError("Unable to find required version")

    if not os.path.isfile(options['exe']):
        raise ValueError(f"No such executable: {options['exe']}")

    if port is None:
        port = options.get('port_range', None)
    if not port or isinstance(port, range):
        port = process.unused_tcp_port(port)
        _LOG.info("Automation server port: %d", port)

    process.launch(*args, port=port, minimize=minimize, **options)

    connect_opts = {'port': port, 'timeout': timeout}
    if address is not None:
        from socket import getaddrinfo # pylint: disable=import-outside-toplevel

        for addr_info in getaddrinfo(address, port):
            addr = addr_info[4][0]
            if addr not in {'0.0.0.0', '::'}:
                connect_opts['host'] = address

    app = connect(**connect_opts)

    # Wait for 1 or more startup tasks to start & finish.
    for _ in range(3):
        app.wait_for_idle()

    # Legacy launch keyword arguments:
    for key in ('certificate', 'fortran_version', 'matlab_version'):
        if key in options:
            if settings is None:
                settings = {}
            settings[key] = val = options[key]
            warnings.warn(
                f'Unsupported keyword parameter "{key}={val!r}".\n'
                f'Use "settings={{{key!r}: {val!r}}}" to specify value',
                DeprecationWarning, stacklevel=2)

    # First things first: if any settings have been given, set them.
    if settings:
        app.settings(**settings)

    app.wait_for_idle()

    return app


#===============================================================================
# PSCAD Versions
#===============================================================================

def versions() -> List[Tuple[str, bool]]:
    """
    Find the installed versions of PSCAD

    Returns:
        List[Tuple]: List of tuples of version and bit-size
    """

    from mhi.common import process # pylint: disable=import-outside-toplevel

    return process.versions('PSCAD')


#===============================================================================
# Fortran/Matlab Versions
#===============================================================================

def _product_list():
    if 'cache' not in _product_list.__dict__:

        product_list = defaultdict(dict)
        for paramlist_name in ('pscad', 'fortran', 'matlab'):
            product_list[paramlist_name] = {}

        folder = Path(os.path.expandvars(r"%PUBLIC%\Documents"))
        if not folder.is_dir():
            folder = shell_folder("Common Documents")

        if folder.is_dir():

            file = folder / r"Manitoba HVDC Research Centre\ATS\ProductList.xml"

            if file.is_file():
                doc = _ET.parse(file)
                root = doc.getroot()
                for paramlist in root:
                    paramlist_name = paramlist.get('name')
                    params = product_list[paramlist_name]

                    for param in paramlist:
                        name = param.get('name')
                        value = param.get('value', '')
                        params[name] = value
            else:
                warnings.warn(f"Not found: '{file}'", stacklevel=3)

        else:
            warnings.warn(r"Unable to find '%PUBLIC%\Documents' or "
                          "'Common Documents' folder", stacklevel=3)

        _product_list.cache = dict(product_list)

    return _product_list.cache


def fortran_versions() -> List[str]:
    """
    Find the installed versions of Fortran

    Returns:
        List[str]: List of Fortran versions
    """

    return list(_product_list()['fortran'].keys())


def matlab_versions() -> List[str]:
    """
    Find the installed versions of Matlab

    Returns:
        List[str]: List of Matlab versions
    """

    return list(_product_list()['matlab'].keys())


def fortran_codec():
    """
    Coder/Decoder for FORTRAN version strings
    """

    return MapCodec(_product_list()['fortran'])


def matlab_codec():
    """
    Coder/Decoder for Matlab version strings
    """

    mapping = _product_list()['matlab']
    if not mapping:
        mapping = {'':''}
    return MapCodec(mapping)
