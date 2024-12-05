import errno
import os

from azureml.studio.core.logger import time_profile


class CustomModuleUtils:
    @staticmethod
    def add_directory_to_sys_path(dir_path):
        import sys

        # Avoid adding nonexistent paths
        if not os.path.exists(dir_path):
            return False

        # Standardize the path. Windows is case-insensitive, so lowercase
        # for definiteness.
        new_path = os.path.abspath(dir_path)
        if sys.platform == 'win32':
            new_path = new_path.lower()

        # Check against all currently available paths
        for x in sys.path:
            x = os.path.abspath(x)
            if sys.platform == 'win32':
                x = x.lower()
            if new_path in (x, x + os.sep):
                return True
        sys.path.append(new_path)
        return True

    @staticmethod
    @time_profile
    def check_r_package_installed(expect_r_version):
        try:
            found_r_version = CustomModuleUtils._get_installed_r_version()
        except OSError as ex:
            # OSError: [Errno 12] Cannot allocate memory
            if ex.errno == errno.ENOMEM:
                raise MemoryError() from ex
            else:
                raise ex
        except Exception:
            raise RuntimeError("R package is NOT pre-installed.")

        if found_r_version != expect_r_version:
            raise RuntimeError(f"Failed to find required R version,"
                               f" expect: {expect_r_version}, actual: {found_r_version}")

    @staticmethod
    def _get_installed_r_version():
        import subprocess
        result = subprocess.run("Rscript --version", stderr=subprocess.PIPE, shell=True)
        version_output = result.stderr.decode('utf-8')
        import re
        m = re.match("R scripting front-end version (?P<version>[0-9.]+)", version_output)
        if m:
            found_r_version = m.group('version')
        else:
            raise RuntimeError(f"Unexpected output {version_output}")
        return found_r_version
