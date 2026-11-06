import subprocess


class Executor:
    def __init__(self, timeout=10):
        self.timeout = timeout

    def run(self, command):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False
            )

            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out"
            }

        except OSError as error:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(error)
            }

    def docker_exec(self, container, command):
        return self.run([
            "docker",
            "exec",
            container,
            *command
        ])
