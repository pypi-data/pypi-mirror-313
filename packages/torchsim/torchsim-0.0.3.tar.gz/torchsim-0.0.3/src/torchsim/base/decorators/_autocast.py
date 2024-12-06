"""Automatic torch converter."""

__all__ = ["autocast"]

import inspect

from functools import wraps
from typing import Callable

import torch

from mrinufft._array_compat import _to_torch, _get_leading_argument, _get_device


def autocast(func: Callable) -> Callable:
    """
    Force all inputs to be torch tensors of the same size on the same device.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        args, kwargs = _fill_kwargs(func, args, kwargs)

        # convert arrays to torch
        args, kwargs = _to_torch(*args, **kwargs)

        # convert remaining objects to torch
        args, kwargs = _to_tensors(*args, **kwargs)

        # enforce float32 for floating point tensors
        args, kwargs = _enforce_precision(*args, **kwargs)

        # get device from first positional or keyworded argument
        leading_arg = _get_leading_argument(args, kwargs)

        # get array module from leading argument
        device = _get_device(leading_arg)

        # move everything to the leading argument device
        args, kwargs = _to_device(device, *args, **kwargs)

        # run function
        return func(*args, **kwargs)

    return wrapper


# %% subroutines
def _fill_kwargs(func, args, kwargs):
    """This automatically fills missing kwargs with default values."""
    signature = inspect.signature(func)

    # Get number of arguments
    n_args = len(args)

    # Create a dictionary of keyword arguments and their default values
    _kwargs = {}
    for k, v in signature.parameters.items():
        if v.default is not inspect.Parameter.empty:
            _kwargs[k] = v.default
        else:
            _kwargs[k] = None

    # Merge the default keyword arguments with the provided kwargs
    for k in kwargs.keys():
        _kwargs[k] = kwargs[k]

    # Replace args
    _keys = list(_kwargs.keys())[n_args:]
    _values = list(_kwargs.values())[n_args:]

    return args, dict(zip(_keys, _values))


def _enforce_precision(*args, **kwargs):
    """Enforce tensors precision."""
    args = list(args)
    for n in range(len(args)):
        if isinstance(args[n], torch.Tensor) and torch.is_floating_point(args[n]):
            args[n] = args[n].to(torch.float32)

    # convert keyworded
    if kwargs:
        process_kwargs_vals, _ = _to_tensors(*kwargs.values())
        kwargs = {k: v for k, v in zip(kwargs.keys(), process_kwargs_vals)}

    return args, kwargs


def _to_tensors(*args, **kwargs):
    """Enforce tensors."""
    args = list(args)
    for n in range(len(args)):
        try:
            args[n] = torch.as_tensor(args[n])
        except Exception:
            pass

    # convert keyworded
    if kwargs:
        process_kwargs_vals, _ = _to_tensors(*kwargs.values())
        kwargs = {k: v for k, v in zip(kwargs.keys(), process_kwargs_vals)}

    return args, kwargs


def _to_device(device, *args, **kwargs):
    """Enforce same device."""
    for arg in args:
        try:
            arg = arg.to(device)
        except Exception:
            pass

    # convert keyworded
    if kwargs:
        process_kwargs_vals, _ = _to_device(device, *kwargs.values())
        kwargs = {k: v for k, v in zip(kwargs.keys(), process_kwargs_vals)}

    return args, kwargs
