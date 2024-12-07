import os
import signal
import subprocess  # nosec
import sys


class ProcessWrapper:
    def __init__(self, command: list[str]) -> None:
        self.command = command
        self.child_process = None

    def forward_signal_to_child(self, signum: int, frame: int) -> None:
        if self.child_process is not None:
            os.kill(self.child_process.pid, signum)

    def run(self) -> int:
        signal.signal(signal.SIGINT, self.forward_signal_to_child)
        signal.signal(signal.SIGTERM, self.forward_signal_to_child)
        self.child_process = subprocess.Popen(self.command)  # nosec
        return self.child_process.wait()


def run() -> None:
    command = [
        os.path.join(os.path.dirname(__file__), 'bauplan-cli'),
        *sys.argv[1:],
    ]
    wrapper = ProcessWrapper(command)
    sys.exit(wrapper.run())


if __name__ == '__main__':
    run()
