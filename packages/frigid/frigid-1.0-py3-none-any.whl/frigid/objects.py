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
''' Immutable objects.

    Provides a base class and decorator for creating objects with immutable
    attributes. Once an object is initialized, its attributes cannot be modified
    or deleted.

    The implementation uses a special dictionary type for attribute storage that
    enforces immutability. This makes it suitable for:

    * Configuration objects
    * Value objects
    * Immutable data containers
    * Objects requiring attribute stability

    >>> from frigid import Object
    >>> class Point( Object ):
    ...     def __init__( self, x, y ):
    ...         self.x = x
    ...         self.y = y
    ...         super( ).__init__( )
    ...
    >>> obj = Point( 1, 2 )  # Initialize with attributes
    >>> obj.z = 3  # Attempt to add attribute
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'z'.
    >>> obj.x = 4  # Attempt modification
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'x'.
'''
# pylint: enable=line-too-long


from . import __


def _check_behavior( obj: object ) -> bool:
    behaviors: __.cabc.MutableSet[ str ]
    if _check_dict( obj ):
        attributes = getattr( obj, '__dict__' )
        behaviors = attributes.get( '_behaviors_', set( ) )
    else: behaviors = getattr( obj, '_behaviors_', set( ) )
    return __.behavior_label in behaviors


def _check_dict( obj: object ) -> bool:
    # Return False even if '__dict__' in '__slots__'.
    if hasattr( obj, '__slots__' ): return False
    return hasattr( obj, '__dict__' )


def immutable( class_: type[ __.C ] ) -> type[ __.C ]: # pylint: disable=too-complex
    ''' Decorator which makes class immutable after initialization.

        Cannot be applied to classes which define their own __setattr__
        or __delattr__ methods.
    '''
    for method in ( '__setattr__', '__delattr__' ):
        if method in class_.__dict__:
            from .exceptions import DecoratorCompatibilityError
            raise DecoratorCompatibilityError( class_.__name__, method )
    original_init = next(
        base.__dict__[ '__init__' ] for base in class_.__mro__
        if '__init__' in base.__dict__ ) # pylint: disable=magic-value-comparison

    def __init__(
        self: object, *posargs: __.a.Any, **nomargs: __.a.Any
    ) -> None:
        # TODO: Use accretive set for behaviors.
        original_init( self, *posargs, **nomargs )
        behaviors: __.cabc.MutableSet[ str ]
        if _check_dict( self ):
            attributes = getattr( self, '__dict__' )
            behaviors = attributes.get( '_behaviors_', set( ) )
            if not behaviors: attributes[ '_behaviors_' ] = behaviors
            setattr( self, '__dict__', __.ImmutableDictionary( attributes ) )
        else:
            behaviors = getattr( self, '_behaviors_', set( ) )
            if not behaviors: setattr( self, '_behaviors_', behaviors )
        behaviors.add( __.behavior_label )

    def __delattr__( self: object, name: str ) -> None:
        if _check_behavior( self ):
            from .exceptions import AttributeImmutabilityError
            raise AttributeImmutabilityError( name )
        super( class_, self ).__delattr__( name )

    def __setattr__( self: object, name: str, value: __.a.Any ) -> None:
        if _check_behavior( self ):
            from .exceptions import AttributeImmutabilityError
            raise AttributeImmutabilityError( name )
        super( class_, self ).__setattr__( name, value )

    class_.__init__ = __init__
    class_.__delattr__ = __delattr__
    class_.__setattr__ = __setattr__
    return class_


@immutable
class Object:
    ''' Immutable objects. '''

    __slots__ = ( '__dict__', '_behaviors_' )

Object.__doc__ = __.generate_docstring(
    Object, 'instance attributes immutability' )
