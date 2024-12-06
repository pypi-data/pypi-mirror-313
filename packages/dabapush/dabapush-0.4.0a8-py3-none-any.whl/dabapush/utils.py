"""Utility functions for working with dictionaries and lists of dictionaries."""
from functools import reduce
from typing import Any, Dict, List


def flatten(thing: dict, namespace: str = None, sep: str = ".") -> dict:
    """Flattens a nested dictionary. The flattened keys are joined together with the
    specified seperator.
    `flatten` only traverses dicts, consequently `list` items are left as is.

    Example
    -------

    To flatten a nested dict:

    >>> not_nice = {'a': {'b': 'yuk'}}
    ... flatten(not_nice)
    {'a.b.': 'yuk'}

    Lists are not unpacked:

    >>> nested_list = {'a': {'b': 'yuk', 'c': [{'d': 'meh'}]}}
    ... flatten(nested_list)
    {'a.b': 'yuk', 'a.c': [{'d': 'meh'}]}

    Parameters
    ----------
    thing : dict
        Nested dict to flatten
    namespace : str
        namespace to preprepend to output key (default value = None)
    sep : str
        Seperator character to use (default value = '.')

    Returns
    -------
    type dict:
        the flattened dict

    """
    res = {}
    for key, item in thing.items():
        if isinstance(item, dict):
            res = {
                **res,
                **{
                    sep.join([namespace, k] if namespace is not None else [k]): v
                    for (k, v) in flatten(item, key).items()
                },
            }
        else:
            res[sep.join([namespace, key] if namespace is not None else [key])] = item
    return res


def safe_access(thing: Dict, path: List[str]):
    """Safely access deep values in a nested dict without risking running into a `KeyException`.
    If the specified key path is not present in the dict `safe_access` returns `None`.

    Parameters
    ----------
    thing : Dict
        A (possibly deeply nested) dictionary to retrieve values from.
    path : List[str]
        List of keys
    Returns
    -------
    any or None:
        Returns whichever value is at the leaf of the specified key path or None
        if no such value exists.
    """

    res = thing
    for attr in path:
        if isinstance(res, dict):
            res = res.get(attr, None)
        if res is None:
            break
    return res


def safe_write(thing: dict, path: List[str], key: str or None, value: any) -> dict:
    """Safely access deep values in a nested dict without risking running into a `KeyException`.
    If the specified key path is not present in the dict `safe_access` returns `None`.

    Parameters
    ----------
    thing : dict
        A (possibly deeply nested) dictionary to retrieve values from.
    path : List[str]
        List of keys
    key : str or None
        key to write to
    value : any
        value to write

    Returns
    -------
    any or None:
        Returns whichever value is at the leaf of the specified key path or None
        if no such value exists.
    """

    def packer(acc: dict, item: str):
        if item not in acc:
            acc[item] = {}
        return acc[item]

    if key is None:
        key = path.pop()

    d = reduce(packer, path, thing)
    d[key] = value
    return thing


def unpack(
    id: str, includes: List[Any], id_key: str  # pylint: disable=W0622
) -> Any or None:  # pylint: disable=W0622
    """Looks up an entity in a array of dicts by given key.

    Parameters
    ----------
    id : str
        Value to look for.
    includes : List[Any]
        List of dicts to look in.
    id_key : str
        Key of those dicts to look in.

    Returns
    -------

    """
    for included in includes:
        if id == included[id_key]:
            return included
    return None
