import json
import os
import subprocess
import urllib.parse
from pathlib import Path

from .. import conf as osc_conf
from .. import oscerr


class GitStore:

    @classmethod
    def is_project_dir(cls, path):
        try:
            store = cls(path)
        except oscerr.NoWorkingCopy:
            return False
        return store.is_project

    @classmethod
    def is_package_dir(cls, path):
        try:
            store = cls(path)
        except oscerr.NoWorkingCopy:
            return False
        return store.is_package

    def __init__(self, path, check=True):
        self.path = path
        self.abspath = os.path.abspath(self.path)
        try:
            self.toplevel = self._run_git(["rev-parse", "--show-toplevel"])
            self.toplevel = os.path.abspath(self.toplevel)
        except subprocess.CalledProcessError:
            self.toplevel = None

        # TODO: how to determine if the current git repo contains a project or a package?
        self.is_project = False
        self.is_package = False

        if self.toplevel:
            # NOTE: we have only one store in project-git for all packages
            config_path = os.path.join(self.toplevel, "_config")
            pbuild_path = os.path.join(self.toplevel, "_pbuild")
            if self.toplevel == self.abspath and (os.path.isfile(config_path) or os.path.isfile(pbuild_path)):
                self.is_project = True
                self.is_package = False
            else:
                self.is_project = False
                self.is_package = True

        self._package = None
        self._project = None

        if check and not any([self.is_project, self.is_package]):
            msg = f"Directory '{self.path}' is not a Git SCM working copy"
            raise oscerr.NoWorkingCopy(msg)

        if check and not self.scmurl:
            msg = f"Directory '{self.path}' is a Git SCM repo that lacks the 'origin' remote"
            raise oscerr.NoWorkingCopy(msg)

        # TODO: decide if we need explicit 'git lfs pull' or not
        # self._run_git(["lfs", "pull"])

    def assert_is_project(self):
        if not self.is_project:
            msg = f"Directory '{self.path}' is not a Git SCM working copy of a project"
            raise oscerr.NoWorkingCopy(msg)

    def assert_is_package(self):
        if not self.is_package:
            msg = f"Directory '{self.path}' is not a Git SCM working copy of a package"
            raise oscerr.NoWorkingCopy(msg)

    def _run_git(self, args):
        return subprocess.check_output(["git"] + args, encoding="utf-8", cwd=self.abspath).strip()

    @property
    def apiurl(self):
        # HACK: we're using the currently configured apiurl
        return osc_conf.config["apiurl"]

    @property
    def project(self):
        if self._project is None:
            try:
                # NOTE: this never triggers if a store is retrieved from osc.store.get_store(),
                # because obs_scm store takes precedence as .osc is present
                with open(os.path.join(self.toplevel, ".osc/_project")) as f:
                    self._project = f.readline().strip()
            except FileNotFoundError:
                pass

        if self._project is None:
            # get project from the branch name
            branch = self._run_git(["branch", "--show-current"])

            # HACK: replace hard-coded mapping with metadata from git or the build service
            # NOTE: you never know which git repo is supposed to be used in which project
            if branch == "factory":
                self._project = "openSUSE:Factory"
            else:
                raise oscerr.NoWorkingCopy(f"Couldn't map git branch '{branch}' to a project")
        return self._project

    @project.setter
    def project(self, value):
        self._project = value

    @property
    def package(self):
        if self._package is None:
            origin = self._run_git(["remote", "get-url", "origin"])
            self._package = Path(urllib.parse.urlsplit(origin).path).stem
        return self._package

    @package.setter
    def package(self, value):
        self._package = value

    def _get_option(self, name):
        try:
            result = self._run_git(["config", "--local", "--get", f"osc.{name}"])
        except subprocess.CalledProcessError:
            result = None
        return result

    def _check_type(self, name, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(f"The option '{name}' should be {expected_type.__name__}, not {type(value).__name__}")

    def _set_option(self, name, value):
        self._run_git(["config", "--local", f"osc.{name}", value])

    def _unset_option(self, name):
        try:
            self._run_git(["config", "--local", "--unset", f"osc.{name}"])
        except subprocess.CalledProcessError:
            pass

    def _get_dict_option(self, name):
        result = self._get_option(name)
        if result is None:
            return None
        result = json.loads(result)
        self._check_type(name, result, dict)
        return result

    def _set_dict_option(self, name, value):
        if value is None:
            self._unset_option(name)
            return
        self._check_type(name, value, dict)
        value = json.dumps(value)
        self._set_option(name, value)

    @property
    def last_buildroot(self):
        self.assert_is_package()
        result = self._get_dict_option("last-buildroot")
        if result is not None:
            result = (result["repo"], result["arch"], result["vm_type"])
        return result

    @last_buildroot.setter
    def last_buildroot(self, value):
        self.assert_is_package()
        if len(value) != 3:
            raise ValueError("A tuple with exactly 3 items is expected: (repo, arch, vm_type)")
        value = {
            "repo": value[0],
            "arch": value[1],
            "vm_type": value[2],
        }
        self._set_dict_option("last-buildroot", value)

    @property
    def scmurl(self):
        try:
            return self._run_git(["remote", "get-url", "origin"])
        except subprocess.CalledProcessError:
            return None
