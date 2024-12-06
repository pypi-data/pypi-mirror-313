"""
Convenience functions for handling HEAObjects.
"""

from . import client
from .representor import factory as representor_factory
from .representor.error import ParseException
from heaobject.root import HEAObject, DesktopObjectTypeVar, DesktopObjectDict, DesktopObject, desktop_object_type_for_name, Permission, DefaultPermissionGroup, PermissionContext, DesktopObjectTypeVar_contra
from heaobject.error import DeserializeException
from heaobject.registry import Component
from heaobject.user import ALL_USERS
from heaserver.service.oidcclaimhdrs import SUB
from aiohttp import web
import logging
from typing import Union, Optional, Type, Generic
from collections.abc import Sequence, Mapping, AsyncGenerator
from yarl import URL
from enum import Enum


class EnumWithAttrs(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class RESTPermissionGroup(EnumWithAttrs):
    """
    Enum that maps heaobject's root.Permission enum values to get, post, put, and delete REST API calls. These are
    aliases to the heaobject package's heaobject.root.PermissionGroup enum.

    In order to execute a GET request for an object, the user must have at least one of the permissions in the
    GETTER_PERMS permission group (VIEWER, COOWNER, or EDITOR) for the object. GETTER_PERMS is an alias to heaobject's
    ACCESSOR_PERMS.

    In order to execute a POST request to create an object, the user must have at least one of the permissions in the
    POSTER_PERMS permission group (CREATOR, COOWNER) for the container in which the object will be created.
    POSTER_PERMS is an alias to heaobject's CREATOR_PERMS.

    In order to execute a PUT request to update an object, the user must have at least one of the permissions in the
    PUTTER_PERMS permission group (EDITOR, COOWNER) for the object. PUTTER_PERMS is an alias to heaobject's
    UPDATER_PERMS.

    In order to execute a DELETE request to delete an object, the user must have at least one of the permissions in the
    DELETER_PERMS permission group (DELETER, COOWNER) for the object. DELETER_PERMS is an alias to heaobject's
    DETETER_PERMS.
    """

    def __init__(self, perms):
        self.__perms = perms

    @property
    def perms(self) -> list[Permission]:
        """
        The permissions that are part of the group.
        """
        return self.__perms[:-1]

    @property
    def _perms_internal(self) -> list[Permission]:
        """
        A representation of a group's permissions intended for incorporating into a database query. In addition to
        the documented permissions, this list also includes a special permission, Permission.CHECK_DYNAMIC, that if
        present in a desktop object's shares for the current user, will always return that object from the database
        and check it with the desktop object's dynamic_permission() method for whether the user has permissions for it.

        This attribute is prefixed with an underscore to indicate that it should only be used for the above purpose.
        Importantly, NEVER compare this list to those in a desktop object's shares for the purpose of deciding whether
        to grant a user permission to access a desktop object. Instead use the object's has_permissions() method or
        heaobjectsupport's has_permissions() function, both of which properly handle the Permission.CHECK_DYNAMIC
        special permission. Or, for simple permissions comparisons, use this enum's perms attribute, provided that you
        are not interested in using the desktop object's dynamic_permission() method to check permissions.
        """
        return list(self.__perms)

    GETTER_PERMS = DefaultPermissionGroup.ACCESSOR_PERMS._perms_internal
    PUTTER_PERMS = DefaultPermissionGroup.UPDATER_PERMS._perms_internal
    POSTER_PERMS = DefaultPermissionGroup.CREATOR_PERMS._perms_internal
    DELETER_PERMS = DefaultPermissionGroup.DELETER_PERMS._perms_internal


async def new_heaobject_from_type_name(request: web.Request, type_name: str) -> DesktopObject:
    """
    Creates a new HEA desktop object of the given type and populates its
    attributes from the body of a HTTP request. The form field names are
    assumed to correspond to attributes of the desktop object, and the
    attributes are set to the values in the form in order of appearance in the
    request. If the object's owner is None or no owner property was provided,
    the owner is set to the current user.

    :param request: the HTTP request.
    :param type_name: the type name of DesktopObject.
    :return: an instance of the given DesktopObject type. It is compared to the
    type of the HEA desktop object in the request body, and a
    DeserializeException is raised if the type of the HEA object is not an
    instance of this type. If the desktop object in the body has no type
    attribute, a DeserializeException is raised.
    :return: an instance of the given DesktopObject type.
    :raises DeserializeException: if creating a HEA object from the request
    body's contents failed.
    """
    _logger = logging.getLogger(__name__)
    obj = desktop_object_type_for_name(type_name)()
    return await populate_heaobject(request, obj)


async def new_heaobject_from_type(request: web.Request, type_: Type[DesktopObjectTypeVar]) -> DesktopObjectTypeVar:
    """
    Creates a new HEA desktop object of the given type and populates its
    attributes from the body of a HTTP request. The form field names are
    assumed to correspond to attributes of the desktop object, and the
    attributes are set to the values in the form in order of appearance in the
    request. If the object's owner is None or no owner property was provided,
    the owner is set to the current user.

    :param request: the HTTP request.
    :param type_: A DesktopObject type. It is compared to the type of the HEA
    desktop object in the request body, and a DeserializeException is raised if
    the type of the HEA object is not an instance of this type. If the desktop
    object in the body has no type attribute, a DeserializeException is raised.
    :return: an instance of the given DesktopObject type.
    :raises DeserializeException: if creating a HEA object from the request
    body's contents failed.
    """
    _logger = logging.getLogger(__name__)
    try:
        representor = representor_factory.from_content_type_header(request.headers['Content-Type'])
        _logger.debug('Using %s input parser', representor)
        result = await representor.parse(request)
        _logger.debug('Got dict %s', result)
        if 'type' not in result:
            raise KeyError("'type' not specified in request body. All types must be specified explicitly in the "
                           "body of the request.")
        actual_type = desktop_object_type_for_name(result['type'])
        if not issubclass(actual_type, type_):
            raise TypeError(f'Type of object in request body must be type {type_} but was {actual_type}')
        if result.get('owner', None) is None:
            result['owner'] = request.headers.get(SUB, None)
        obj = actual_type()
        obj.from_dict(result)
        return obj
    except ParseException as e:
        raise DeserializeException(str(e)) from e
    except (ValueError, TypeError) as e:
        raise DeserializeException(str(e)) from e
    except KeyError as e:
        raise DeserializeException(str(e)) from e
    except Exception as e:
        raise DeserializeException(str(e)) from e


async def populate_heaobject(request: web.Request, obj: DesktopObjectTypeVar) -> DesktopObjectTypeVar:
    """
    Populate an HEA desktop object from a POST or PUT HTTP request.

    :param request: the HTTP request. Required.
    :param obj: the HEAObject instance. Required.
    :return: the populated object.
    :raises DeserializeException: if creating a HEA object from the request body's contents failed.
    """
    _logger = logging.getLogger(__name__)
    try:
        representor = representor_factory.from_content_type_header(request.headers['Content-Type'])
        _logger.debug('Using %s input parser', representor)
        result = await representor.parse(request)
        _logger.debug('Got dict %s', result)
        obj.from_dict(result)
        return obj
    except (ParseException, ValueError) as e:
        _logger.exception('Failed to parse %s%s', obj, e)
        raise DeserializeException from e
    except Exception as e:
        _logger.exception('Got exception %s', e)
        raise DeserializeException from e


async def type_to_resource_url(request: web.Request, type_or_type_name: Union[str, Type[DesktopObject]],
                               parameters: Optional[Mapping[str, Union[Sequence[Union[int, float, complex, str]], Mapping[str, Union[int, float, complex, str]], tuple[str, Union[int, float, complex, str]], int, float, complex, str]]] = None,
                               **kwargs: Union[Sequence[Union[int, float, complex, str]], Mapping[str, Union[int, float, complex, str]], tuple[str, Union[int, float, complex, str]], int, float, complex, str]) -> str:
    """
    Use the HEA registry service to get the resource URL for accessing HEA objects of the given type.

    :param request: the HTTP request. Required.
    :param type_or_type_name: the type or type name of HEA desktop object. Required.
    :param parameters: for resource URLs with a URI template, the template parameters.
    :return: the URL string.
    :raises ValueError: if no resource URL was found in the registry or there was a problem accesing the registry
    service.
    """
    result = await client.get_resource_url(request.app, type_or_type_name, client_session=None, parameters=parameters, **kwargs)
    if result is None:
        raise ValueError(f'No resource in the registry for type {type_or_type_name}')
    return result


async def get_dict(request: web.Request, id_: str, type_or_type_name: Union[str, Type[DesktopObject]],
                   headers: Optional[Mapping[str, str]] = None) -> Optional[DesktopObjectDict]:
    """
    Gets the HEA desktop object dict with the provided id from the service for the given type, file system type,
    and file system name.

    :param request: the aiohttp request (required).
    :param id_: the id of the HEA desktop object of interest.
    :param type_or_type_name: the desktop object type or type name.
    :param headers: optional HTTP headers to use.
    :return: the requested HEA desktop object dict, or None if not found.
    :raises ValueError: if no appropriate service was found or there was a problem accessing the registry service.
    """
    url = await type_to_resource_url(request, type_or_type_name=type_or_type_name)
    return await client.get_dict(request.app, URL(url) / id_, headers)


async def get(request: web.Request, id_: str, type_: Type[DesktopObjectTypeVar],
              headers: Optional[Mapping[str, str]] = None) -> Optional[DesktopObjectTypeVar]:
    """
    Gets the HEA desktop object with the provided id from the service for the given type, file system type, and file
    system name.

    :param request: the aiohttp request (required).
    :param id_: the id of the HEA desktop object of interest.
    :param type_: the desktop object type.
    :param headers: optional HTTP headers to use.
    :return: the requested HEA desktop object, or None if not found.
    :raises ValueError: if no appropriate service was found or there was a problem accessing the registry service.
    """
    url = await type_to_resource_url(request, type_or_type_name=type_)

    return await client.get(request.app, URL(url) / id_, type_, headers)


async def get_all(request: web.Request, type_: Type[DesktopObjectTypeVar],
                  headers: Optional[Mapping[str, str]] = None) -> AsyncGenerator[DesktopObjectTypeVar, None]:
    """
    Async generator for all HEA desktop objects from the service for the given type, file system type, and file system
    name.

    :param request: the aiohttp request (required).
    :param type_: the desktop object type.
    :param headers: optional HTTP headers to use.
    :return: an async generator with the requested desktop objects.
    :raises ValueError: if no appropriate service was found or there was a problem accessing the registry service.
    """
    url = await type_to_resource_url(request, type_or_type_name=type_)

    return client.get_all(request.app, url, type_, headers)


def desktop_object_type_or_type_name_to_type(type_or_type_name: str | type[DesktopObject], default_type: type[DesktopObject] | None = None) -> type[DesktopObject]:
    """
    Takes a variable that may contain either a DesktopObject type or type name, and return a type. If a type is passed
    in, and it is a subclass of DesktopObject, it will be returned as-is. If a type name is passed in, its corresponding
    type will be returned if the type is a subclass of DesktopObject.

    :param type_or_type_name: the type or type name. Required.
    :param default_type: what to return if type_or_type_name is None. If omitted, None is returned.
    """
    if default_type is not None and not issubclass(default_type, DesktopObject):
        raise TypeError('default_type is defined and not a DesktopObject')
    if isinstance(type_or_type_name, type):
        if not issubclass(type_or_type_name, DesktopObject):
            raise TypeError(f'type_or_type_name not a DesktopObject')
        if issubclass(type_or_type_name, DesktopObject):
            result_ = type_or_type_name
        else:
            raise TypeError('type_or_type_name not a DesktopObject')
    else:
        file_system_type_ = desktop_object_type_for_name(type_or_type_name)
        if not issubclass(file_system_type_, DesktopObject):
            raise TypeError(f'file_system_type_or_type_name is a {file_system_type_} not a DesktopObject')
        else:
            result_ = file_system_type_
    if result_ is None:
        return default_type
    else:
        return result_


def type_or_type_name_to_type(type_or_type_name: str | type[HEAObject], default_type: type[HEAObject] | None = None) -> type[HEAObject]:
    """
    Takes a variable that may contain either a HEAObject type or type name, and return a type. If a type is passed
    in, and it is a subclass of HEAObject, it will be returned as-is. If a type name is passed in, its corresponding
    type will be returned if the type is a subclass of HEAObject.

    :param type_or_type_name: the type or type name. Required.
    :param default_type: what to return if type_or_type_name is None. If omitted, None is returned.
    """
    if default_type is not None and not issubclass(default_type, HEAObject):
        raise TypeError('default_type is defined and not a HEAObject')
    if isinstance(type_or_type_name, type):
        if not issubclass(type_or_type_name, HEAObject):
            raise TypeError(f'type_or_type_name not a HEAObject')
        if issubclass(type_or_type_name, HEAObject):
            result_ = type_or_type_name
        else:
            raise TypeError('type_or_type_name not a HEAObject')
    else:
        file_system_type_ = desktop_object_type_for_name(type_or_type_name)
        if not issubclass(file_system_type_, HEAObject):
            raise TypeError(f'file_system_type_or_type_name is a {file_system_type_} not a HEAObject')
        else:
            result_ = file_system_type_
    if result_ is None:
        return default_type
    else:
        return result_


def display_name_for_multiple_objects(objs: Sequence[DesktopObject]) -> str:
    """
    Returns a user-friendly display name for multiple desktop objects. For one
    object, it will return just the object's display name.

    :param objs: a sequence of desktop objects
    :raises ValueError: if objs is None or an empty sequence.
    """
    if objs is None:
        raise ValueError('objs cannot be None')
    match len(objs):
        case 0:
            raise ValueError('No objects in objs')
        case 1:
            return objs[0].display_name
        case 2:
            return f'{objs[0].display_name} and 1 other object'
        case _:
            return f'{objs[0].display_name} and {len(objs) - 1} other objects'


class HEAServerPermissionContext(PermissionContext[DesktopObjectTypeVar_contra], Generic[DesktopObjectTypeVar_contra]):

    def __init__(self, sub: str, request: web.Request, **kwargs):
        super().__init__(sub, **kwargs)
        if request is None:
            raise ValueError('request cannot be None')
        self.__request = request

    @property
    def request(self) -> web.Request:
        return self.__request

    async def can_create(self, desktop_object_type: type[DesktopObjectTypeVar_contra]) -> bool:
        component = await client.get_component(self.request.app, Component)
        assert component is not None, 'component cannot be None'
        resource = component.get_resource(str(desktop_object_type))
        if resource is None:
            raise ValueError(f'Invalid desktop object type {desktop_object_type}')
        return resource.manages_creators and any(user in (self.sub, ALL_USERS) for user in resource.creator_users)
