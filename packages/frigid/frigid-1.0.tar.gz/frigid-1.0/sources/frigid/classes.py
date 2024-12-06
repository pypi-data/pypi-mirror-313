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


# pylint: disable=line-too-long
''' Immutable classes.

    Provides metaclasses for creating classes with immutable attributes. Once a
    class is initialized, its attributes cannot be reassigned or deleted.

    The implementation includes:

    * ``Class``: Standard metaclass for immutable classes; derived from
      :py:class:`type`.
    * ``ABCFactory``: Metaclass for abstract base classes; derived from
      :py:class:`abc.ABCMeta`.
    * ``ProtocolClass``: Metaclass for protocol classes; derived from
      :py:class:`typing.Protocol`.

    These metaclasses are particularly useful for:

    * Creating classes with constant class attributes
    * Defining stable abstract base classes
    * Building protocol classes with fixed interfaces

    >>> from frigid import Class
    >>> class Example( metaclass = Class ):
    ...     x = 1
    >>> Example.y = 2  # Attempt assignment
    Traceback (most recent call last):
        ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'y'.
    >>> Example.x = 3  # Attempt reassignment
    Traceback (most recent call last):
        ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'x'.
'''
# pylint: enable=line-too-long


from __future__ import annotations

from . import __


ClassDecorators: __.a.TypeAlias = (
    __.cabc.Iterable[ __.cabc.Callable[ [ type ], type ] ] )


_behavior = 'immutability'


class Class( type ):
    ''' Immutable class factory. '''

    def __new__(  # pylint: disable=too-many-arguments
        factory: type[ type ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.a.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: __.Optional[ __.a.Nullable[ str ] ] = __.absent,
        **args: __.a.Any
    ) -> Class:
        class_ = type.__new__(
            factory, name, bases, namespace, **args )
        return _class__new__(  # type: ignore
            class_, decorators = decorators, docstring = docstring )

    def __init__( selfclass, *posargs: __.a.Any, **nomargs: __.a.Any ):
        super( ).__init__( *posargs, **nomargs )
        _class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.a.Any ) -> None:
        if not _class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

Class.__doc__ = __.generate_docstring(
    Class,
    'description of class factory class',
    'class attributes immutability'
)


class ABCFactory( __.ABCFactory ):  # type: ignore
    ''' Immutable abstract base class factory. '''

    def __new__(  # pylint: disable=too-many-arguments
        factory: type[ type ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.a.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: __.Optional[ __.a.Nullable[ str ] ] = __.absent,
        **args: __.a.Any
    ) -> ABCFactory:
        class_ = __.ABCFactory.__new__(
            factory, name, bases, namespace, **args )
        return _class__new__(  # type: ignore
            class_, decorators = decorators, docstring = docstring )

    def __init__( selfclass, *posargs: __.a.Any, **nomargs: __.a.Any ):
        super( ).__init__( *posargs, **nomargs )
        _class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.a.Any ) -> None:
        if not _class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

ABCFactory.__doc__ = __.generate_docstring(
    ABCFactory,
    'description of class factory class',
    'class attributes immutability'
)


# pylint: disable=bad-classmethod-argument,no-self-argument
class ProtocolClass( type( __.a.Protocol ) ):
    ''' Immutable protocol class factory. '''

    def __new__(  # pylint: disable=too-many-arguments
        factory: type[ type ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.a.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: __.Optional[ __.a.Nullable[ str ] ] = __.absent,
        **args: __.a.Any
    ) -> ProtocolClass:
        class_ = __.a.Protocol.__class__.__new__(  # type: ignore
            factory, name, bases, namespace, **args )  # type: ignore
        return _class__new__(
            class_,  # type: ignore
            decorators = decorators, docstring = docstring )

    def __init__( selfclass, *posargs: __.a.Any, **nomargs: __.a.Any ):
        super( ).__init__( *posargs, **nomargs )
        _class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.a.Any ) -> None:
        if not _class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )
# pylint: enable=bad-classmethod-argument,no-self-argument

ProtocolClass.__doc__ = __.generate_docstring(
    ProtocolClass,
    'description of class factory class',
    'class attributes immutability'
)


def _class__new__(
    original: type,
    decorators: ClassDecorators = ( ),
    docstring: __.Optional[ __.a.Nullable[ str ] ] = __.absent,
) -> type:
    # Handle decorators similar to accretive implementation.
    # Some decorators create new classes, which invokes this method again.
    # Short-circuit to prevent recursive decoration and other tangles.
    class_decorators_ = original.__dict__.get( '_class_decorators_', [ ] )
    if class_decorators_: return original
    if not __.is_absent( docstring ): original.__doc__ = docstring
    setattr( original, '_class_decorators_', class_decorators_ )
    reproduction = original
    for decorator in decorators:
        class_decorators_.append( decorator )
        reproduction = decorator( original )
        if original is not reproduction:
            __.repair_class_reproduction( original, reproduction )
        original = reproduction
    class_decorators_.clear( )  # Flag '__init__' to enable immutability
    return reproduction


def _class__init__( class_: type ) -> None:
    # Some metaclasses add class attributes in '__init__' method.
    # So, we wait until last possible moment to set immutability.
    if class_.__dict__.get( '_class_decorators_' ): return
    del class_._class_decorators_
    if ( class_behaviors := class_.__dict__.get( '_class_behaviors_' ) ):
        class_behaviors.add( _behavior )
    else: setattr( class_, '_class_behaviors_', { _behavior } )


def _class__delattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore immutable base classes.
    if _behavior not in class_.__dict__.get( '_class_behaviors_', ( ) ):
        return False
    from .exceptions import AttributeImmutabilityError
    raise AttributeImmutabilityError( name )


def _class__setattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore immutable base classes.
    if _behavior not in class_.__dict__.get( '_class_behaviors_', ( ) ):
        return False
    from .exceptions import AttributeImmutabilityError
    raise AttributeImmutabilityError( name )
