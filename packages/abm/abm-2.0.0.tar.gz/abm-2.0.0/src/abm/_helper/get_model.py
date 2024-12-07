__all__ = ["get_model_i", "get_models"]

from pathlib import Path

import pandas as pd
import tabeline as tl

from .._sdk.job import Job
from .._sdk.ode_model import OdeModel, OdeModelFromText
from .get_table import get_table
from .helper import DataFrameLike, PathLike


def get_models(model: DataFrameLike | PathLike | Job[OdeModel, None]) -> tl.DataFrame | Job[OdeModel, None]:
    match model:
        case str() | Path():
            models_path = Path(model)

            if not models_path.is_file():
                raise FileNotFoundError(f"{models_path} is not a file")
            if models_path.suffix in {".txt", ".model"}:
                text = models_path.read_text(encoding="utf-8")
                return OdeModelFromText(text=text, format="reaction").parse().store()
            elif models_path.suffix in {".sbml"}:
                text = models_path.read_text(encoding="utf-8")
                return OdeModelFromText(text=text, format="sbml").parse().store()
            elif models_path.suffix == ".csv":
                return get_table(models_path)
            else:
                raise ValueError(f"Unsupported file type: {models_path.suffix}")
        case tl.DataFrame() | pd.DataFrame():
            return get_table(model)
        case _:
            raise NotImplementedError(f"{type(model).__name__} is not supported type for models")


def get_model_i(
    models: list[dict], model_map: dict[str, Job[OdeModel, None]], labels: dict[str, str | float | int | bool]
) -> Job[OdeModel, None]:
    unique_models = {value["model"] for dictionary in models for value in dictionary.values()}

    # make sure that there is only one model for each simulation
    if len(models) > 1:
        if len(labels) == 0:
            raise ValueError(
                f"Multiple models found while there is no simulation table: {', '.join(sorted(unique_models))}"
            )
        else:
            raise ValueError(
                f"Multiple models found for label(s) {', '.join([f'{key}={value}' for key, value in labels.items()])}:"
                f" {', '.join(sorted(unique_models))}"
            )

    model_path = next(iter(models[0].values()))["model"]

    return model_map[model_path]
