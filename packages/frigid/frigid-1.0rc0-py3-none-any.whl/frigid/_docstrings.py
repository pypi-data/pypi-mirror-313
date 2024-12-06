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


''' Docstrings table for reuse across subpackages. '''


from types import MappingProxyType as _DictionaryProxy


TABLE: _DictionaryProxy[ str, str ] = _DictionaryProxy( {

    'class attributes immutability': '''
Prevents assignment or deletion of class attributes after class creation.
''',

    'description of class factory class': '''
Derived from :py:class:`type`, this is a metaclass. A metaclass is a class
factory class. I.e., it is a class that produces other classes as its
instances.
''',

    'description of module': '''
Derived from :py:class:`types.ModuleType`, this class is suitable for use as a
Python module class.
''',

    'description of namespace': '''
A namespace is an object, whose attributes can be determined from iterables and
keyword arguments, at initialization time. The string representation of the
namespace object reflects its current instance attributes. Modeled after
:py:class:`types.SimpleNamespace`.
''',

    'dictionary entries immutability': '''
Prevents addition, alteration, or removal of dictionary entries after creation.
''',

    'dictionary entries validation': '''
When an attempt to create a dictionary with entries, each entry is validated
against supplied criteria. If validation fails for any entry, then the
dictionary creation is rejected.
''',

    'instance attributes immutability': '''
Prevents assignment or deletion of instance attributes after instance creation.
''',

    'module attributes immutability': '''
Prevents assignment or deletion of module attributes after module creation.

This behavior helps ensure that module-level constants remain constant and that
module interfaces remain stable during runtime.
''',

} )
