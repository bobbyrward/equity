import subprocess
import collections
import logging
import re


class SvnController(object):
    status_response_re = re.compile(r'^([^\s]+)\s+(.+)$')

    log = logging.getLogger(__name__)

    def __init__(self):
        self.svn_location = None

    def _find_svn(self):
        pipe = subprocess.Popen('which svn', stdout=subprocess.PIPE, shell=True)
        output, error_output = pipe.communicate()
        return_code = pipe.returncode

        if return_code != 0:
            raise Exception('svn not found')

        self.svn_location = output.strip()

    def run(self, command, args=None):
        if not self.svn_location:
            self._find_svn()

        all_arguments = [self.svn_location, command]

        if args:
            if isinstance(args, collections.Sequence):
                all_arguments.extend(args)
            else:
                all_arguments.append(args)

        self.log.info('Running "{}"'.format(' '.join(all_arguments)))

        pipe = subprocess.Popen(all_arguments, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        output, error_output = pipe.communicate()
        return_code = pipe.returncode

        return return_code, output, error_output

    def info(self, where=None):
        args = None

        if where is not None:
            args = [where]

        rc, output, error_output = self.run('info', args)

        return dict([y.split(':', 1) for y in output.split('\n') if y.strip()])


    def status(self, where=None):
        args = None

        if where is not None:
            args = [where]

        rc, output, error_output = self.run('status', args)

        results = []

        for line in output.split('\n'):
            line = line.strip()

            if not line:
                continue

            result = self.status_response_re.match(line)

            if not result:
                raise Exception('Unrecognized line in status: {}'.format(line))

            results.append(result.groups())

        return results
