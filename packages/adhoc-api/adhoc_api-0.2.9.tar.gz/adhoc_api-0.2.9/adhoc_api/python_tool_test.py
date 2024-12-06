# See: https://stackoverflow.com/questions/52954248/capture-output-as-a-tty-in-python

import errno
import os
import pty
import signal
import subprocess


def subprocess_tty(cmd, encoding="utf-8", timeout=10, **kwargs):
    """`subprocess.Popen` yielding stdout lines acting as a TTY"""
    m, s = pty.openpty()
    p = subprocess.Popen(cmd, stdout=s, stderr=s, **kwargs)
    os.close(s)

    try:
        for line in open(m, encoding=encoding):
            if not line:  # EOF
                break
            yield line
    except OSError as e:
        if errno.EIO != e.errno:  # EIO also means EOF
            raise
    finally:
        if p.poll() is None:
            p.send_signal(signal.SIGINT)
            try:
                p.wait(timeout)
            except subprocess.TimeoutExpired:
                p.terminate()
                try:
                    p.wait(timeout)
                except subprocess.TimeoutExpired:
                    p.kill()
        p.wait()


import textwrap

for line in subprocess_tty(
    [
        "python",
        "-c",
        textwrap.dedent(
            """\
            import sys
            print(sys.stdin.isatty())
            print(sys.stdout.isatty())
            print(sys.stderr.isatty())
            """
        ),
    ]
):
    print(f"{line!r}")



################################################################################################

import subprocess
from archytas.tool_utils import tool
from typing import Callable, Any


class PythonTool:
    """Tool for running python code. If the user asks you to write code, you can run it here."""
    def __init__(self, sideeffect:Callable[[str, str, str, int], Any]=lambda *_: None):
        """
        Set up a PythonTool instance.

        Args:
            sideeffect (Callable[[str], Any], optional): A side effect function to run when the tool is used. Defaults to do nothing.
        """
        self.sideeffect = sideeffect

        # Start Python as a subprocess. capture stdout and stderr
        self.process = subprocess.Popen(['python', '-u'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, bufsize=1)

    
    def __del__(self):
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait()
    
    
    @tool
    def run(self, code: str) -> tuple[str, str, int]:
        """
        Runs python code in a python subprocess.

        The environment is not persistent between runs, so any variables created will not be available in subsequent runs.
        The only visible effects of this tool are from output to stdout/stderr. If you want to view a result, you MUST print it.

        Args:
            code (str): The code to run

        Returns:
            tuple: The stdout, stderr, and returncode from executing the code
        """
        # Send input to the subprocess
        self.process.stdin.write(code)  # Feed a command
        self.process.stdin.flush()  # Ensure the command is sent

        # Read output/stderr from the subprocess
        import pdb; pdb.set_trace()
        stdout = self.process.stdout.read()
        stderr = self.process.stderr.read()

        # simulate a return code depending on if the code errored or not
        returncode = 1 if stderr else 0

        # Run the side effect function
        self.sideeffect(code, stdout, stderr, returncode)

        return stdout, stderr, returncode
        





if __name__ == '__main__':
    py = PythonTool()
    print(py.run('x = 3'))
    print(py.run('a = 5\nprint(a)'))
    print(py.run('print(a)'))
    print(py.run('print(x+y)'))  # should error