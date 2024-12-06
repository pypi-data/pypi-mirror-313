'''Helper functions.'''

import subprocess
import tempfile


def executeShell(cmd, print_output=True, save_output_as=''):
    """
    Execute a shell command with the given parameters.
    
    :param cmd: Command to execute and the parameters to pass to it.
    :type cmd: list
    :param print_output: Print the output on screen if True.
    :type print_output: boolean
    :param save_output_as: (optional) Filename to save the output to.
    :type save_output_as: str
    :return: void
    
    """
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(cmd, stdout=tempf)
        proc.wait()
        tempf.seek(0)
        output = str(tempf.read().decode())
        
    if save_output_as:
        with open(save_output_as, 'w') as f:
            f.write(output)
        
    if print_output:
        print(output)
