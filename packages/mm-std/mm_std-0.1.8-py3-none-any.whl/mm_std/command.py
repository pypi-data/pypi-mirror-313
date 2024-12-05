import subprocess  # nosec
from dataclasses import dataclass


@dataclass
class CommandResult:
    stdout: str
    stderr: str
    code: int

    @property
    def out(self) -> str:
        if self.stdout:
            return self.stdout + "\n" + self.stderr
        return self.stderr


def run_command(cmd: str, timeout: int | None = 60, capture_output: bool = True, echo_cmd_console: bool = False) -> CommandResult:
    if echo_cmd_console:
        print(cmd)  # noqa: T201
    try:
        process = subprocess.run(cmd, timeout=timeout, capture_output=capture_output, shell=True, check=False)  # nosec
        stdout = process.stdout.decode("utf-8") if capture_output else ""
        stderr = process.stderr.decode("utf-8") if capture_output else ""
        return CommandResult(stdout=stdout, stderr=stderr, code=process.returncode)
    except subprocess.TimeoutExpired:
        return CommandResult(stdout="", stderr="timeout", code=124)


def run_ssh_command(host: str, cmd: str, ssh_key_path: str | None = None, timeout: int = 60) -> CommandResult:
    ssh_cmd = "ssh -o 'StrictHostKeyChecking=no' -o 'LogLevel=ERROR'"
    if ssh_key_path:
        ssh_cmd += f" -i {ssh_key_path} "
    ssh_cmd += f" {host} {cmd}"
    return run_command(ssh_cmd, timeout=timeout)
