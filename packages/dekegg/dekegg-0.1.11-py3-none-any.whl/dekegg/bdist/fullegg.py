import os
import sys
import json
import tempfile
import shutil
import subprocess
from dektools.package.entry_points import entry_points
from dektools.dict import dict_merge
from dektools.file import read_text, write_file, read_lines, remove_path
from dektools.sys import sys_paths_relative
from dektools.shell import shell_wrapper, shell_exitcode
from ..tmpl import ProjectGenerator
from .fixegg import bdist_fixegg


class bdist_fullegg(bdist_fixegg):
    description = "create an full-egg (egg with dependencies) distribution"

    def run(self):
        requirements = 'requirements.txt'
        if requirements and os.path.exists(requirements):
            self._install(requirements, self.bdist_dir)
        super().run()

    def copy_metadata_to(self, target_dir):
        super().copy_metadata_to(target_dir)
        if self._entry_points:
            path = os.path.join(target_dir, 'entry_points.txt')
            data = {}
            dict_merge(data, entry_points.load(path, default={}), self._entry_points)
            entry_points.dump(path, data)

    def _install(self, requirements, target):
        target = os.path.normpath(os.path.abspath(target))
        if shutil.which('pdm'):
            path_need_clean = path_dir = tempfile.mkdtemp(prefix='dekegg-pdm-install')
            dependencies = []
            if requirements:
                for line in read_text(requirements).splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        dependencies.append(line)
            ProjectGenerator(path_dir, dict(
                dependencies=json.dumps(dependencies)
            )).action()
            write_file(os.path.join(path_dir, 'pdm.lock'), mi='requirements.lock')
            last_dir = os.getcwd()
            os.chdir(path_dir)
            shell_wrapper('virtualenv .venv --no-pip --no-setuptools --no-wheel')
            os.environ['PDM_IGNORE_ACTIVE_VENV'] = 'true'
            os.environ['PDM_NO_CACHE'] = 'true'
            shell_wrapper('pdm install')
            os.chdir(last_dir)
            path_platlib = sys_paths_relative(os.path.join(path_dir, '.venv'))['platlib']
        elif shell_exitcode(f'{sys.executable} -m pip') == 0:
            path_need_clean = path_platlib = tempfile.mkdtemp(prefix='dekegg-pip-install')
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install']
                + ['-U', '-t', path_platlib, '-r', requirements]
            )
        else:
            raise RuntimeError(f"Can't find a valid package installer.")
        self._entry_points = {}
        for file in os.listdir(path_platlib):
            if file.endswith('.dist-info'):
                path_dist = os.path.join(path_platlib, file)
                pr = os.path.join(path_dist, 'RECORD')
                if os.path.exists(pr):
                    for line in read_lines(pr, True):
                        path, _ = line.split(',', 1)
                        if not path.startswith(file + '/'):
                            write_file(os.path.join(target, path), c=os.path.join(path_platlib, path))
                dict_merge(
                    self._entry_points,
                    entry_points.load(os.path.join(path_dist, 'entry_points.txt'), default={})
                )
        remove_path(path_need_clean)
        shell_wrapper(f'{sys.executable} -m compileall {target}')
