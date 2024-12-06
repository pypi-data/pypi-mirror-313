from __future__ import annotations

import os
import platform
from collections.abc import Callable, Collection, Generator
from contextlib import contextmanager
from io import TextIOBase
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from threading import Event, Thread
from typing import IO, Final, TextIO, final

from _atoti_core import LICENSE_KEY_ENV_VAR_NAME, LicenseKeyLocation, get_atoti_home

from ._get_java_executable_path import get_java_executable_path
from ._resources_directory import RESOURCES_DIRECTORY
from ._supported_java_version import SUPPORTED_JAVA_VERSION
from ._wait_for_matching_output import wait_for_matching_output

_ADD_OPENS: Collection[str] = [
    # Arrow reflexive access: https://github.com/activeviam/activepivot/pull/4297/files#diff-d9ef6fa90dda49aa1ec2907eba7be19c916c5f553c9846b365d30a307740aea2
    "--add-opens=java.base/java.nio=ALL-UNNAMED",
    # Py4J reflexive access: java.lang.reflect.InaccessibleObjectException: Unable to make public java.lang.Object[] java.util.HashMap$KeySet.toArray() accessible: module java.base does not "opens java.util" to unnamed module @647fd8ce
    "--add-opens=java.base/java.util=ALL-UNNAMED",
    "--add-opens=java.base/java.lang=ALL-UNNAMED",
]

_COMMUNITY_LICENSE_KEY_PATH = RESOURCES_DIRECTORY / "community.lic"

_SERVER_JAR_PATH = RESOURCES_DIRECTORY / "server.jar"

_HADOOP_DIRECTORY = RESOURCES_DIRECTORY / "hadoop-3.2.1"

# Keep in sync with Java's ApplicationStarter.BIND_ADDRESS_ARGUMENT
_BIND_ADDRESS_ARGUMENT = "--bind-address"
# Keep in sync with Java's ApplicationStarter.ENABLE_AUTH_OPTION.
_ENABLE_AUTH_OPTION = "--enable-auth"

# Keep in sync with Java's ServerUtils.serverStarted().
_PY4J_SERVER_STARTED_PATTERN = (
    r"Py4J server started on port (?P<port>\d+)(?: with auth token (?P<token>.+))?$"
)


def _get_logs_directory(session_directory: Path, /) -> Path:
    return session_directory / "logs"


def _create_session_directory(*, session_id: str) -> Path:
    session_directory = get_atoti_home() / session_id
    _get_logs_directory(session_directory).mkdir(parents=True)
    return session_directory


def _get_command(
    *,
    address: str | None,
    enable_py4j_auth: bool,
    extra_jars: Collection[Path],
    java_executable_path: Path,
    java_options: Collection[str],
    log_to_stdout: bool,
    port: int,
    py4j_server_port: int | None,
    session_directory: Path,
) -> list[Path | str]:
    command: list[Path | str] = [
        java_executable_path,
        "-jar",
        *_ADD_OPENS,
        f"-Dserver.port={port}",  # spell-checker: disable-line
        f"-Dserver.session_directory={session_directory}",  # spell-checker: disable-line
        "-Dactiveviam.feature.experimental.experimental_copper.enabled=true",  # spell-checker: disable-line
        # Remove following line in 0.9.0.
        "-Dactiveviam.feature.experimental.copper_in_distributed_cube.enabled=true",  # spell-checker: disable-line
        "-Dactiveviam.feature.experimental.allow_change_measure_type.enabled=true",  # spell-checker: disable-line
        # The user is allowed to pass any options to Java, even dangerous ones.
        *java_options,
    ]

    if not log_to_stdout:
        command.append(
            "-Dserver.logging.disable_console_logging=true",  # spell-checker: disable-line
        )

    if platform.system() == "Windows":
        command.append(
            f"-Dhadoop.home.dir={_HADOOP_DIRECTORY}",  # spell-checker: disable-line
        )
        hadoop_path = str(_HADOOP_DIRECTORY / "bin")
        if hadoop_path not in os.environ["PATH"]:
            os.environ["PATH"] = f"{os.environ['PATH']};{hadoop_path}"

    extra_jar_paths = [
        *[
            jar_path
            for jar_path in RESOURCES_DIRECTORY.glob("*.jar")
            if jar_path != _SERVER_JAR_PATH
        ],
        *extra_jars,
    ]
    command.append(
        f"-Dloader.path={','.join([str(jar_path) for jar_path in extra_jar_paths])}",  # spell-checker: disable-line
    )

    if py4j_server_port is not None:
        command.append(f"-Dpy4j.port={py4j_server_port}")

    command.append(_SERVER_JAR_PATH)

    if address is not None:
        command.append(f"{_BIND_ADDRESS_ARGUMENT}={address}")

    if enable_py4j_auth:
        command.append(_ENABLE_AUTH_OPTION)

    return command


def _get_env(
    *,
    license_key: LicenseKeyLocation | str,
) -> dict[str, str] | None:
    match license_key:
        case LicenseKeyLocation.EMBEDDED:
            assert _COMMUNITY_LICENSE_KEY_PATH.exists()
            return _get_env(license_key=str(_COMMUNITY_LICENSE_KEY_PATH))
        case LicenseKeyLocation.ENVIRONMENT:
            return None
        case str():
            return {**os.environ, LICENSE_KEY_ENV_VAR_NAME: license_key}


def _copy_stream(
    input_stream: IO[str],
    output_stream: TextIO | TextIOBase | None = None,
    *,
    should_stop: Callable[[], bool],
) -> None:
    for line in input_stream:
        if output_stream and not output_stream.closed:
            output_stream.write(line)
        if should_stop():
            break
    if not input_stream.closed:
        input_stream.close()


@final
class ServerSubprocess:
    @contextmanager
    @staticmethod
    def create(
        *,
        address: str | None = None,
        enable_py4j_auth: bool = True,
        extra_jars: Collection[Path] = (),
        java_options: Collection[str] = (),
        license_key: LicenseKeyLocation | str,
        logs_destination: Path | TextIO | TextIOBase | None = None,
        port: int = 0,
        py4j_server_port: int | None = None,
        session_id: str,
    ) -> Generator[ServerSubprocess, None, None]:
        java_executable_path = get_java_executable_path(
            supported_java_version=SUPPORTED_JAVA_VERSION,
        )

        session_directory = _create_session_directory(session_id=session_id)

        match logs_destination:
            case Path():
                logs_path: Path | None = logs_destination
            case TextIO() | TextIOBase():
                logs_path = None
            case None:
                logs_path = _get_logs_directory(session_directory) / "server.log"

        command = _get_command(
            address=address,
            enable_py4j_auth=enable_py4j_auth,
            extra_jars=extra_jars,
            java_executable_path=java_executable_path,
            java_options=java_options,
            log_to_stdout=isinstance(logs_destination, TextIOBase),
            port=port,
            py4j_server_port=py4j_server_port,
            session_directory=session_directory,
        )
        env = _get_env(license_key=license_key)

        process = Popen(  # noqa: S603
            command,
            env=env,
            stderr=STDOUT,
            stdout=PIPE,
            text=True,
        )

        try:
            match, startup_output = wait_for_matching_output(
                _PY4J_SERVER_STARTED_PATTERN,
                process=process,
            )

            py4j_auth_token = match.group("token")
            py4j_java_port = int(match.group("port"))

            if isinstance(logs_destination, TextIOBase):
                logs_destination.write(startup_output)
            else:
                startup_log_path = (
                    _get_logs_directory(session_directory) / "startup.log"
                )
                startup_log_path.write_text(startup_output, encoding="utf8")

            stop_event = Event()
            output_copier = Thread(
                target=_copy_stream,
                args=(
                    process.stdout,
                    logs_destination
                    if isinstance(logs_destination, TextIO | TextIOBase)
                    else None,
                ),
                kwargs={"should_stop": stop_event.is_set},
                daemon=True,
            )
            output_copier.start()

            server_subprocess = ServerSubprocess(
                logs_path=logs_path,
                process=process,
                py4j_auth_token=py4j_auth_token,
                py4j_java_port=py4j_java_port,
            )
            try:
                yield server_subprocess
            finally:
                stop_event.set()
        finally:
            process.terminate()
            process.wait()

    def __init__(
        self,
        *,
        logs_path: Path | None,
        process: Popen[str],
        py4j_auth_token: str | None,
        py4j_java_port: int,
    ) -> None:
        self._logs_path: Final = logs_path
        self._process = process
        self.py4j_auth_token: Final = py4j_auth_token
        self.py4j_java_port: Final = py4j_java_port

    @property
    def logs_path(self) -> Path:
        if not self._logs_path:
            raise RuntimeError("Logs are not being written to a file.")

        return self._logs_path

    @property
    def pid(self) -> int:
        return self._process.pid

    def wait(self) -> None:
        """Wait for the process to terminate.

        This will prevent the Python process from exiting.
        If the Py4J gateway is closed the Atoti server will stop itself anyway.
        """
        self._process.wait()
