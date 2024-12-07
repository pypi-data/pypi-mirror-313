from collections import defaultdict
from pathlib import Path

import pandas as pd
from parsita import Success

from .._sdk import client
from .._sdk.ode_model import OdeModelFromText
from .._sdk.ode_model_reference import OdeModelReference
from .._sdk.ode_simulation import OdeSimulation
from .._sdk.reaction_model import Parameter, ReactionModel
from .parser import parse_unitted_nan


def initialize_parameter_table(model_path: str, parameter_table: str) -> None:
    model_path = Path(model_path)
    text = model_path.read_text(encoding="utf-8")
    original_model = OdeModelFromText(text=text, format="reaction").parse()

    # find nans and replace them with zeros (this only works for nan:unit)
    parameters = original_model.parameters
    nan_parameters = []
    for key, value in parameters.items():
        maybe_nan_parameter = parse_unitted_nan(str(value.value))
        if isinstance(maybe_nan_parameter, Success):
            _, unit = maybe_nan_parameter.unwrap()
            nan_parameters.append(key)
            if unit is None and value.unit is not None:
                unit = value.unit
            parameters[key] = Parameter(value=0, unit=unit)

    # reduce a model to only parameters and time unit
    reduced_model = ReactionModel(parameters=original_model.parameters).store(include_definition=True)
    model_reference = OdeModelReference(reduced_model.id)
    simulation = OdeSimulation(model=model_reference, output_times=[0])
    job = client.create_jobs([simulation])
    _ = client.create_contract(job, progress=True)
    output = job[0].output_or_raise()
    parameters = defaultdict(list)
    for key, value in output.outputs.items():
        parameters["parameter"].append(key)
        if key in nan_parameters:
            parameters["value"].append("nan")
        else:
            parameters["value"].append(value.value)
        parameters["unit"].append(value.unit)

    df = pd.DataFrame.from_dict(parameters)
    df.to_csv(parameter_table, index=False)

    #  Remove the last new line character
    #  This happens because the last line is written with a newline character.
    parameter_table = Path(parameter_table)
    content = parameter_table.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    parameter_table.write_text(content)
