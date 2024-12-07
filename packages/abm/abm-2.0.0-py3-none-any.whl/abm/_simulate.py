from __future__ import annotations

__all__ = ["Options", "SimulationResult", "simulate"]

import math
import warnings
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
import tabeline as tl
from ordered_set import OrderedSet

from ._helper.create_map import create_doses_map, create_models_map, create_parameters_map, create_times_map
from ._helper.get_dose_schedules import get_dose_schedules
from ._helper.get_model import get_model_i, get_models
from ._helper.get_table import get_table
from ._helper.helper import (
    DataFrameLike,
    PathLike,
    UnittedLinSpace,
    find_duplicate_keys,
    is_equivalent,
    maybe_add_parentheses,
    necessary_dose_columns,
    necessary_model_columns,
    necessary_parameter_columns,
    necessary_time_columns,
    optional_dose_columns,
    replace_asterisk_with_none,
)
from ._helper.parse_output_times import parse_times
from ._helper.parser import parse_unitted_number
from ._labelset import LabelSet
from ._scan_ast import NoScan, Scan
from ._sdk import client
from ._sdk.contract import Contract
from ._sdk.data_frame import DataFrame
from ._sdk.data_pipe import ConcatenateRowsElement, DataPipe, OdeSimulationElement
from ._sdk.expression import Expression
from ._sdk.job import Job
from ._sdk.ode_model import OdeModel, OdeModelFromText
from ._sdk.ode_model_reference import OdeModelReference
from ._sdk.ode_simulation import OdeSimulation
from ._sdk.reaction_model import ReactionModel
from ._sdk.solver_configuration import BdfSolver, KluSolver, SolverConfiguration, SpgmrSolver
from ._sdk.time_course import TimeCourse
from ._sdk.times import Times
from ._sdk.to_latex_ode_model import to_latex as _to_latex


@dataclass(frozen=True)
class Options:
    allow_none: bool = False
    allow_asterisk: bool = False


def simulate(
    *,
    simulations: DataFrameLike | PathLike | None = None,
    models: DataFrameLike | PathLike,
    parameters: DataFrameLike | PathLike | None = None,
    doses: DataFrameLike | PathLike | None = None,
    times: DataFrameLike | PathLike | list[Expression] | UnittedLinSpace,
    outputs: list[str] | None = None,
    scans: Scan = NoScan(),
    linear_solver: Literal["KLU", "SPGMR"] = "KLU",
    reltol: float = 1e-6,
    abstol: float = 1e-9,
    maxstep: float = math.inf,
    maxord: int = 5,
    nonnegative: bool | dict[str, bool] = False,
) -> SimulationResult:
    """Run simulations based on tables of models, parameters, and doses.

    Parameters
    ----------
    simulations: pd.DataFrame | tl.DataFrame | DataFrame | Path | str | None
        A data frame or a path to a CSV file. Each row is a single simulation.

        This table has arbitrary columns each of which is a label column. Each record in those
        label columns is used to match records in columns of the same name in the models,
        parameters, and doses tables. Those that match determine how the simulation runs. In the
        other tables, a "*" may be used in a label column to indicate that that row should match
        any value in the measurement table.

        If None, there is only one simulation.
    models: pd.DataFrame | tl.DataFrame | DataFrame | Path | strç
        A model or a data frame or a path to a CSV file. If a model, it is used for all
        simulations. If a data frame or CSV, it has columns:
            `model`: str, path to a model file
    parameters: pd.DataFrame | tl.DataFrame | DataFrame | Path | str | None
        Parameter value table with columns:
            `parameter`: str, name of parameter
            `value`: float, value of parameter
            `unit`: str, unit for `value`

        If None, the model parameters are used.
    doses: pd.DataFrame | tl.DataFrame | DataFrame | Path | str | None
        Dose table with columns:
            `route`: str, name of a model route
            `times`: float or list[float], times of the doses
            `time_unit`: str, unit for `times`
            `amounts`: float or list[float], amount of the doses
            `amount_unit`: str, unit for `amounts`
            `durations`: float or list[float], duration of the doses, default = 0.0
            `duration_unit`: str, unit for `durations`, only mandatory if `durations` is not zero

        If None, the model schedules are used.
    times: pd.DataFrame | tl.DataFrame | DataFrame | Path | str | list[Expression]
        A list of output times or a data frame or a path to a CSV file. If a list of expressions,
        it is the output times for all simulations. If a data frame or CSV, it has columns:
            `times`: float or list[float], times of the outputs
            `times_unit`: str, unit for `times`
    outputs: list[str] | None
        Outputs to simulate. Outputs must be present in all models or it is an error. If None, it
        is the intersection of all model outputs. Exported outputs across all models must have the
        same units.
    scans: Scan
        A scan object to scan parameters.
    linear_solver : `'KLU'`, `'SPGMR'`, default=`'KLU'`
        Linear solver used by the ODE solver to solve the implicit formula for
        each integration step. Generally this should not be changed from the
        default.
    reltol: `float`, default=1e-6
        Relative tolerance of the integration.
    abstol: `float`, default=1e-9
        Absolute tolerance of the integration.
    maxstep : `float`, default=inf
        Maximum time step allowed during integration. Generally, this should not
        be changed from the default (unbounded).
    maxord: `int`, default=5
        Maximum order of the linear multistep formulas used by the ODE solver.
        Setting to a lower value results in smaller but more stable time steps.
        Generally it is recommended to use the largest value that converges.
    nonnegative: `bool` or `dict[str, bool]`, default=`False`
        Substitute 0 for negative values in the indicated states when evaluating
        the ODE right-hand side. This is useful for avoiding numerical
        difficulties with model expressions like `sqrt` that are not real or not
        defined for negative values. If `False`, no states are substituted if
        negative. If `True`, all states are substituted if negative. If a
        `dict[str, bool]` is provided, any keys with `True` values are
        interpreted as state names to be substituted; any states not appearing
        in the dictionary are not substituted.

    Returns
    -------
    SimulationResult
    """
    # initial validation and processing of the incoming tables
    simulations = validate_and_process_simulation_table(simulations)
    models = validate_and_process_model_table(models)
    parameters = validate_and_process_parameter_table(parameters)
    doses = validate_and_process_dose_table(doses)
    times = validate_and_process_times(times)

    # get the parameters map
    all_label_columns = OrderedSet(simulations.column_names)
    parameters_labels = all_label_columns.intersection(OrderedSet(parameters.column_names)).items
    parameters_map = create_parameters_map(parameters, parameters_labels)
    doses_labels = all_label_columns.intersection(OrderedSet(doses.column_names)).items
    doses_map = create_doses_map(doses, doses_labels)

    # The type of the column in `simulations` takes precedence (e.g. if numbers appear in the parameters table,
    # they must be cast to string if the column in `simulations` is string)

    # create the labels from simulation table and scans for final results
    # labels_info_table is only being used to produce the final output table
    if not isinstance(scans, NoScan):
        # label_columns does not work for NoScan
        scans_label_columns = scans.label_columns
        labels_info_table = tl.DataFrame.from_polars(
            simulations.to_polars().join(scans_label_columns.to_polars(), how="cross")
        )
    else:
        labels_info_table = simulations

    # Add id column for each simulation to use as key to inner-join later with the simulation results.
    labels_info_table = labels_info_table.mutate(id="row_index0()")

    # check if there is one model object for all simulations.
    # There is one way that we know upfront that there is one model for all simulations,
    #  which is a OdeModelReference being provided and converted to Job[OdeModel, None] after processing
    one_model_for_all_simulations = False
    if isinstance(models, Job):
        one_model_for_all_simulations = True
        model = models
        model = model.refresh(include_definition=True)
        assert isinstance(model.definition, ReactionModel)
        all_parameters = {key: parameter.unit for key, parameter in model.definition.parameters.items()}
        all_outputs = (
            {key: assignment.unit for key, assignment in model.definition.assignments.items()}
            | {key: variable.unit for key, variable in model.definition.bound_variables.items()}
            | all_parameters
            | {key: state.unit for key, state in model.definition.states.items()}
        )
    else:
        model_paths = set(models[:, "model"])
        remote_model_map = {
            model_path: OdeModelFromText(text=Path(model_path).read_text(encoding="utf-8"), format="reaction")
            .parse()
            .store(include_definition=True)
            for model_path in model_paths
        }
        models_labels = all_label_columns.intersection(OrderedSet(models.column_names)).items
        models_map = create_models_map(models, models_labels)

    # possible cases for outputs:
    # 1) outputs is not None & there is one model for all simulations:
    #       Verification steps:
    #                   1a) verify all outputs exist in the model
    # 2) outputs is not None and there are more than one model for all simulations (models is a table)
    #       Verification steps:
    #                   2a) verify all outputs exist in every model
    #                   2b) verify that all outputs have the same unit in all models
    # 3) outputs is not None & there is one model for all simulations:
    #       Verification steps: There is no verification steps since outputs comes directly from the model
    # 4) outputs is None and there are more than one model for all simulations (models is a table)
    # in this case the outputs would be intersection of all model outputs
    #       Verification steps:
    #                   4a) verify that all final outputs have the same unit in all models

    outputs_set = OrderedSet()
    if outputs is not None:
        outputs_set = OrderedSet(outputs)

    # if there is one model for all simulations (case 1 or case 3) then there must be one set of outputs for
    # all simulations: either the provided list in the outputs or all parameters/assignments of the model.
    if one_model_for_all_simulations:
        if outputs is not None:
            # case (1)
            nonexistent_outputs = outputs_set - OrderedSet(all_outputs.keys())
            if len(nonexistent_outputs) > 0:
                raise ValueError(
                    f"Cannot output variables not present in the model: {', '.join(sorted(nonexistent_outputs))}"
                )
        else:
            # case (3)
            outputs_set = OrderedSet(all_outputs.keys())

    one_output_times_for_all_simulations = False
    if isinstance(times, Times | list):
        output_times = times
        one_output_times_for_all_simulations = True
    else:
        times_labels = all_label_columns.intersection(OrderedSet(times.column_names)).items
        times_map = create_times_map(times, times_labels)

    model_reference_list = []
    output_times_list = []
    simulation_labels = LabelSet.from_df(simulations)
    filled_scans_df_list = []

    # building the simulations has the following main steps:
    # 1) get the model for the simulation if these is not one model for all simulations.
    # 2) get the outputs for simulations and validate them.
    # 3) get the parameters for the simulation and do some validations.
    # 4) get the doses for the simulation and do some validations.
    # 5) get the output times for each simulation and add it to the list.
    # 6) if there are scans then get the parameter for each scan.
    # 7) create the OdeModelReference and add it to the list.
    # 8) build the SimulationList object and run it.

    for i_lbs, lbs in enumerate(simulation_labels):
        # Step 1: get the model for the simulation if these is not one model for all simulations.
        if not one_model_for_all_simulations:
            # find the model by filtering the model tables based on label columns
            model_list_i = models_map.get_values([lbs.labels.get(k, "*") for k in models_labels])
            model = get_model_i(model_list_i, remote_model_map, lbs.original_labels)
            assert isinstance(model.definition, ReactionModel)

            # build the reference time unit from the first model:
            if i_lbs == 0:
                reference_time_unit = model.definition.time_unit

            # check if the time unit of the model is the same as the reference time unit
            if not is_equivalent(model.definition.time_unit, reference_time_unit):
                raise ValueError(
                    f"all models must have the same time unit but model {model.id} has time unit"
                    f" {model.definition.time_unit} which is different from {reference_time_unit}"
                )

            # all parameters of the model
            all_parameters = {key: parameter.unit for key, parameter in model.definition.parameters.items()}

            # Step 2: get the outputs for simulations and validate them.

            # all possible outputs for this model
            all_outputs = (
                {key: assignment.unit for key, assignment in model.definition.assignments.items()}
                | {key: variable.unit for key, variable in model.definition.bound_variables.items()}
                | all_parameters
                | {key: state.unit for key, state in model.definition.states.items()}
            )

            # case (2)
            if outputs is not None:
                # outside the loop outputs_set has been defined if outputs is not None
                nonexistent_outputs = outputs_set - OrderedSet(all_outputs.keys())
                if len(nonexistent_outputs) > 0:
                    raise ValueError(
                        "Cannot output variables not present in all the model:"
                        f" {', '.join(sorted(nonexistent_outputs))}"
                    )
                # build the reference units from the first model:
                if i_lbs == 0:
                    reference_units = {key: all_outputs[key] for key in outputs_set}

                # check if the units of the outputs are the same as the reference units
                for key in outputs_set:
                    if not is_equivalent(all_outputs[key], reference_units[key]):
                        raise ValueError(
                            f"requested outputs in all models must have the same unit but {key} has unit"
                            f" {all_outputs[key]} which is different from {reference_units[key]}"
                        )

            # case (4)
            else:
                if i_lbs == 0:
                    reference_units = all_outputs
                    reference_outputs = set(reference_units.keys())
                    # we set output_sets at the first iteration and then every time update it
                    outputs_set = reference_outputs
                # we set output_sets as the all potential outputs of this model
                outputs_set = outputs_set.intersection(OrderedSet(all_outputs.keys()))
                outputs_i = {key: all_outputs[key] for key in outputs_set}
                # check if the units of the outputs are the same as the reference units
                for key in outputs_set:
                    if not is_equivalent(outputs_i[key], reference_units[key]):
                        raise ValueError(
                            f"requested outputs in all models must have the same unit but {key} has unit"
                            f" {outputs_i[key]} which is different from {reference_units[key]}"
                        )

        # Step 3: get the parameters for the simulation and do some validations.
        parameter_list_i = parameters_map.get_values([lbs.labels.get(k, "*") for k in parameters_labels])
        duplicate_parameters = find_duplicate_keys(parameter_list_i)
        if len(duplicate_parameters) > 0:
            if len(lbs.original_labels) > 0:
                raise ValueError(
                    "Duplicate parameters found for label(s)"
                    f" {', '.join([f'{key}={value}' for key, value in lbs.original_labels.items()])}:"
                    f" {', '.join(duplicate_parameters)}"
                )
            else:
                raise ValueError(f"Duplicate parameters found: {', '.join(duplicate_parameters)}")
        parameter_dict_i = {key: value for dic in parameter_list_i for key, value in dic.items()}

        # check for parameters that are not in the model
        non_model_parameters = set(parameter_dict_i.keys()) - set(all_parameters.keys())
        if len(non_model_parameters) > 0:
            warnings.warn(
                f"Parameters not present in the model will be ignored: {', '.join(sorted(non_model_parameters))} ",
                stacklevel=1,
            )
            # remove the parameters that are not in the model
            parameter_dict_i = {
                key: value for key, value in parameter_dict_i.items() if key not in non_model_parameters
            }

        # Step 4: get the doses for the simulation and do some validations.
        dose_i = doses_map.get_values([lbs.labels.get(k, "*") for k in doses_labels])
        route_schedules_i = get_dose_schedules(dose_i, lbs.original_labels)

        # Step 5: get the output times for each simulation and add it to the list.
        output_times_i = []
        if not one_output_times_for_all_simulations:
            times_list_i = times_map.get_values([lbs.labels.get(k, "*") for k in times_labels])
            if len(times_list_i) == 0:
                raise ValueError(
                    "No output times found for the simulation with labels for label(s): "
                    f" {', '.join([f'{key}={value}' for key, value in lbs.original_labels.items()])}"
                )
            if len(times_list_i) > 1:
                raise ValueError(
                    "Multiple output times found for the simulation with labels for label(s): "
                    f" {', '.join([f'{key}={value}' for key, value in lbs.original_labels.items()])}"
                )
            output_times_i = parse_times(times_list_i[0])
        else:
            output_times_i = output_times

        # create to a list of expressions for parameters
        parameter_dict_i_expressions = {
            key: f"{param.value}:{maybe_add_parentheses(param.unit)}" for key, param in parameter_dict_i.items()
        }

        # Step 6: if there are scans then get the parameter for each scan.
        # check scan parameters:
        nonexistent_params = scans.parameters - set(all_parameters.keys())
        if len(nonexistent_params) > 0:
            raise ValueError(
                f"Cannot scan parameters not present in parameter table: {', '.join(sorted(nonexistent_params))}"
            )
        evaluated_scans = scans.evaluate(parameter_dict_i)
        for evaluated_scan in evaluated_scans:
            parameter_dict_ij = parameter_dict_i_expressions.copy()
            validate_scan_units(evaluated_scan, parameter_dict_ij)
            # Since in both scan and fold scans the units are the same as the reference units, we can use the
            # reference units to create the scan parameters. With this implementation we ensure that the units
            # of the scan parameters are the same as the units in the parameter table in terms of formating

            scan_parameters = {
                key: f"{param.value}:{maybe_add_parentheses(parse_unitted_number(parameter_dict_ij[key])[1])}"
                for key, param in evaluated_scan.items()
            }

            filled_scans_df_list.append(fill_scan_table(evaluated_scan, parameter_dict_ij))
            parameter_dict_ij.update(scan_parameters)
            # Step 7: create the OdeModelReference and add it to the list.
            model_reference_list.append(OdeModelReference(model.id, parameter_dict_ij, route_schedules_i))
            output_times_list.append(output_times_i)

    # Step 8: build the SimulationList object and run it.
    final_outputs = list(outputs_set)
    if not isinstance(scans, NoScan):
        filled_scans_df = tl.concatenate_rows(*filled_scans_df_list)
        labels_info_table = tl.concatenate_columns(
            labels_info_table.deselect(*filled_scans_df.column_names), filled_scans_df
        )

    match linear_solver:
        case "KLU":
            linear_solver_obj = KluSolver()
        case "SPGMR":
            linear_solver_obj = SpgmrSolver()
        case unsupported:
            raise ValueError(f"Unsupported linear solver {unsupported}")

    solver_configuration = SolverConfiguration(
        ode_solver=BdfSolver(
            linear_solver=linear_solver_obj,
            relative_tolerance=reltol,
            absolute_tolerance=abstol,
            max_step=maxstep,
            max_order=maxord,
        ),
        nonnegative=nonnegative,
    )
    simulations = [
        OdeSimulation(
            model=model, output_times=output_times, output_names=final_outputs, configuration=solver_configuration
        )
        for model, output_times in zip(model_reference_list, output_times_list, strict=True)
    ]

    # Store and run jobs
    jobs = client.create_jobs(simulations)
    contract = client.create_contract(jobs, progress=True)
    return SimulationResult(
        _contract=contract,
        _jobs=jobs,
        _simulations=simulations,
        _scans=scans,
        _labels_info_table=labels_info_table,
        _outputs=final_outputs,
    )


@dataclass(frozen=True, eq=False)
class SimulationResult:
    """Reference to simulation outputs.

    Attributes
    ----------
    _contract: Contract
        Handle to the contract that is running the simulations.
    _jobs: list[Job]
        List of jobs.
    _simulations: list[OdeSimulation]
        List of simulations.
    _scans: Scan
        A scan object to scan parameters.
    _labels_info_table: tl.DataFrame
        A table of the labels used in each simulation. Each row of the table is a simulation.
    _outputs: list[str]
        Outputs to simulate.
    """

    _contract: Contract
    _jobs: list[Job[OdeSimulation, TimeCourse]]
    _simulations: list[OdeSimulation]
    _scans: Scan
    _labels_info_table: tl.DataFrame
    _outputs: list[str]

    def to_data_pipe(self, tall_outputs: bool = False, on_failure: Literal["error", "ignore"] = "error") -> DataPipe:
        """Convert the simulation results to an data_pipe object.

        Parameters
        ----------
        tall_outputs: bool
            If True, the output table will be tall, otherwise it will be wide.

        on_failure: Literal["error", "ignore"], default="error"
            Specifies the action to take when one or more simulations fail. If set to "error", the first simulation to
            fail will raise its error. If set to "ignore", an empty DataFrame will be used as the output of failed
            simulations.

        Returns
        -------
        DataPipe
        """

        if len(self._simulations) == 0:
            raise ValueError("There is no simulation to output")

        # Update on_failure to match SDK's SimulationElement
        if on_failure == "ignore":
            on_failure = "empty"

        labels_data_pipe = DataFrame.from_tabeline(self._labels_info_table).to_data_pipe()
        simulation_data_pipe = ConcatenateRowsElement(
            [
                OdeSimulationElement(job.id, on_failure=on_failure).mutate(id=index)
                for index, job in enumerate(self._jobs)
            ]
        )
        final_data_pipe = labels_data_pipe.inner_join(simulation_data_pipe, by=[("id", "id")])

        if tall_outputs:
            return final_data_pipe.gather("output", "value", *self._outputs, unit="output_unit")
        else:
            return final_data_pipe

    def to_data_frame(self, tall_outputs: bool = False, on_failure: Literal["error", "ignore"] = "error") -> DataFrame:
        """Convert the simulation results to a data frame.

        Parameters
        ----------
        tall_outputs: bool
            If True, the output data frame will be tall, otherwise it will be wide.

        on_failure: Literal["error", "ignore"], default="error"
            Specifies the action to take when one or more simulations fail. If set to "error", the first simulation to
            fail will raise its error. If set to "ignore", an empty DataFrame will be used as the output of failed
            simulations.

        Returns
        -------
        DataFrame
        """

        return self.to_data_pipe(tall_outputs=tall_outputs, on_failure=on_failure).run().to_data_frame()

    def to_tabeline(self, tall_outputs: bool = False, on_failure: Literal["error", "ignore"] = "error") -> tl.DataFrame:
        """Convert the simulation results to a Tabeline DataFrame.

        Parameters
        ----------
        tall_outputs: bool
            If True, the output table will be tall, otherwise it will be wide.

        on_failure: Literal["error", "ignore"], default="error"
            Specifies the action to take when one or more simulations fail. If set to "error", the first simulation to
            fail will raise its error. If set to "ignore", an empty DataFrame will be used as the output of failed
            simulations.

        Returns
        -------
        tl.DataFrame
        """

        return self.to_data_pipe(tall_outputs=tall_outputs, on_failure=on_failure).run().to_tabeline()

    def to_pandas(self, tall_outputs: bool = False, on_failure: Literal["error", "ignore"] = "error") -> pd.DataFrame:
        """Convert the simulation results to a Pandas DataFrame.

        Parameters
        ----------
        tall_outputs: bool
            If True, the output table will be tall, otherwise it will be wide.

        on_failure: Literal["error", "ignore"], default="error"
            Specifies the action to take when one or more simulations fail. If set to "error", the first simulation to
            fail will raise its error. If set to "ignore", an empty DataFrame will be used as the output of failed
            simulations.

        Returns
        -------
        pd.DataFrame
        """

        return self.to_data_pipe(tall_outputs=tall_outputs, on_failure=on_failure).run().to_pandas()

    def to_matlab(self, path: Path | str, row: int = 0) -> None:
        """Create Matlab script from simulations.


        Parameters
        ----------
        path: Path | str
            The path of the file that will be created.

        row: int
            The index of the row of the simulation table to be converted to a Matlab script.
            The default is 0 which is the first row. If the simulation table is None, then there is only
            one simulation.
        """

        row = row * len(self._scans)
        self._simulations[row].to_matlab(path)

    def to_simbiology(self, path: Path | str, row: int = 0) -> None:
        """Create Simbiology script from simulation.


        Parameters
        ----------
        path: Path | str
            The path of the file that will be created.

        row: int
            The index of the row of the simulation table to be converted to a simbiology script.
            The default is 0 which is the first row. If the simulation table is None, then there is only
            one simulation.
        """

        row = row * len(self._scans)
        self._simulations[row].to_simbiology(path)

    def to_latex(
        self,
        path: Path | str,
        row: int = 0,
        inlined: bool = False,
        name_map: dict[str, str] | None = None,
    ) -> None:
        """Create LateX document for a model associated with a simulation.


        Parameters
        ----------
        path: Path | str
            The path of the file that will be created.

        row: int
            The index of the row of the simulation table that its model will be converted to a LaTeX document.
            The default is 0 which is the first row. If the simulation table is None, then there is only
            one simulation and one model.

        inlined : bool
            Specifies if the right hand side of the equations are inlined. Default is False

        name_map: dict[str, str] | None
            A dictionary where the keys are parameter, assignment, or state names from the model
            and the values are the preferred name in LaTeX format.
            for example {v_central: v_{c}, SECONDS_PER_MINUTE: r'\frac{sec}{min}'}
        """

        row = row * len(self._scans)
        model_reference = self._simulations[row].model
        _to_latex(path=path, model=model_reference, inlined=inlined, name_map=name_map)


def validate_and_process_simulation_table(simulations: DataFrameLike | PathLike | None = None) -> tl.DataFrame:
    if simulations is None:
        return tl.DataFrame.columnless(height=1)
    else:
        options = Options(allow_none=False, allow_asterisk=False)
        simulation_table = get_table(simulations)
        validate_columns(simulation_table, "simulation table", options=options)
        return simulation_table


def validate_and_process_model_table(
    models: DataFrameLike | PathLike,
) -> Job[OdeModel, None] | tl.DataFrame:
    models = get_models(models)
    if isinstance(models, Job):
        return models
    else:
        options = Options(allow_none=False, allow_asterisk=True)
        validate_columns(models, "model table", necessary_columns=necessary_model_columns, options=options)
        # replace asterisks with None
        models_table = replace_asterisk_with_none(models)
        return models_table


def validate_and_process_parameter_table(parameters: DataFrameLike | PathLike | None = None) -> tl.DataFrame:
    if parameters is None:
        kw = {key: [] for key in necessary_parameter_columns}
        return tl.DataFrame(**kw)
    else:
        parameters_table = get_table(parameters)
        options = Options(allow_none=False, allow_asterisk=True)
        validate_columns(
            parameters_table, "parameter table", necessary_columns=necessary_parameter_columns, options=options
        )
        # replace asterisks with None
        parameters_table = replace_asterisk_with_none(parameters_table)
        parameters_table = parameters_table.mutate(unit="to_string(unit)")
        return parameters_table


def validate_and_process_dose_table(doses: DataFrameLike | PathLike | None = None) -> tl.DataFrame:
    if doses is None:
        kw = {key: [] for key in necessary_dose_columns}
        return tl.DataFrame(**kw)
    else:
        doses_table = get_table(doses)
        options = Options(allow_none=False, allow_asterisk=True)
        # check for optional columns
        if "durations" in doses_table.column_names or "duration_unit" in doses_table.column_names:
            necessary_columns = necessary_dose_columns | optional_dose_columns
        else:
            necessary_columns = necessary_dose_columns

        validate_columns(doses_table, "dose table", necessary_columns=necessary_columns, options=options)
        # replace asterisks with None
        doses_table = replace_asterisk_with_none(doses_table)
        doses_table = doses_table.mutate(amount_unit="to_string(amount_unit)", time_unit="to_string(time_unit)")
        if "duration_unit" in doses_table.column_names:
            doses_table = doses_table.mutate(duration_unit="to_string(duration_unit)")
        return doses_table


def validate_and_process_times(
    times: DataFrameLike | PathLike | list[Expression] | UnittedLinSpace,
) -> tl.DataFrame | Times:
    if isinstance(times, list):
        return times
    if isinstance(times, UnittedLinSpace):
        return times.to_linspace_times()
    else:
        times_table = get_table(times)
        options = Options(allow_none=False, allow_asterisk=True)
        validate_columns(times_table, "time table", necessary_columns=necessary_time_columns, options=options)
        # replace asterisks with None
        times_table = replace_asterisk_with_none(times_table)
        times_table = times_table.mutate(times_unit="to_string(times_unit)")
        return times_table


def validate_columns(df: tl.DataFrame, table_name: str, *, necessary_columns: set[str] = {}, options: Options) -> None:
    column_names = df.column_names
    if len(necessary_columns) > 0 and not necessary_columns.issubset(set(column_names)):
        raise ValueError(f"{table_name} must have the necessary column(s): {', '.join(sorted(necessary_columns))}.")
    errors = defaultdict(list)
    for column in column_names:
        # check for null values in columns (depending on options)
        if not options.allow_none and None in df[:, column]:
            errors["none"].append(column)
        # asterisk is not allowed in necessary columns
        if "*" in df[:, column]:
            if column in necessary_columns:
                errors["asterisk_in_necessary"].append(column)
            else:
                # check for asterisk in label columns (depending on options)
                if not options.allow_asterisk:
                    errors["asterisk"].append(column)
    if len(errors) > 0:
        error_message = ""
        if len(errors["none"]) > 0:
            error_message += (
                f"NULL(empty) values are not allowed in {table_name} but found in column(s):"
                f" {', '.join(errors['none'])}."
            )
        if len(errors["asterisk_in_necessary"]) > 0:
            error_message += (
                f"'*' is not allowed in necessary column(s) of {table_name} but found in column(s):"
                f" {', '.join(errors['asterisk_in_necessary'])}."
            )
        if len(errors["asterisk"]) > 0:
            error_message += (
                f"'*' is not allowed in label column(s) of {table_name} but found in column(s):"
                f" {', '.join(errors['asterisk'])}."
            )
        raise ValueError(error_message)


def fill_scan_table(evaluated_scan, parameter_dict_ij) -> tl.DataFrame:
    tabel_data = defaultdict(list)
    for i, (key, value) in enumerate(evaluated_scan.items()):
        tabel_data[f"param_scan_{i}"].append(key)
        tabel_data[f"scan_{i}_value"].append(value.value)
        reference_value = parse_unitted_number(parameter_dict_ij[key])[0]
        try:
            new_fold = value.value / reference_value
        except ZeroDivisionError:
            new_fold = np.nan if value.value == 0.0 else np.inf
        tabel_data[f"scan_{i}_fold"].append(new_fold)

    return tl.DataFrame.from_dict(tabel_data)


def validate_scan_units(evaluated_scan, parameter_dict_ij) -> None:
    for key, value in evaluated_scan.items():
        scan_unit = value.unit

        reference_unit = parse_unitted_number(parameter_dict_ij[key])[1]

        if not is_equivalent(scan_unit, reference_unit):
            raise ValueError(
                f"requested scan parameters {key} must have the same unit as in parameter table or model"
                f" but it has unit {scan_unit} which is different from {reference_unit}"
            )
