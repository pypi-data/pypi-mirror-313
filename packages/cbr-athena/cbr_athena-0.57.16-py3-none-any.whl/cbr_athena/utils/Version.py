from osbot_utils.utils.Files import path_combine, file_contents

import cbr_athena


class Version:

    def path_code_root(self):
        return cbr_athena.path

    def path_version_file(self):
        return path_combine(self.path_code_root(), 'version')

    def version(self):
        version = file_contents(self.path_version_file())
        if version:
            return version.strip()
        return '....'

version__cbr_athena = Version().version()