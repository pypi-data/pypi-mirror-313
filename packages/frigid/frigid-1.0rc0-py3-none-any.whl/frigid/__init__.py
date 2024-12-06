# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Immutable data structures. '''

# ruff: noqa: F401,F403


from . import __
from . import classes
from . import dictionaries
from . import exceptions
from . import modules
from . import namespaces
from . import objects
from . import qaliases

from .classes import *
from .dictionaries import *
from .modules import *
from .namespaces import *
from .objects import *


__version__ = '1.0rc0'


_attribute_visibility_includes_ = frozenset( ( '__version__', ) )

class _InternalModule( __.InternalObject, __.Module ): pass # type: ignore
def _reclassify_modules(
    attributes: __.cabc.Mapping[ str, __.a.Any ]
) -> None:
    from inspect import ismodule
    for attribute in attributes.values( ):
        if not ismodule( attribute ): continue
        if isinstance( attribute, _InternalModule ):
            continue # pragma: no coverage
        attribute.__class__ = _InternalModule

_reclassify_modules( globals( ) )
__.modules[ __name__ ].__class__ = _InternalModule
