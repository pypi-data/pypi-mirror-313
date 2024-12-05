# PyZefir
# Copyright (C) 2023-2024 Narodowe Centrum Badań Jądrowych
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import configparser
from dataclasses import dataclass, field
from itertools import repeat
from pathlib import Path
from typing import Any, overload

import linopy
import numpy as np
import pandas as pd

from pyzefir.cli.logger import DEFAULT_LOG_LEVEL, LOG_LEVEL_MAPPING


class ConfigException(Exception):
    pass


@dataclass(frozen=True, kw_only=True)
class ConfigParams:
    """Class to hold configuration parameters."""

    input_path: Path
    """path to the model input data (either *.csv or *.xlsx files)"""
    scenario: str
    """name of the scenario"""
    input_format: str
    """csv or xlsx"""
    output_path: Path
    """path to the folder, where model results will be dumped"""
    csv_dump_path: Path | None
    """path to the folder, where converted (xlsx -> csv) files will be stored [default = output_path/model-csv-input]"""
    sol_dump_path: Path
    """path where linopy *.sol file will be dumped [default = output_path/results.sol]"""
    opt_logs_path: Path
    """path where linopy log file will be dumped [default = output_path/linopy.log]"""
    year_sample: np.ndarray | None
    """indices of years forming year sample [if not provided, full year index will be used]"""
    hour_sample: np.ndarray | None
    """indices of hours forming hour sample [if not provided, full hour index will be used]"""
    discount_rate: np.ndarray | None
    """vector containing discount year for consecutive years [if not provided, zero discount rate is assumed]"""
    network_config: dict[str, Any]
    """network configuration"""
    money_scale: float = 1.0
    """ numeric scale parameter """
    use_hourly_scale: bool = True
    """ use ratio of the total number of hours to the total number of hours in given sample """
    n_years: int | None
    """ number of years in which the simulation will be calculated (used for structure creator) """
    n_hours: int | None
    """ number of hours in which the simulation will be calculated (used for structure creator) """
    solver: str | None = None
    structure_creator_input_path: Path | None = None
    """ path to the creator input files """
    format_exceptions: bool = True
    """ whether to format exceptions or not handle them at all """
    log_level: int
    """ logging level """
    solver_settings: dict[str, dict[str, Any]] = field(default_factory=dict)
    """ additional settings that can be passed to the solver """
    n_years_aggregation: int = 1
    """ number of years to aggregate in the optimization """
    year_aggregates: np.ndarray | None = None
    """ indices of years to aggregate """
    aggregation_method: str | None = None
    """ method of aggregation """
    xlsx_results: bool = False
    """ dump results into additional xlsx files (outside the default CSV files)"""

    def __post_init__(self) -> None:
        """Validate parameters."""
        validate_dir_path(self.input_path, "input_path")
        validate_dir_path(self.output_path, "output_path", create=True)
        validate_1D_array(self.year_sample, "year_sample")
        validate_1D_array(self.discount_rate, "discount_rate")
        validate_1D_array(self.hour_sample, "hour_sample")
        validate_input_format(self.input_format)
        validate_csv_dump_path(self.csv_dump_path, self.input_format)
        validate_sol_dump_path(self.sol_dump_path)
        validate_dir_path(self.opt_logs_path.parent, "opt_logs_path parent")
        validate_solver_name(self.solver)
        validate_structure_create(
            self.n_hours, self.n_years, self.structure_creator_input_path
        )
        validate_network_config(self.network_config)


def validate_network_config(network_config: dict[str, Any]) -> None:

    if not isinstance(network_config["binary_fraction"], bool):
        raise ConfigException("given binary_fraction parameter must be a boolean")

    if not isinstance(network_config["ens_penalty_cost"], float):
        raise ConfigException("given ens_penalty_cost must be a float")

    if network_config["generator_capacity_cost"] not in ["netto", "brutto"]:
        raise ConfigException(
            f"given value of a generator_capacity_cost {network_config['generator_capacity_cost']} "
            f"is different than allowed values netto or brutto."
        )


def validate_generator_capacity_cost(generator_capacity_cost: str) -> None:
    """
    Validate if given value of generator_capacity_cost is correct.
    """
    if generator_capacity_cost not in ["netto", "brutto"]:
        raise ConfigException(
            f"given value of a generator_capacity_cost {generator_capacity_cost} is different than allowed values "
            f"netto or brutto."
        )


def validate_structure_create(
    n_hours: int | None,
    n_years: int | None,
    input_path: Path | None,
) -> None:
    """Validate if are the same type and if both are int check if input_path exists"""
    if (n_hours is None) != (n_years is None):
        raise ConfigException(
            "Both parameters must have the same int or None value,"
            f"and they do n_hours: {type(n_hours)} and n_years: {type(n_years)}"
        )
    if n_hours is not None and n_years is not None and input_path is not None:
        validate_dir_path(input_path, "structure creator")


def validate_file_path(file_path: Path, param_name: str) -> None:
    """Validate if the specified path points to an existing file."""
    if not file_path.exists():
        raise ConfigException(
            f"Path specified as {param_name} does not exist: {file_path}"
        )
    if not file_path.is_file():
        raise ConfigException(
            f"Path specified as {param_name} does not point to a file: {file_path}"
        )


def validate_dir_path(dir_path: Path, param_name: str, create: bool = False) -> None:
    """Validate if the specified path points to an existing folder."""
    if not dir_path.exists():
        if not create:
            raise ConfigException(
                f"Path specified as {param_name} should exist: {dir_path}"
            )
        dir_path.mkdir(parents=True)
    if not dir_path.is_dir():
        raise ConfigException(
            f"Path specified as {param_name} should point to a folder: {dir_path}"
        )


def validate_suffix(path: Path, suffix: str, param_name: str) -> None:
    """Validate if path is pointing to a file / directory with given suffix."""
    if not path.suffix == suffix:
        raise ConfigException(
            f"Path specified as {param_name} has incorrect suffix: {path.name} (expected {suffix})"
        )


def validate_config_path(config_ini_path: Path) -> None:
    """Validate if the specified path is a valid .ini configuration file."""
    validate_file_path(config_ini_path, "config_file_path")
    validate_suffix(config_ini_path, ".ini", "config_file_path")


def validate_sol_dump_path(path: Path) -> None:
    """Validate specified path to *.sol file."""
    validate_dir_path(path.parent, "sol_dump_path directory")
    validate_suffix(path, ".sol", "sol_dump_path")


def validate_1D_array(data: np.ndarray | None, param_name: str) -> None:
    """Validate if hour_sample, year_sample or discount_rate is 1D NumPy array."""
    if data is not None and not data.ndim == 1:
        raise ConfigException(
            f"provided {param_name} is {data.ndim} dimensional dataset, one dimensional data is required"
        )


def validate_input_format(input_format: str) -> None:
    """Validate if provided input_file parameter is correct."""
    if input_format not in ["csv", "xlsx"]:
        raise ConfigException(
            f"provided input_format {input_format} is different than valid formats: csv, xlsx"
        )


def validate_csv_dump_path(csv_dump_path: Path | None, input_format: str) -> None:
    """Validate if csv_dump_path is provided only for xlsx input_format and, if it is provided - it exists."""
    if input_format == "csv" and csv_dump_path is not None:
        raise ConfigException(
            "csv_dump_path should not be specified for csv input_format"
        )
    if input_format == "xlsx" and csv_dump_path is None:
        raise ConfigException("csv_dump_path should be specified for xlsx input_format")
    if csv_dump_path is not None:
        validate_dir_path(csv_dump_path, param_name="csv_dump_path", create=True)


def validate_solver_name(solver_name: str | None) -> None:
    """Validate if solver_name is correct."""
    if solver_name is not None and solver_name not in linopy.available_solvers:
        raise ConfigException(
            f"provided solver_name {solver_name} is different than valid solvers: {linopy.available_solvers}"
        )


def validate_n_years_aggregation(n_years_aggregation: int) -> None:
    """Validate if n_years_aggregation is positive integer."""
    if n_years_aggregation <= 0:
        raise ConfigException(
            f"n_years_aggregation should be positive integer, but given: {n_years_aggregation}"
        )


def load_vector_from_csv(path: Path, param_name: str) -> np.ndarray:
    """Load 1 dimensional dataset (as 1D NumPy array) from given path."""
    validate_file_path(path, param_name)
    validate_suffix(path, ".csv", param_name)
    return pd.read_csv(path, header=None, sep=";").values.squeeze()


class ConfigLoader:
    _req, _opt, _any = "required", "optional", {"any"}
    _configurable_solvers = {"gurobi", "cplex", "highs", "glpk"}
    _mandatory_sections = {
        "input": {"input_path": _req, "scenario": _req, "input_format": _req},
        "output": {
            "output_path": _req,
            "sol_dump_path": _opt,
            "opt_logs_path": _opt,
            "csv_dump_path": _opt,
            "xlsx_results": _opt,
        },
    }
    _optional_sections = {
        "parameters": {"year_sample": _opt, "discount_rate": _opt, "hour_sample": _opt},
        "optimization": {
            "binary_fraction": _opt,
            "money_scale": _opt,
            "use_hourly_scale": _opt,
            "solver": _opt,
            "ens_penalty_cost": _opt,
            "generator_capacity_cost": _opt,
            "n_years_aggregation": _opt,
            "aggregation_method": _opt,
        },
        "create": {"n_years": _opt, "n_hours": _opt, "input_path": _opt},
        "debug": {
            "format_network_exceptions": _opt,
            "log_level": _opt,
        },
        **{solver: val for solver, val in zip(_configurable_solvers, repeat(_any))},
    }

    _sections = _mandatory_sections | _optional_sections

    _default_csv_dump_path_name = "model-csv-input"
    _default_opt_log = "opt.log"
    _default_sol = "results.sol"

    def __init__(self, config_ini_path: Path) -> None:
        validate_config_path(config_ini_path)
        self.config = configparser.ConfigParser()
        self.config.optionxform = str  # type: ignore
        self.config.read(config_ini_path)
        self._validate_config_file_structure()

    def _validate_config_file_structure(self) -> None:
        """Validate sections and parameters in loaded *.ini file."""
        if set(self._mandatory_sections) - set(self.config.sections()) or not set(
            self.config.sections()
        ).issubset(self._sections):
            raise ConfigException(
                f"incorrect *.ini file: required sections: {set(self._sections)}, given: {set(self.config.sections())}"
            )
        if "create" in self.config.sections():
            if (
                input_format_value := self.config.get("input", "input_format")
            ) != "xlsx":
                raise ConfigException(
                    "Invalid input format: If you want to use structure creator,"
                    f" input format must be xlsx but given :{input_format_value}"
                )

        self._validate_section_structure()

    def _validate_section_structure(self) -> None:
        for section in self.config.sections():
            given_keys, allowed_keys = (
                set(self.config[section]),
                set(self._sections[section]),
            )
            required_keys = set(
                [
                    key
                    for key in self._sections[section]
                    if self._sections[section] == self._req
                ]
            )
            if not required_keys.issubset(given_keys):
                raise ConfigException(
                    f"incorrect *.ini file: required parameters in section {section} are: {required_keys}, but given: "
                    f"{given_keys}"
                )
            if not allowed_keys == self._any and not given_keys.issubset(allowed_keys):
                raise ConfigException(
                    f"incorrect *.ini file: allowed parameters in section {section} are: {allowed_keys}, but given: "
                    f"{given_keys}"
                )

    @staticmethod
    def try_parse_config_option(string: str) -> float | int | bool | str:
        if string.lower() == "true":
            return True
        if string.lower() == "false":
            return False
        try:
            number = float(string)
            if number.is_integer():
                return int(number)
            return number
        except ValueError:
            pass

        return string

    def load(self) -> ConfigParams:
        """Create ConfigParams obj from given *.ini file."""
        output_path = Path(self.config.get("output", "output_path"))
        return ConfigParams(
            input_path=Path(self.config.get("input", "input_path")),
            scenario=self.config.get("input", "scenario"),
            input_format=self.config.get("input", "input_format"),
            output_path=output_path,
            csv_dump_path=self._get_path("output", "csv_dump_path"),
            sol_dump_path=self._get_path(
                "output", "sol_dump_path", output_path / self._default_sol
            ),
            opt_logs_path=self._get_path(
                "output", "opt_logs_path", output_path / self._default_opt_log
            ),
            year_sample=self._load_parameter_from_csv("year_sample"),
            hour_sample=self._load_parameter_from_csv("hour_sample"),
            discount_rate=self._load_parameter_from_csv("discount_rate"),
            money_scale=self.config.getfloat(
                "optimization", "money_scale", fallback=1.0
            ),
            network_config=self._load_network_config(),
            use_hourly_scale=self.config.getboolean(
                "optimization", "use_hourly_scale", fallback=True
            ),
            n_years=(
                int(n_years_raw)
                if (n_years_raw := self.config.get("create", "n_years", fallback=None))
                is not None
                else None
            ),
            n_hours=(
                int(n_hours_raw)
                if (n_hours_raw := self.config.get("create", "n_hours", fallback=None))
                is not None
                else None
            ),
            solver=self.config.get("optimization", "solver", fallback=None),
            structure_creator_input_path=(
                Path(creator_input)
                if (
                    creator_input := self.config.get(
                        "create", "input_path", fallback=None
                    )
                )
                is not None
                else None
            ),
            format_exceptions=self.config.getboolean(
                "debug", "format_network_exceptions", fallback=True
            ),
            log_level=self._get_log_level(),
            solver_settings={
                section: {
                    key: self.try_parse_config_option(value)
                    for key, value in self.config.items(section)
                }
                for section in self._configurable_solvers
                if section in self.config.sections()
            },
            xlsx_results=self.config.getboolean(
                "output", "xlsx_results", fallback=False
            ),
            n_years_aggregation=(
                int(n_years_aggregation)
                if (
                    n_years_aggregation := self.config.get(
                        "optimization", "n_years_aggregation", fallback=None
                    )
                )
                is not None
                else 1
            ),
            aggregation_method=self.config.get(
                "optimization", "aggregation_method", fallback="last"
            ),
        )

    def _get_log_level(self) -> int:
        config_log_level = self.config.get("debug", "log_level", fallback="")
        if (log_level := LOG_LEVEL_MAPPING.get(config_log_level.lower())) is not None:
            return log_level
        return DEFAULT_LOG_LEVEL

    def _load_network_config(self) -> dict[str, Any]:
        network_config: dict[str, Any] = {}
        if "optimization" not in self.config.sections():
            self.config.add_section("optimization")
        optimization_section = self.config["optimization"]
        network_config["binary_fraction"] = optimization_section.getboolean(
            "binary_fraction", fallback=False
        )
        network_config["ens_penalty_cost"] = optimization_section.getfloat(
            "ens_penalty_cost", fallback=np.nan
        )
        network_config["generator_capacity_cost"] = optimization_section.get(
            "generator_capacity_cost", fallback="brutto"
        )
        return network_config

    def _load_parameter_from_csv(self, parameter: str) -> np.ndarray | None:
        path = self._get_path("parameters", parameter)
        return (
            load_vector_from_csv(path, param_name=parameter)
            if path is not None
            else None
        )

    @overload
    def _get_path(self, section: str, key: str, default: Path) -> Path:
        pass

    @overload
    def _get_path(self, section: str, key: str, default: None = None) -> Path | None:
        pass

    def _get_path(
        self, section: str, key: str, default: Path | None = None
    ) -> Path | None:
        path_str = self.config[section].get(key, "")
        return Path(path_str) if path_str.strip() else default
