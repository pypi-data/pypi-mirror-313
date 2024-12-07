#!/usr/bin/env python
# ******************************************************************************
# Copyright 2024 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
__all__ = ["make_fn_on_list", "make_fn_on_dict"]


def make_fn_on_list(func):
    """Decorator that handles list arguments to a function.

    Call the function recursively for each iterable-element in the arguments.
    Stops when the arguments are no longer a list.

    Note auxiliary key-arguments are propagated for each call with their value.

    Args:
        func (callable): function to call.
    """
    def wrapper_fn(*args, **kwargs):
        types = (list, tuple)
        if any(isinstance(x, types) for x in args):
            assert all(isinstance(x, types) for x in args), "All args must be a list or tuple"
            assert all(len(args[0]) == len(x) for x in args), "All args must have the same length"
            return [wrapper_fn(*new_args, **kwargs) for new_args in zip(*args)]
        return func(*args, **kwargs)
    return wrapper_fn


def make_fn_on_dict(func):
    """Decorator that handles dictionaries arguments to a function.

    Call the function recursively for each iterable-element in the arguments.
    Stops when the arguments are no longer a dictionnary.

    Note auxiliary key-arguments are propagated for each call with their value.

    Args:
        func (callable): function to call.
    """
    def wrapper_fn(*args, **kwargs):
        if any(isinstance(x, dict) for x in args):
            assert all(isinstance(x, dict) for x in args), "All args must be a dict"
            keys = args[0].keys()
            if not all(k in keys for x in args for k in x):
                raise KeyError("All args must have the same keys")
            return {k: wrapper_fn(*tuple(x[k] for x in args), **kwargs) for k in keys}
        return func(*args, **kwargs)
    return wrapper_fn
