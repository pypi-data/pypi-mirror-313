# -*- encoding: utf-8 -*-
import contextlib
import os
import platform
import random
import re
import shutil
import string
import subprocess
import sys
import typing as t

import click
import psutil
from click import testing
from flask import Flask

__all__ = [
    "app_cli_runner",
    "check_output",
    "click_echo",
    "click_exit",
    "conda_command",
    "conda_executable",
    "conda_info",
    "init_conda",
    "new_conda_env",
    "pip_freeze",
    "pip_reqs",
    "pip_show",
    "platform_uname",
    "random_string",
    "run_command",
    "run_subprocess",
    "sample_string",
]


def sample_string(source: str, num: int) -> str:
    return "".join([random.choice(source) for _ in range(num)])


def random_string(num: int = 8) -> str:
    first_char = sample_string(string.ascii_letters, 1)
    return first_char + sample_string(string.ascii_letters + string.digits, num - 1)


def platform_uname(conda_env: str) -> str:
    script = "\"import sys; print(f'{sys.version_info.major}{sys.version_info.minor}');\""
    result = check_output(conda_executable("python", "-c", script, conda_env=conda_env), echo=False)
    assert len(result) >= 1

    if sys.platform == "win32":
        return f"cp{result[0]}-win_{platform.machine().lower()}"
    elif sys.platform == "linux":
        return f"cpython-{result[0]}-{platform.machine().lower()}-linux"
    elif sys.platform == "darwin":
        return f"cpython-{result[0]}-darwin"
    else:
        raise Exception(f"platform not support: {platform.uname()}")


def click_echo(message: str, err: bool = False, fg: str | None = None):
    if err is True:
        click.echo(click.style(message, fg=fg or "red"))
    else:
        click.echo(click.style(message, fg=fg))


def click_exit(message: str, return_code: int = 1):
    click_echo(message, err=True)
    sys.exit(return_code)


def app_cli_runner(app: Flask, *args: str):
    with app.app_context():
        runner = app.test_cli_runner()
        result: testing.Result = runner.invoke(args=args)
        if result.stdout_bytes:
            print(result.stdout_bytes.decode(errors="ignore"))
        if result.stderr_bytes:
            print(result.stderr_bytes.decode(errors="ignore"))


def run_command(*args: str, echo: bool = True, executable: str | None = None) -> int:
    if executable is None:
        command = " ".join(args)
    else:
        command = f'{executable} {" ".join(args)}'

    if echo is True:
        print(">>>", command)
    return os.system(command)


def run_subprocess(
    *args: str,
    echo: bool = True,
    shell: bool = True,
    executable: str | None = None,
    detached: bool = False,
    priority: int | None = None,
) -> int:
    if echo is True:
        if executable is None:
            print(">>>", *args)
        else:
            print(">>>", executable, *args)

    kwargs: dict[str, t.Any] = dict()
    if sys.platform.startswith("win32"):
        kwargs.update(
            startupinfo=subprocess.STARTUPINFO(
                dwFlags=subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW,
                wShowWindow=subprocess.SW_HIDE,
            )
        )
        if detached is True:
            kwargs.update(creationflags=subprocess.DETACHED_PROCESS)
        else:
            kwargs.update(creationflags=subprocess.HIGH_PRIORITY_CLASS)
    else:
        raise Exception(f"platform not support: {sys.platform}")

    kwargs.update(
        shell=shell,
        executable=executable,
    )
    if detached is True:
        kwargs.update(
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        p = subprocess.Popen(" ".join(args), **kwargs)
        if priority is not None:
            psutil.Process(p.pid).nice(priority)
        return 0
    else:
        kwargs.update(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        p = subprocess.Popen(" ".join(args), **kwargs)
        if priority is not None:
            psutil.Process(p.pid).nice(priority)
        while True:
            if p.stdout is None:
                break

            output = p.stdout.readline()
            if not output and p.poll() is not None:
                break

            if isinstance(output, bytes):
                if len(output):
                    print(output.decode(errors="ignore"), end="")
            else:
                if len(output):
                    print(output, end="")

        while True:
            if p.stderr is None:
                break

            output = p.stderr.readline()
            if not output and p.poll() is not None:
                break

            if isinstance(output, bytes):
                if len(output):
                    print(output.decode(errors="ignore"), end="")
            else:
                if len(output):
                    print(output, end="")

        return p.poll() or 0


def check_output(
    *args: str,
    cwd: str | None = None,
    executable: str | None = None,
    echo: bool = True,
    shell: bool = True,
) -> list[str]:
    if cwd is None:
        cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    previous_cwd = os.getcwd()
    os.chdir(cwd)
    if echo is True:
        print(">>>", " ".join(args).replace("\r\n", "\\n").replace("\n", "\\n"))
    result = subprocess.check_output(" ".join(args), executable=executable, shell=shell)
    os.chdir(previous_cwd)
    if isinstance(result, (bytes, bytearray)):  # type: ignore
        text = result.decode(errors="ignore")
    elif isinstance(result, memoryview):  # type: ignore
        text = result.tobytes().decode(errors="ignore")
    else:
        text = result

    if echo is True:
        print(text)
    return re.split("\r?\n", text)


def conda_executable(*args: str, conda_env: str) -> str:
    if len(args) == 0:
        raise Exception("command_args not specified")

    if sys.platform.startswith("win32"):
        result = check_output("where conda", echo=False)
    else:
        result = check_output("which conda", echo=False)

    if len(result) == 0 or len(result[0]) == 0:
        click_exit("conda not found")

    conda_filename = result[0]

    result = check_output(f"{conda_filename} env list", echo=False)
    if not any((text.startswith(conda_env + " ") for text in result)):
        click_exit(f"entry_python not found: {conda_env}")

    if sys.platform.startswith("win32"):
        if re.match("^(python[3]?$|python[3]? )", args[0]):
            return os.path.abspath(os.path.join(os.path.dirname(conda_filename), f"../envs/{conda_env}")) + os.sep + " ".join(args)
        else:
            return os.path.abspath(os.path.join(os.path.dirname(conda_filename), f"../envs/{conda_env}/Scripts")) + os.sep + " ".join(args)
    else:
        return os.path.abspath(os.path.join(os.path.dirname(conda_filename), f"../envs/{conda_env}/bin")) + os.sep + " ".join(args)


def conda_command(
    *args: str,
    conda_env: str,
    shell: bool = True,
    echo: bool = True,
    detached: bool = False,
    priority: int | None = None,
) -> int:
    if echo is True:
        print(">>>", " ".join(args))

    command = conda_executable(*args, conda_env=conda_env)

    if detached is True:
        return run_subprocess(command, shell=shell, detached=True, priority=priority)

    if priority is not None:
        return run_subprocess(command, shell=shell, priority=priority)
    else:
        return run_command(command, echo=False)


def init_conda(env_name: str, python_version: str, force: bool = False, requirements_txt: str | None = None) -> int:
    if sys.platform.startswith("win32"):
        result = check_output("where conda", echo=False)
    else:
        result = check_output("which conda", echo=False)

    if len(result) == 0 or len(result[0]) == 0:
        click_exit("conda not found")

    conda_filename = result[0]

    result = check_output(f"{conda_filename} env list")
    print(f"\n{env_name}")
    print("=" * 32)

    ret = -1
    if any((text.startswith(env_name + " ") for text in result)):
        if force is True:
            ret = run_command(f"{conda_filename} remove -n {env_name} --all -y")
            environment_path = os.path.abspath(os.path.join(os.path.dirname(conda_filename), f"../envs/{env_name}"))
            if os.path.isdir(environment_path):
                shutil.rmtree(environment_path)
            ret = run_command(f"{conda_filename} create -q --no-default-packages --name {env_name} python={python_version} -y")
    else:
        ret = run_command(f"{conda_filename} create -q --no-default-packages --name {env_name} python={python_version} -y")

    if requirements_txt is not None:
        ret = conda_command(f'pip install --no-warn-script-location -r "{requirements_txt}"', conda_env=env_name)

    return ret


@contextlib.contextmanager
def new_conda_env(random_tag: str, python_version: str, *, requirements_txt: str | None = None) -> t.Iterator[str]:
    if not bool(re.fullmatch("\\d+\\.\\d+", python_version)):
        raise ValueError("invalid python_version, {}".format(python_version))

    conda_env = "{}_{}".format(random_tag, python_version.replace(".", ""))
    run_command(f"conda create -n {conda_env} python={python_version} -q -y")
    if requirements_txt is not None:
        conda_command(f"pip install --no-warn-script-location -q -r {requirements_txt}", conda_env=conda_env)
    try:
        yield conda_env
    finally:
        run_command(f"conda remove -n {conda_env} --all -q -y")


def conda_info() -> dict[str, str | list[str]]:
    result = check_output("conda info", echo=False)

    conda_info_dict: dict[str, list[str]] = dict()

    last_key: str | None = None
    sep = " : "
    for text in result:
        parts = text.split(sep)
        if len(parts) == 1:
            if last_key is not None and last_key in conda_info_dict:
                conda_info_dict[last_key].append(sep.join(parts).strip())
        elif len(parts) >= 2:
            last_key = parts[0].strip().replace(" ", "_")
            conda_info_dict[last_key] = [sep.join(parts[1:]).strip()]
        else:
            pass

    return {key: line_list if len(line_list) >= 2 else line_list[0] for key, line_list in conda_info_dict.items()}


def pip_show(package_name: str, conda_env: str) -> dict[str, str] | None:
    pip_filename = conda_executable("pip", conda_env=conda_env)
    result = check_output(f"{pip_filename} show {package_name}", echo=False)
    package_info_dict: dict[str, str] = dict()
    for text in result:
        parts = text.split(":")
        if len(parts) >= 2:
            package_info_dict[parts[0].strip()] = ":".join(parts[1:]).strip()

    if "Name" in package_info_dict and "Version" in package_info_dict:
        return package_info_dict
    else:
        return None


def pip_freeze(conda_env: str) -> dict[str, str]:
    pip_filename = conda_executable("pip", conda_env=conda_env)
    result = check_output(f"{pip_filename} freeze", echo=False)
    package_version_dict: dict[str, str] = dict()
    for text in result:
        parts = text.split("==")
        if len(parts) == 2:
            package_version_dict[parts[0].strip()] = parts[1].strip()
    return package_version_dict


def pip_reqs(requirements_txt: str, conda_env: str) -> None:
    pip_filename = conda_executable("pip", conda_env=conda_env)
    result = check_output(f"{pip_filename} freeze", echo=False)
    package_info_dict: dict[str, str] = dict()
    for text in result:
        parts = text.split("==")
        if len(parts) == 2:
            package_info_dict[parts[0].strip().lower()] = parts[1].strip()

    with open(requirements_txt, "r") as f:
        result = f.read().split("\n")

    line_list: list[str] = []
    for text in result:
        text = text.strip()
        if text.startswith("-r "):
            line_list.append(text)
            continue

        parts = text.split("==")
        if len(parts) == 2:
            package_name = parts[0].strip()
            package_version = parts[1].strip()
        else:
            package_name = text.strip()
            package_version = ""

        if not package_name:
            continue

        if package_name.lower() in package_info_dict:
            package_version = package_info_dict[package_name.lower()]

        if package_version:
            print("{}=={}".format(package_name, package_version))
            line_list.append("{}=={}".format(package_name, package_version))
        else:
            print("{}: not found".format(package_name))
            line_list.append(package_name)

    with open(requirements_txt, "w") as f:
        f.write("\n".join(line_list))
