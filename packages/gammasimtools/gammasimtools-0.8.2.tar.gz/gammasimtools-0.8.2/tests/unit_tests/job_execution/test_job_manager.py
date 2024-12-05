import logging
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

import simtools.job_execution.job_manager as jm
from simtools.job_execution.job_manager import JobExecutionError

LOG_EXCERPT = "log excerpt"
OS_SYSTEM = "os.system"
PATHLIB_PATH_EXISTS = "pathlib.Path.exists"

logger = logging.getLogger()


@pytest.fixture
def job_submitter():
    submitter = jm.JobManager()
    submitter._logger = MagicMock()
    submitter.submit_engine = "local"
    submitter.test = True
    return submitter


@pytest.fixture
def output_log():
    """Fixture for the output log file."""
    return Path("output.log")


@pytest.fixture
def logfile_log():
    """Fixture for the general log file."""
    return Path("logfile.log")


@pytest.fixture
def script_file():
    """Fixture for the script file."""
    return Path("script.sh")


@pytest.fixture
def job_messages(script_file):
    """Fixture for the script message."""
    return {
        "script_message": f"Submitting script {script_file}",
        "job_output": "Job output stream output.out",
        "job_error_stream": "Job error stream output.err",
        "job_log_stream": "Job log stream output.job",
        "running_locally": "Running script locally",
        "log_excerpt": LOG_EXCERPT,
    }


def test_test_submission_system():
    jm.JobManager(submit_engine=None)
    jm.JobManager(submit_engine="local")


def test_submit_engine():
    j = jm.JobManager()
    assert j.submit_engine == "local"
    for engine in ["local", "htcondor", "gridengine"]:
        j.submit_engine = engine
        assert j.submit_engine == engine

    with pytest.raises(ValueError, match="Invalid submit command: abc"):
        j.submit_engine = "abc"


@patch("simtools.job_execution.job_manager.gen.program_is_executable", return_value=True)
def test_check_submission_system(mock_program_is_executable, job_submitter):
    job_submitter.submit_engine = "local"
    job_submitter.check_submission_system()
    job_submitter.submit_engine = "test_wms"
    job_submitter.check_submission_system()
    job_submitter.submit_engine = "htcondor"
    job_submitter.check_submission_system()
    assert job_submitter._logger.error.call_count == 0


@patch("simtools.utils.general")
def test_submit_local(
    mock_gen, job_submitter, mocker, output_log, logfile_log, script_file, job_messages
):
    mocker.patch(OS_SYSTEM, return_value=0)
    mock_gen.get_log_excerpt.return_value = LOG_EXCERPT
    mocker.patch(PATHLIB_PATH_EXISTS, return_value=False)

    job_submitter.submit(script_file, output_log, logfile_log)

    job_submitter._logger.info.assert_any_call(job_messages["script_message"])
    job_submitter._logger.info.assert_any_call(job_messages["job_output"])
    job_submitter._logger.info.assert_any_call(job_messages["job_error_stream"])
    job_submitter._logger.info.assert_any_call(job_messages["job_log_stream"])
    job_submitter._logger.info.assert_any_call(job_messages["running_locally"])
    job_submitter._logger.info.assert_any_call("Testing (local)")


@patch("simtools.utils.general")
def test_submit_htcondor(mock_gen, job_submitter, mocker, output_log, logfile_log, script_file):
    job_submitter.submit_engine = "htcondor"
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)
    mock_execute = mocker.patch.object(job_submitter, "_execute")

    job_submitter.submit(script_file, output_log, logfile_log)

    mock_execute.assert_called_with(
        "htcondor", job_submitter.engines["htcondor"] + f" {script_file}.condor"
    )
    mock_file().write.assert_has_calls(
        [call(f"Executable = {script_file}\n"), call("Output = output.out\n")],
        any_order=True,
    )

    # extra submit options
    job_submitter.submit_options = "max_materialize = 800, priority = 5"
    job_submitter.submit(script_file, output_log, logfile_log)
    mock_file().write.assert_has_calls(
        [
            call(f"Executable = {script_file}\n"),
            call("Output = output.out\n"),
            call("max_materialize = 800\n"),
            call("priority = 5\n"),
        ],
        any_order=True,
    )


def mock_open_side_effect(*args, **kwargs):
    """Mock open function that raises FileNotFoundError when the file is opened in write mode."""
    if "w" in args[1] or "w" in kwargs.get("mode", ""):
        raise FileNotFoundError(f"No such file or directory: {args[0]}")
    return mock_open()(*args, **kwargs)


@patch("builtins.open", side_effect=mock_open_side_effect)
def test_submit_htcondor_no_script(mock_gen, job_submitter, mocker, output_log, logfile_log):
    job_submitter.submit_engine = "htcondor"

    with pytest.raises(JobExecutionError):
        job_submitter.submit("invalid_path/non_existent_script.sh", output_log, logfile_log)

    job_submitter._logger.error.assert_any_call(
        "Failed creating condor submission file invalid_path/non_existent_script.sh.condor"
    )


@patch("simtools.utils.general")
def test_submit_gridengine(mock_gen, job_submitter, mocker, output_log, logfile_log, script_file):
    job_submitter.submit_engine = "gridengine"
    mock_execute = mocker.patch.object(job_submitter, "_execute")

    job_submitter.submit(script_file, output_log, logfile_log)

    expected_command = (
        f"{job_submitter.engines['gridengine']} -o output.out -e output.err script.sh"
    )
    mock_execute.assert_called_with("gridengine", expected_command)


@patch("simtools.job_execution.job_manager.os.system")
def test_execute(mock_os_system, job_submitter, job_submitter_real):

    shell_command = "echo Hello World"
    job_submitter._execute("local", shell_command)

    job_submitter._logger.info.assert_any_call("Submitting script to local")
    job_submitter._logger.debug.assert_called_with(shell_command)
    job_submitter._logger.info.assert_any_call("Testing (local)")
    job_submitter._logger.info.assert_any_call(shell_command)

    job_submitter_real._execute("local", shell_command)
    mock_os_system.assert_called_once_with(shell_command)


@pytest.fixture
def job_submitter_real():
    submitter = jm.JobManager()
    submitter._logger = MagicMock()
    submitter.submit_engine = "local"
    submitter.test = False
    return submitter


@patch("simtools.utils.general")
def test_submit_local_real(
    mock_gen, job_submitter_real, mocker, output_log, logfile_log, script_file, job_messages
):
    mock_system = mocker.patch(OS_SYSTEM, return_value=0)
    mock_gen.get_log_excerpt.return_value = job_messages["log_excerpt"]
    mocker.patch(PATHLIB_PATH_EXISTS, return_value=False)

    job_submitter_real.submit(script_file, output_log, logfile_log)

    job_submitter_real._logger.info.assert_any_call(job_messages["script_message"])
    job_submitter_real._logger.info.assert_any_call(job_messages["job_output"])
    job_submitter_real._logger.info.assert_any_call(job_messages["job_error_stream"])
    job_submitter_real._logger.info.assert_any_call(job_messages["job_log_stream"])
    job_submitter_real._logger.info.assert_any_call(job_messages["running_locally"])
    mock_system.assert_called_with(f"{script_file} > output.out 2> output.err")


@patch("simtools.utils.general")
def test_submit_local_real_failure(
    mock_gen, job_submitter_real, mocker, output_log, logfile_log, script_file, job_messages
):
    mock_system = mocker.patch(OS_SYSTEM, return_value=1)
    mock_gen.get_log_excerpt.return_value = job_messages["log_excerpt"]
    mocker.patch(PATHLIB_PATH_EXISTS, return_value=True)
    mock_gen.get_file_age.return_value = 4

    mocker.patch("simtools.utils.general.get_log_excerpt", return_value=LOG_EXCERPT)
    mocker.patch("simtools.utils.general.get_file_age", return_value=4)

    with patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(JobExecutionError):
            job_submitter_real.submit(script_file, output_log, logfile_log)

    job_submitter_real._logger.info.assert_any_call(job_messages["script_message"])
    job_submitter_real._logger.info.assert_any_call(job_messages["job_output"])
    job_submitter_real._logger.info.assert_any_call(job_messages["job_error_stream"])
    job_submitter_real._logger.info.assert_any_call(job_messages["job_log_stream"])
    job_submitter_real._logger.info.assert_any_call(job_messages["running_locally"])
    mock_system.assert_called_with(f"{script_file} > output.out 2> output.err")
    job_submitter_real._logger.error.assert_any_call(job_messages["log_excerpt"])
