import subprocess
import collections
import logging
import re



def apply_patch(patch_text):
    pipe = subprocess.Popen('patch -p0', stdout=subprocess.PIPE,
            stdin=subprocess.PIPE, shell=True)

    output, error_output = pipe.communicate(patch_text)
    return_code = pipe.returncode

    if return_code != 0:
        raise Exception( 'Patch apply failed: \n{}\n{}'.format(
                    output, error_output
                ))
