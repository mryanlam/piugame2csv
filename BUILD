load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

py_binary(
    name = "cli",
    srcs = ["cli.py"],
    deps = [
        ":piugame2csv",
        "@pypi//typer:pkg",
    ],
)

py_library(
    name = "piugame2csv",
    srcs = ["piugame2csv.py"],
    deps = [
        "@pypi//beautifulsoup4:pkg",
        "@pypi//requests:pkg",
    ],
)

# This rule adds a convenient way to update the requirements file.
compile_pip_requirements(
    name = "requirements",
    src = "requirements.in",
    requirements_txt = "requirements_lock.txt",
    requirements_windows = "requirements_windows.txt",
)
