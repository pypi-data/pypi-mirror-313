from __future__ import annotations

import logging
import os
import sys
import sysconfig
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from string import Template

from distlib.version import NormalizedVersion  # type: ignore[import-untyped]

from .. import __version__
from ..common import PackageInfo
from .cmd_runner import CommandRunner

logger = logging.getLogger(__name__)


@dataclass
class CMakeSettings:
    working_dir: Path
    source_path: Path
    build_path: Path
    os: str
    find_python: bool
    find_python3: bool
    minimum_required: str
    generator_platform: str | None
    command: Path = Path("cmake")


@dataclass
class CMakeConfigureSettings:
    environment: dict
    build_type: str | None
    options: dict[str, str]
    args: list[str]
    preset: str | None
    generator: str | None
    make_program: Path | None
    cross_compiling: bool
    toolchain_file: Path | None
    python_prefix: Path | None
    python_library: Path | None
    python_include_dir: Path | None
    python_interpreter_id: str | None


@dataclass
class CMakeBuildSettings:
    args: list[str]
    tool_args: list[str]
    presets: list[str]
    configs: list[str]


@dataclass
class CMakeInstallSettings:
    args: list[str]
    configs: list[str]
    components: list[str]
    prefix: Path | None


@dataclass
class Option:
    name: str
    value: str
    type: str = "STRING"
    description: str = ""


class CMaker:
    def __init__(
        self,
        cmake_settings: CMakeSettings,
        conf_settings: CMakeConfigureSettings,
        build_settings: CMakeBuildSettings,
        install_settings: CMakeInstallSettings,
        package_info: PackageInfo,
        runner: CommandRunner,
    ):
        self.cmake_settings = cmake_settings
        self.conf_settings = conf_settings
        self.build_settings = build_settings
        self.install_settings = install_settings
        self.package_info = package_info
        self.runner = runner
        self.environment: dict[str, str] | None = None

    def run(self, *args, **kwargs):
        return self.runner.run(*args, **kwargs)

    def prepare_environment(self):
        """Copy of the current environment with the variables defined in the
        user's configuration settings."""
        if self.environment is None:
            self.environment = os.environ.copy()
            self.environment["PY_BUILD_CMAKE_VERSION"] = str(__version__)
            self.environment["PY_BUILD_CMAKE_BINARY_DIR"] = str(
                self.cmake_settings.build_path
            )
            if self.install_settings.prefix is not None:
                self.environment["PY_BUILD_CMAKE_INSTALL_PREFIX"] = str(
                    self.install_settings.prefix
                )
            if self.conf_settings.environment:
                for k, v in self.conf_settings.environment.items():
                    templ = Template(v)
                    self.environment[k] = templ.substitute(self.environment)
        return self.environment

    def cross_compiling(self) -> bool:
        return self.conf_settings.cross_compiling

    def get_configure_options_package(self) -> list[Option]:
        """Flags specific to py-build-cmake, useful in the user's CMake scripts."""
        return [
            Option("PY_BUILD_CMAKE_VERSION", str(__version__)),
            Option("PY_BUILD_CMAKE_PACKAGE_VERSION", self.package_info.version),
            Option("PY_BUILD_CMAKE_PACKAGE_NAME", self.package_info.norm_name),
            Option("PY_BUILD_CMAKE_MODULE_NAME", self.package_info.module_name),
        ]

    def get_native_python_abi_tuple(self):
        cmake_version = self.cmake_settings.minimum_required
        has_t_flag = NormalizedVersion("3.30") <= NormalizedVersion(cmake_version)
        dmu = "dmut" if has_t_flag else "dmu"
        return ";".join("ON" if c in sys.abiflags else "OFF" for c in dmu)

    def get_native_python_implementation(self) -> str | None:
        return {
            "cpython": "CPython",
            "pypy": "PyPy",
        }.get(sys.implementation.name)

    def get_native_python_hints(self, prefix):
        """FindPython hints and artifacts for this (native) Python installation."""
        yield Option(prefix + "_ROOT_DIR", Path(sys.prefix).as_posix())
        impl = self.get_native_python_implementation()
        if impl:
            yield Option(prefix + "_FIND_IMPLEMENTATIONS", impl)
        if impl == "PyPy":
            inc = sysconfig.get_path("platinclude")
            if inc:
                yield Option(prefix + "_INCLUDE_DIR", Path(inc).as_posix())
        return
        # FIND_ABI seems to confuse CMake
        yield Option(prefix + "_FIND_ABI", self.get_native_python_abi_tuple())

    def get_cross_python_hints(self, prefix):
        """FindPython hints and artifacts to set when cross-compiling."""
        if self.conf_settings.python_prefix:
            pfx = self.conf_settings.python_prefix.as_posix()
            yield Option(prefix + "_ROOT_DIR", pfx, "PATH")
        if self.conf_settings.python_library:
            lib = self.conf_settings.python_library.as_posix()
            yield Option(prefix + "_LIBRARY", lib, "FILEPATH")
        if self.conf_settings.python_include_dir:
            inc = self.conf_settings.python_include_dir.as_posix()
            yield Option(prefix + "_INCLUDE_DIR", inc, "PATH")
        if self.conf_settings.python_interpreter_id:
            id = self.conf_settings.python_interpreter_id
            yield Option(prefix + "_INTERPRETER_ID", id, "STRING")

    def get_configure_options_python(self) -> list[Option]:
        """Flags to help CMake find the right version of Python."""

        def get_opts(prefix):
            executable = Path(sys.executable).as_posix()
            yield Option(prefix + "_EXECUTABLE", executable, "FILEPATH")
            yield Option(prefix + "_FIND_REGISTRY", "NEVER")
            yield Option(prefix + "_FIND_FRAMEWORK", "NEVER")
            yield Option(prefix + "_FIND_STRATEGY", "LOCATION")
            yield Option(prefix + "_FIND_VIRTUALENV", "FIRST")
            if not self.cross_compiling():
                yield from self.get_native_python_hints(prefix)
            else:
                yield from self.get_cross_python_hints(prefix)

        opts = []
        if self.cmake_settings.find_python:
            opts += list(get_opts("Python"))
        if self.cmake_settings.find_python3:
            opts += list(get_opts("Python3"))
        return opts

    def get_configure_options_install(self) -> list[Option]:
        prefix = self.install_settings.prefix
        if prefix:
            return [
                Option("CMAKE_INSTALL_PREFIX", prefix.as_posix(), "PATH"),
                Option("CMAKE_FIND_NO_INSTALL_PREFIX", "On", "BOOL"),
            ]
        return []

    def get_configure_options_make(self) -> list[Option]:
        """Sets CMAKE_MAKE_PROGRAM."""
        if self.conf_settings.make_program:
            opt = Option(
                "CMAKE_MAKE_PROGRAM",
                self.conf_settings.make_program.as_posix(),
                "FILEPATH",
            )
            return [opt]
        return []

    def get_configure_options_toolchain(self) -> list[str]:
        """Sets CMAKE_TOOLCHAIN_FILE."""
        return (
            ["CMAKE_TOOLCHAIN_FILE:FILEPATH=" + str(self.conf_settings.toolchain_file)]
            if self.conf_settings.toolchain_file
            else []
        )

    def get_configure_options_settings(self) -> list[str]:
        return [k + "=" + v for k, v in self.conf_settings.options.items()]

    def get_configure_options(self) -> list[str]:
        """Get the list of options (-D) passed to the CMake configure step
        through the command line."""
        return (
            self.get_configure_options_toolchain()
            + self.get_configure_options_settings()
        )

    def get_preload_options(self) -> list[Option]:
        """Get the list of options set in the CMake pre-load script (-C)."""
        return (
            self.get_configure_options_package()
            + self.get_configure_options_make()
            + self.get_configure_options_python()
            + self.get_configure_options_install()
        )

    def write_preload_options(self) -> list[str]:
        """Write the options into the CMake pre-load script and return the
        command-line flags that tell CMake to load it."""
        opts = self.get_preload_options()
        if not opts:
            return []

        def fmt_opt(o: Option):
            return (
                f'set({o.name} "{o.value}"'
                f' CACHE {o.type} "{o.description}" FORCE)\n'
            )

        preload_file = self.cmake_settings.build_path / "py-build-cmake-preload.cmake"
        version = self.cmake_settings.minimum_required
        if self.runner.verbose:
            print("Writing CMake pre-load file")
            print(f"{preload_file}")
            print("---------------------------")
            print(f"cmake_minimum_required(VERSION {version})")
            for o in opts:
                print(fmt_opt(o), end="")
            print("---------------------------\n")
        if not self.runner.dry:
            self.cmake_settings.build_path.mkdir(parents=True, exist_ok=True)
            with preload_file.open("w", encoding="utf-8") as f:
                f.write(f"cmake_minimum_required(VERSION {version})\n")
                for o in opts:
                    f.write(fmt_opt(o))
        return ["-C", str(preload_file)]

    def get_cmake_generator_platform(self) -> list[str]:
        """Returns -A <platform> for the Visual Studio generator on Windows."""
        win = self.cmake_settings.os == "windows"
        gen = self.conf_settings.generator
        vs_gen = win and (not gen or gen.lower().startswith("visual studio"))
        cmake_plat = self.cmake_settings.generator_platform
        if vs_gen and cmake_plat:
            return ["-A", cmake_plat]
        return []

    def get_configure_command(self):
        options = self.get_configure_options()
        cmd = [str(self.cmake_settings.command)]
        cmd += ["-S", str(self.cmake_settings.source_path)]
        if self.conf_settings.preset:
            cmd += ["--preset", self.conf_settings.preset]
        if not self.conf_settings.preset or not self.build_settings.presets:
            cmd += ["-B", str(self.cmake_settings.build_path)]
        if self.conf_settings.generator:
            cmd += ["-G", self.conf_settings.generator]
        cmd += self.get_cmake_generator_platform()
        cmd += self.write_preload_options()
        cmd += [f for opt in options for f in ("-D", opt)]
        cmd += self.conf_settings.args
        return cmd

    def get_working_dir(self):
        cwd = self.cmake_settings.working_dir
        return str(cwd) if cwd is not None else None

    def configure(self):
        env = self.prepare_environment()
        cmd = self.get_configure_command()
        cwd = self.get_working_dir()
        self.run(cmd, cwd=cwd, check=True, env=env)

    def get_build_command(self, config, preset):
        cmd = [str(self.cmake_settings.command), "--build"]
        if preset is not None:
            cmd += ["--preset", preset]
        else:
            cmd += [str(self.cmake_settings.build_path)]
        if config is not None:
            cmd += ["--config", config]
        if self.build_settings.args:
            cmd += self.build_settings.args
        if self.build_settings.tool_args:
            cmd += ["--", *self.build_settings.tool_args]
        return cmd

    def get_build_commands(self):
        presets = self.build_settings.presets or [None]
        configs = self.build_settings.configs or [None]
        for preset, config in product(presets, configs):
            yield self.get_build_command(config, preset)

    def build(self):
        env = self.prepare_environment()
        cwd = self.get_working_dir()
        for cmd in self.get_build_commands():
            self.run(cmd, cwd=cwd, check=True, env=env)

    def get_install_command(self, config):
        for component in self.install_settings.components:
            cmd = [str(self.cmake_settings.command), "--install"]
            cmd += [str(self.cmake_settings.build_path)]
            if self.install_settings.prefix:
                cmd += ["--prefix", str(self.install_settings.prefix)]
            if config is not None:
                cmd += ["--config", config]
            if component:
                cmd += ["--component", component]
            if self.install_settings.args:
                cmd += self.install_settings.args
            yield cmd

    def get_install_commands(self):
        for config in self.install_settings.configs or [None]:
            yield from self.get_install_command(config)

    def install(self):
        env = self.prepare_environment()
        cwd = self.get_working_dir()
        for cmd in self.get_install_commands():
            self.run(cmd, cwd=cwd, check=True, env=env)
