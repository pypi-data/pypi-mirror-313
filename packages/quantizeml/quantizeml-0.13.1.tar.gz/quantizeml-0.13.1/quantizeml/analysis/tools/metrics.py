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
__all__ = ["SMAPE", "Saturation", "print_metric_table"]

from collections import defaultdict
import warnings
import numpy as np
import keras


class SMAPE(keras.metrics.Metric):
    """Compute the Symmetric Mean Absolute Percentage Error (SMAPE) as:

    >>> mean(abs(x - y) / (abs(x) + abs(y)))

    Reference: https://en.wikipedia.org/wiki/Symmetric_mean_absolute_percentage_error

    Args:
        name (str, optional): name of the metric. Defaults to "smape".
    """

    def __init__(self, name="smape", **kwargs):
        super().__init__(name=name, **kwargs)
        self.error = self.add_weight(name='error', initializer='zeros', dtype="float64")
        self.count = self.add_weight(name='count', initializer='zeros', dtype="float64")

    def update_state(self, y_true, y_pred):
        assert y_true.shape == y_pred.shape
        total = y_true.size

        # Skip values that undefine the metric
        mask = (y_true == 0) & (y_pred == 0)
        y_true = y_true[~mask]
        y_pred = y_pred[~mask]

        # Compute smape
        smape = np.sum(np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred)))
        self.error.assign_add(smape)

        # Update the metric count.
        # Note here we take into account the set of values y_true = y_pred = 0,
        # since the error they contribute is zero.
        self.count.assign_add(total)

    def result(self):
        if self.count == 0:
            return 0.0
        return self.error / self.count

    def reset_states(self):
        self.error.assign(0.0)
        self.count.assign(0.0)


class Saturation(keras.metrics.Metric):
    """Returns the percentage of saturating values.

    We consider a value saturated if it is one of {min_value, max_value}

    Args:
        min_value (np.ndarray, optional): the minimum of values.
            If not provided, it is inferred from the values type. Defaults to None.
        max_value (np.ndarray, optional): the maximum of values.
            If not provided, it is inferred from the values type. Defaults to None.
    """

    def __init__(self, name="saturation", min_value=None, max_value=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self._min_value = min_value
        self._max_value = max_value
        self.total = self.add_weight(name='total', initializer='zeros', dtype="int64")
        self.count = self.add_weight(name='count', initializer='zeros', dtype="int64")

    @property
    def min_value(self):
        if self._min_value is None:
            iinfo = np.iinfo(self.dtype) if np.issubdtype(self.dtype, np.integer) else None
            assert iinfo, f"Unknown minimum value for data type {self.dtype}"
            return iinfo.min
        return self._min_value

    @property
    def max_value(self):
        if self._max_value is None:
            iinfo = np.iinfo(self.dtype) if np.issubdtype(self.dtype, np.integer) else None
            assert iinfo, f"Unknown maximum value for data type {self.dtype}"
            return iinfo.max
        return self._max_value

    def update_state(self, values):
        if np.any(values > self.max_value) or np.any(values < self.min_value):
            warnings.warn(f"Saturation is not accurate: there are values outside of range "
                          f"[{self.min_value}, {self.max_value}].")
        sat_values = np.sum((values == self.min_value) | (values == self.max_value))
        self.total.assign_add(sat_values)
        self.count.assign_add(values.size)

    def result(self):
        count = self.count if self.count != 0 else 1
        return 100 * (self.total / count)

    def reset_states(self):
        self.total.assign(0)
        self.count.assign(0)

    def get_config(self):
        config = super().get_config()
        config.update({"min_value": self._min_value, "max_value": self._max_value})
        return config


def print_metric_table(summary, model_name=""):
    """Print a table with the results of a set of metrics.

    The following format is expected:

    .. code-block::

        # Format for metrics
        # 1. Simple set of metrics
        metrics_for_key_1 = {"metric_1": key1_metric1_value, "metric_2": key1_metric2_value}
        # 2. List of simple set of metrics
        metrics_for_key_2 = [{"metric_1": key2_metric1_value1, "metric_2": key2_metric2_value1},
                             {"metric_1": key2_metric1_value2, "metric_2": key2_metric2_value2}]
        # 3. List of complex set of metrics
        metrics_for_key_3 = [metrics_for_key_2, metrics_for_key_2]

        # Summary
        summary = {
            "key_1": metrics_for_key_1,
            "key_2": metrics_for_key_2,
            "key_3": metrics_for_key_3,
        }

    Args:
        summary (dict): summary of metrics to draw
        model_name (str, optional): A model name to display. Defaults to "".

    Note:
        All metrics must contain the same set of measures
    """
    FLOAT_PRECISION = 4
    saturate = False

    def _flat_measures(summary):
        nonlocal saturate
        new_summary = {}
        for name, measures in summary.items():
            if isinstance(measures, (list, tuple)):
                new_el = _flat_measures({f"{name}:{idx+1}": v for idx, v in enumerate(measures)})
            else:
                assert isinstance(measures, dict), f"Wrong measurement format for {name}."
                # Check if saturation is higher than 60 %
                saturated_layer = measures.get("Saturation (%)", 0.0) > 60
                new_el = {("*" if saturated_layer else "") + name: measures}
                saturate |= saturated_layer
            new_summary.update(new_el)
        return new_summary

    def _find_max_length(summary):
        max_key_len = defaultdict(int)
        for values in summary.values():
            for key, val in values.items():
                # Variable length is given by: integer part + '.' + float precision
                var_len = len(str(val).split('.')[0]) + 1 + FLOAT_PRECISION
                # Take into account length of key
                max_key_len[key] = max(max_key_len[key], var_len, len(key))
        return max_key_len

    summary = _flat_measures(summary)
    # Compute lengths per column
    title_names = "Layer/node"
    max_name_len = max(*(len(x) for x in summary), len(title_names))
    max_len_per_key = _find_max_length(summary)

    # Print head
    title_measures_cols = " | ".join([k.ljust(v) for k, v in max_len_per_key.items()])
    title_cols = title_names.ljust(max_name_len) + " | " + title_measures_cols
    total_table_len = len(title_cols)
    print(f"\nQuantization error for {model_name}:\n" + "=" * total_table_len)
    print(title_cols + "\n" + "=" * total_table_len, end="")

    # Print measures
    for name, measures in summary.items():
        print("\n" + name.ljust(max_name_len), end="")
        for key, just_len in max_len_per_key.items():
            if key not in measures:
                raise KeyError(f"'{name}' does not contain '{key}' in measures.")
            str_measure = ("{:." + str(FLOAT_PRECISION) + "f}").format(measures[key])
            print(" | " + str_measure.ljust(just_len), end="")
    print("\n" + "=" * total_table_len)

    # Print footer
    if saturate:
        print("* Measurement results are not reliable, as outputs saturate by more than 60%")
