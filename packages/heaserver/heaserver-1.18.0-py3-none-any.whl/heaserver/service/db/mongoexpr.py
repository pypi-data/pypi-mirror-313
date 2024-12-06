"""Provides a function for creating mockmongo query expressions from HEA REST API parameters.
"""
from heaobject import user
from aiohttp.web import Request
from typing import cast, Any
from collections.abc import Sequence, Mapping
import logging
from copy import deepcopy, copy


def mongo_expr(request: Request | None, var_parts: str | Sequence[str] | None,
               mongoattributes: str | Sequence[str] | Mapping[str, Any] | None = None,
               extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """
    Create and returns a mockmongo query expression representing filter criteria.

    1. If mongoattributes is a string, then mongoattributes is treated as a mockmongo field name, and var_parts is
    expected to be the name of a variable in the request's match_info with the desired value of the field name.

    2. If var_parts is a string and mongoattributes is not specified or None, the value of var_parts is treated as a
    mongo field name, and it is also the name of a variable in the request's match_info with the desired value of the
    field name.

    3. If mongoattributes is a Mapping, then it is treated as a mockmongo query expression, and the value of var_parts
    is ignored.

    4. If mongoattributes is a Sequence of strings, then it is treated as an array of mockmongo field names, and var_parts
    is expected to be a Sequence of aiohttp match_info strings with the desired values of the corresponding field names
    in mongoattributes.

    If var_parts is a Sequence of strings and mongoattributes is unspecified or None, then it is treated as both an
    iterable of mockmongo field names and corresponding aiohttp dynamic resource variable parts with the desired values of
    the corresponding field names.

    If mongoattributes or var_parts are specified but neither is a Mapping, a Sequence of strings nor a string, a
    TypeError will be raised.

    5. If mongoattributes and var_parts are both unspecified or None, an empty mockmongo query expression is created.

    If extra is a Mapping, it will be merged with the query expression dict above, overriding any overlapping parts of
    the expression. If extra is not None and is not a Mapping, a TypeError will be raised.

    The resulting query expression is returned.

    :param request: the aiohttp request. Required if var_parts is used.
    :param var_parts: the names of the dynamic resource's variable parts.
    :param mongoattributes: the attribute(s) to filter by, or a mockmongo query expression.
    :param extra: another mockmongo query expression.
    :return: a dict containing a mockmongo query expression.
    :raises TypeError: as described above.
    """
    logger = logging.getLogger(__name__)
    if isinstance(mongoattributes, str) and isinstance(var_parts, str):
        # 1 above
        if request is None:
            raise TypeError('request must be not None when var_parts is used')
        d: dict[str, Any] = {mongoattributes: request.match_info[var_parts]}
    elif not mongoattributes and isinstance(var_parts, str):
        # 2 above
        if request is None:
            raise TypeError('request must be not None when var_parts is used')
        d = {var_parts: request.match_info[var_parts]}
    elif isinstance(mongoattributes, Mapping):
        # 3 above
        d = dict(deepcopy(mongoattributes))
    elif mongoattributes or var_parts:
        # 4 above
        if var_parts is None:
            raise ValueError('var_parts cannot be None in this situation')
        if isinstance(var_parts, str):
            raise TypeError('var_parts cannot be a str in this situation')
        if mongoattributes is not None and isinstance(mongoattributes, str):
            raise TypeError('mongoattributes cannot be a str in this situation')
        if request is None:
            raise ValueError('request must be not None when var_parts is used')
        d = {nm: request.match_info[var_parts[idx]]
             for idx, nm in enumerate(mongoattributes if mongoattributes else var_parts)}
    else:
        # 5 above
        d = {}
    if extra:
        extra_ = dict(deepcopy(extra))
        if '$or' in extra_ and '$or' in d:
            if '$and' not in d:
                d.update({'$and': [{'$or': extra_.pop('$or')}, {'$or': d.pop('$or')}]})
            else:
                d['$and'].append({'$or': extra_.pop('$or')})
        if '$and' in extra_ and '$and' in d:
            d['$and'].extend(extra_.pop('$and'))
        d.update(extra_)
    logger.debug('Mongo expression is %s', d)
    return d


def sub_filter_expr(sub: str | None, permissions: Sequence[str] | None = None) -> dict[str, Any] | None:
    """
    Returns mongodb expression that filters results by user and permissions.

    :param sub: the user to filter by.
    :param permissions: the permissions to filter by. If None or empty, permissions are not checked.
    :return: a dict.
    """
    return {'$or': [{'owner': sub},
                    {'shares': {
                        '$elemMatch': {
                            'user': {'$in': _matching_users(sub)}
                        } if not permissions else {
                            'user': {'$in': _matching_users(sub)}, 'permissions': {'$elemMatch': {'$in': permissions}}
                        }
                    }}]
            } if sub else None


def _matching_users(sub: str) -> list[str]:
    """
    Returns a list containing the provided user and generic system users.

    :param sub: the user.
    :return: a list of users.
    """
    return [sub, user.ALL_USERS]

