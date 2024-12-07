import copy
import datetime
import logging
from typing import Dict, List, Optional, Union

from databricks.ml_features.utils import utils
from databricks.ml_features_common.entities._feature_store_object import (
    _FeatureStoreObject,
)

_logger = logging.getLogger(__name__)


class FeatureLookup(_FeatureStoreObject):
    """
    .. note::

       Aliases: `!databricks.feature_engineering.entities.feature_lookup.FeatureLookup`, `!databricks.feature_store.entities.feature_lookup.FeatureLookup`

    Value class used to specify a feature to use in a :class:`TrainingSet <databricks.ml_features.training_set.TrainingSet>`.

    :param table_name: Feature table name.
    :param lookup_key: Key to use when joining this feature table with the :class:`DataFrame <pyspark.sql.DataFrame>` passed to
       :meth:`create_training_set() <databricks.feature_engineering.client.FeatureEngineeringClient.create_training_set>`. The ``lookup_key`` must be the columns
       in the DataFrame passed to :meth:`create_training_set() <databricks.feature_engineering.client.FeatureEngineeringClient.create_training_set>`. The type and order of
       ``lookup_key`` columns in that DataFrame must match the primary key of the
       feature table referenced in this :class:`FeatureLookup`.

    :param feature_names: A single feature name, a list of feature names, or None to lookup all features
        (excluding primary keys) in the feature table at the time that the training set is created.  If your model
        requires primary keys as features, you can declare them as independent FeatureLookups.
    :param rename_outputs: If provided, renames features in the :class:`TrainingSet <databricks.ml_features.training_set.TrainingSet>`
        returned by of :meth:`create_training_set() <databricks.feature_engineering.client.FeatureEngineeringClient.create_training_set>`.
    :param timestamp_lookup_key: Key to use when performing point-in-time lookup on this feature table
        with the :class:`DataFrame <pyspark.sql.DataFrame>` passed to :meth:`create_training_set() <databricks.feature_engineering.client.FeatureEngineeringClient.create_training_set>`.
        The ``timestamp_lookup_key`` must be the columns in the DataFrame passed to :meth:`create_training_set() <databricks.feature_engineering.client.FeatureEngineeringClient.create_training_set>`.
        The type of ``timestamp_lookup_key`` columns in that DataFrame must match the type of the timestamp key of the
        feature table referenced in this :class:`FeatureLookup`.

        .. note::
            Experimental: This argument may change or be removed in a future release without warning.

    :param lookback_window: The lookback window to use when performing point-in-time lookup on the feature table with
        the dataframe passed to :meth:`create_training_set() <databricks.feature_engineering.client.FeatureEngineeringClient.create_training_set>`. Feature Store will retrieve the latest
        feature value prior to the timestamp specified in the dataframe’s ``timestamp_lookup_key`` and within the
        ``lookback_window``, or null if no such feature value exists. When set to 0, only exact matches from the feature
        table are returned.

    :param feature_name: Feature name.  **Deprecated**. Use `feature_names`.
    :param output_name: If provided, rename this feature in the output of
       :meth:`create_training_set() <databricks.feature_engineering.client.FeatureEngineeringClient.create_training_set>`.
       **Deprecated**. Use `rename_outputs`.
    """

    def __init__(
        self,
        table_name: str,
        lookup_key: Union[str, List[str]],
        *,
        feature_names: Union[str, List[str], None] = None,
        rename_outputs: Optional[Dict[str, str]] = None,
        timestamp_lookup_key: Optional[str] = None,
        lookback_window: Optional[datetime.timedelta] = None,
        **kwargs,
    ):
        """Initialize a FeatureLookup object. See class documentation."""

        self._feature_name_deprecated = kwargs.pop("feature_name", None)
        self._output_name_deprecated = kwargs.pop("output_name", None)

        if kwargs:
            raise TypeError(
                f"FeatureLookup got unexpected keyword argument(s): {list(kwargs.keys())}"
            )

        self._table_name = table_name

        if type(timestamp_lookup_key) is list:
            if len(timestamp_lookup_key) == 0:
                timestamp_lookup_key = None
            elif len(timestamp_lookup_key) == 1:
                timestamp_lookup_key = timestamp_lookup_key[0]
            else:
                raise ValueError(
                    f"Setting multiple timestamp lookup keys is not supported."
                )

        if rename_outputs is not None and not isinstance(rename_outputs, dict):
            raise ValueError(
                f"Unexpected type for rename_outputs: {type(rename_outputs)}"
            )

        self._feature_names = utils.as_list(feature_names, default=[])

        # Make sure the user didn't accidentally pass in any nested lists/dicts in feature_names
        for fn in self._feature_names:
            if not isinstance(fn, str):
                raise ValueError(
                    f"Unexpected type for element in feature_names: {type(self._feature_names)}, only strings allowed in list"
                )

        if lookback_window is not None:
            if not timestamp_lookup_key:
                raise ValueError(
                    f"Unexpected lookback_window value: {lookback_window}, lookback windows can only be applied on time series "
                    f"feature tables. Use timestamp_lookup_key to perform point-in-time lookups with lookback window."
                )
            if not isinstance(
                lookback_window, datetime.timedelta
            ) or lookback_window < datetime.timedelta(0):
                raise ValueError(
                    f"Unexpected value for lookback_window: {lookback_window}, only non-negative datetime.timedelta allowed."
                )

        self._lookup_key = copy.copy(lookup_key)
        self._timestamp_lookup_key = copy.copy(timestamp_lookup_key)
        self._lookback_window = copy.copy(lookback_window)

        self._rename_outputs = {}
        if rename_outputs is not None:
            self._rename_outputs = rename_outputs.copy()

        self._inject_deprecated_feature_name()
        self._inject_deprecated_output_name()

    @property
    def table_name(self):
        """The table name to use in this FeatureLookup."""
        return self._table_name

    @property
    def lookup_key(self):
        """The lookup key(s) to use in this FeatureLookup."""
        return self._lookup_key

    @property
    def feature_name(self):
        """The feature name to use in this FeatureLookup. **Deprecated**. Use `feature_names`."""
        return self._feature_name_deprecated

    @property
    def feature_names(self):
        """The feature names to use in this FeatureLookup."""
        return self._feature_names

    @property
    def output_name(self):
        """The output name to use in this FeatureLookup. **Deprecated**. Use `feature_names`."""
        if self._output_name_deprecated:
            return self._output_name_deprecated
        else:
            return self._feature_name_deprecated

    @property
    def timestamp_lookup_key(self):
        return self._timestamp_lookup_key

    @property
    def lookback_window(self):
        """A lookback window applied only for point-in-time lookups."""
        return self._lookback_window

    def _get_feature_names(self):
        return self._feature_names

    def _get_output_name(self, feature_name):
        """Lookup the renamed output, or fallback to the feature name itself if no mapping is present"""
        return self._rename_outputs.get(feature_name, feature_name)

    def _inject_deprecated_feature_name(self):
        if self._feature_name_deprecated:
            if len(self._feature_names) > 0:
                raise ValueError(
                    "Use either feature_names or feature_name parameter, but not both."
                )
            _logger.warning(
                f'The feature_name parameter is deprecated. Use "feature_names".'
            )
            self._feature_names = [self._feature_name_deprecated]

    def _inject_deprecated_output_name(self):
        if len(self._feature_names) == 1 and self._output_name_deprecated:
            if len(self._rename_outputs) > 0:
                raise ValueError(
                    "Use either output_name or rename_outputs parameter, but not both."
                )
            _logger.warning(
                f'The output_name parameter is deprecated.  Use "rename_outputs".'
            )
            self._rename_outputs[self._feature_names[0]] = self._output_name_deprecated
