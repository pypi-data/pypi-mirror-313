import tabeline as tl

from .._labelset import LabelSet
from .nested_map import NestedMap
from .parameter import Parameter


def create_parameters_map(df: tl.DataFrame, parameter_label_columns: list[str]) -> dict[str, dict[str, Parameter]]:
    labels = LabelSet.from_df(df)  # This is necessary because labels need to be standardized

    param_map = NestedMap()

    for i, lb in enumerate(labels):
        param_map.set_value(
            # if the label does not exist it is wildcard.
            # Add the parameter column to the list of columns to be used as keys for the last layer and
            # it is guaranteed that it is not wildcard
            [lb.labels.get(k, "*") for k in [*parameter_label_columns, "parameter"]],
            {df[i, "parameter"]: Parameter(value=df[i, "value"], unit=df[i, "unit"])},
        )

    return param_map


def create_fitting_parameters_map(
    df: tl.DataFrame, parameter_label_columns: list[str]
) -> dict[str, dict[str, Parameter]]:
    labels = LabelSet.from_df(df)  # This is necessary because labels need to be standardized

    param_map = NestedMap()

    for i, lb in enumerate(labels):
        parameter_i = {
            "parameter": df[i, "parameter"],
            "value": df[i, "value"],
            "unit": df[i, "unit"],
            "is_fit": df[i, "is_fit"],
            "lower_bound": df[i, "lower_bound"],
            "upper_bound": df[i, "upper_bound"],
            "global_parameter_name": df[i, "global_parameter_name"],
        }

        if "prior_distribution" in df.column_names:
            parameter_i["prior_distribution"] = df[i, "prior_distribution"]
        if "location" in df.column_names:
            parameter_i["location"] = df[i, "location"]
        if "scale" in df.column_names:
            parameter_i["scale"] = df[i, "scale"]

        param_map.set_value(
            # if the label does not exist it is wildcard.
            # Add the parameter column to the list of columns to be used as keys for the last layer and
            # it is guaranteed that it is not wildcard
            [lb.labels.get(k, "*") for k in [*parameter_label_columns, "parameter"]],
            {df[i, "parameter"]: parameter_i},
        )

    return param_map


def create_doses_map(df: tl.DataFrame, dose_label_columns: list[str]) -> dict[str, dict[str, int]]:
    labels = LabelSet.from_df(df)  # This is necessary because labels need to be standardized
    dose_map = NestedMap()
    has_durations = "durations" in df.column_names

    for i, lb in enumerate(labels):
        schedule_i = {
            "route": df[i, "route"],
            "amounts": df[i, "amounts"],
            "amount_unit": df[i, "amount_unit"],
            "times": df[i, "times"],
            "time_unit": df[i, "time_unit"],
        }
        if has_durations:
            schedule_i.update({"durations": df[i, "durations"], "duration_unit": df[i, "duration_unit"]})
        # if the label does not exist it is wildcard.
        # Add the route column to the list of columns to be used as keys for the last layer and
        # it is guaranteed that it is not wildcard
        dose_map.set_value(
            [lb.labels.get(k, "*") for k in [*dose_label_columns, "route"]], {df[i, "route"]: schedule_i}
        )

    return dose_map


def create_models_map(df: tl.DataFrame, model_label_columns: list[str]) -> dict[str, dict[str, str]]:
    labels = LabelSet.from_df(df)  # This is necessary because labels need to be standardized
    model_map = NestedMap()

    for i, lb in enumerate(labels):
        # if the label does not exist it is wildcard.
        # Add the route column to the list of columns to be used as keys for the last layer and
        # it is guaranteed that it is not wildcard
        model_map.set_value(
            [lb.labels.get(k, "*") for k in [*model_label_columns, "model"]],
            {df[i, "model"]: {"model": df[i, "model"]}},
        )

    return model_map


def create_times_map(df: tl.DataFrame, time_label_columns: list[str]) -> dict[str, dict[str, str]]:
    labels = LabelSet.from_df(df)  # This is necessary because labels need to be standardized
    time_map = NestedMap()

    for i, lb in enumerate(labels):
        # if the label does not exist it is wildcard.
        # Add the index to the list of columns to be used as keys for the last layer
        # for times duplication is fine
        time_map.set_value(
            [lb.labels.get(k, "*") for k in time_label_columns] + [f"{i}"],
            {"times": df[i, "times"], "times_unit": df[i, "times_unit"]},
        )

    return time_map


def create_measurements_map(df: tl.DataFrame, measurement_label_columns: list[str]) -> dict[str, dict[str, str]]:
    labels = LabelSet.from_df(df)  # This is necessary because labels need to be standardized
    measurement_map = NestedMap()

    has_exponential_error = "exponential_error" in df.column_names
    has_constant_error = "constant_error" in df.column_names
    has_proportional_error = "proportional_error" in df.column_names

    for i, lb in enumerate(labels):
        measurement_i = {
            "time": df[i, "time"],
            "time_unit": df[i, "time_unit"],
            "output": df[i, "output"],
            "measurement": df[i, "measurement"],
            "measurement_unit": df[i, "measurement_unit"],
        }
        if has_exponential_error:
            measurement_i.update({"exponential_error": df[i, "exponential_error"]})
        if has_constant_error:
            measurement_i.update({"constant_error": df[i, "constant_error"]})
        if has_proportional_error:
            measurement_i.update({"proportional_error": df[i, "proportional_error"]})

        # if the label does not exist it is wildcard.
        # Add the index to the list of columns to be used as keys for the last layer
        # for measurements duplication is fine
        measurement_map.set_value([lb.labels.get(k, "*") for k in measurement_label_columns] + [f"{i}"], measurement_i)

    return measurement_map
