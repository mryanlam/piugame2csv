load("@my_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_binary(
    name = "cli",
    srcs = ["cli.py"],
    deps = [
        requirement("Typer"),
        ":piugame2csv",
    ],
)

py_library(
    name = "piugame2csv",
    srcs = ["piugame2csv.py"],
    deps = [
        requirement("beautifulsoup4"),
        requirement("requests"),
    ],
)
