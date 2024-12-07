from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from codeflash.cli_cmds.console import logger
from codeflash.code_utils.code_utils import get_run_tmp_file
from codeflash.code_utils.config_consts import TOTAL_LOOPING_TIME
from codeflash.code_utils.coverage_utils import prepare_coverage_files
from codeflash.models.models import CodeOptimizationContext, TestFiles
from codeflash.verification.test_results import TestType

if TYPE_CHECKING:
    from codeflash.models.models import TestFiles

is_posix = os.name != "nt"


def execute_test_subprocess(
    cmd_list: list[str], cwd: Path | None, env: dict[str, str] | None, timeout: int = 600
) -> subprocess.CompletedProcess:
    """Execute a subprocess with the given command list, working directory, environment variables, and timeout."""
    logger.debug(f"executing test run with command: {' '.join(cmd_list)}")
    return subprocess.run(cmd_list, capture_output=True, cwd=cwd, env=env, text=True, timeout=timeout, check=False)


def run_tests(
    test_paths: TestFiles,
    test_framework: str,
    test_env: dict[str, str],
    cwd: Path | None = None,
    pytest_timeout: int | None = None,
    pytest_cmd: str = "pytest",
    verbose: bool = False,
    only_run_these_test_functions: dict[Path, str] | None = None,
    pytest_target_runtime_seconds: float = TOTAL_LOOPING_TIME,
    pytest_min_loops: int = 5,
    pytest_max_loops: int = 100_000,
    enable_coverage: bool = False,
) -> tuple[Path, subprocess.CompletedProcess, Path | None]:
    assert test_framework in ["pytest", "unittest"]
    coverage_out_file = None
    if test_framework == "pytest":
        test_files = []
        for file in test_paths.test_files:
            if file.test_type == TestType.REPLAY_TEST:
                test_files.append(
                    str(file.instrumented_file_path) + "::" + only_run_these_test_functions[file.instrumented_file_path]
                )
            else:
                test_files.append(str(file.instrumented_file_path))
        pytest_cmd_list = shlex.split(pytest_cmd, posix=is_posix)

        common_pytest_args = [
            "--capture=tee-sys",
            f"--timeout={pytest_timeout}",
            "-q",
            f"--codeflash_seconds={pytest_target_runtime_seconds}",
            "--codeflash_loops_scope=session",
        ]
        pytest_test_env = test_env.copy()
        pytest_test_env["PYTEST_PLUGINS"] = "codeflash.verification.pytest_plugin"

        if enable_coverage:
            coverage_out_file, coveragercfile = prepare_coverage_files()

            pytest_ignore_files = ["--ignore-glob=build/*", "--ignore-glob=dist/*", "--ignore-glob=*.egg-info/*"]

            coverage_args = ["--codeflash_min_loops=1", "--codeflash_max_loops=1"]

            cov_erase = execute_test_subprocess(
                shlex.split(f"{sys.executable} -m coverage erase"), cwd=cwd, env=pytest_test_env
            )  # this cleanup is necessary to avoid coverage data from previous runs, if there are any, then the current run will be appended to the previous data, which skews the results
            logger.debug(cov_erase)

            files = [
                str(file.instrumented_file_path)
                for file in test_paths.test_files
                if file.test_type == TestType.GENERATED_REGRESSION
            ]

            cov_run = execute_test_subprocess(
                shlex.split(f"{sys.executable} -m coverage run --rcfile={coveragercfile} -m pytest")
                + files
                + common_pytest_args
                + coverage_args
                + pytest_ignore_files,
                cwd=cwd,
                env=pytest_test_env,
            )
            logger.debug(cov_run)

            cov_report = execute_test_subprocess(
                shlex.split(f"{sys.executable} -m coverage json --rcfile={coveragercfile}"),
                cwd=cwd,
                env=pytest_test_env,
            )  # this will generate a json file with the coverage data
            logger.debug(cov_report)
        result_file_path = get_run_tmp_file(Path("pytest_results.xml"))
        result_args = [f"--junitxml={result_file_path}", "-o", "junit_logging=all"]

        results = execute_test_subprocess(
            pytest_cmd_list
            + test_files
            + common_pytest_args
            + result_args
            + [f"--codeflash_min_loops={pytest_min_loops}", f"--codeflash_max_loops={pytest_max_loops}"],
            cwd=cwd,
            env=pytest_test_env,
            timeout=600,  # TODO: Make this dynamic
        )
    elif test_framework == "unittest":
        result_file_path = get_run_tmp_file(Path("unittest_results.xml"))
        unittest_cmd_list = [sys.executable, "-m", "xmlrunner"]
        log_level = ["-v"] if verbose else []
        files = [str(file.instrumented_file_path) for file in test_paths.test_files]
        output_file = ["--output-file", str(result_file_path)]

        results = execute_test_subprocess(
            unittest_cmd_list + log_level + files + output_file, cwd=cwd, env=test_env, timeout=600
        )

    else:
        raise ValueError("Invalid test framework -- I only support Pytest and Unittest currently.")

    return result_file_path, results, coverage_out_file if enable_coverage else None
