
class ConnectivityChecker:

    def __init__(self, executor, ping_count=2):
        self.executor = executor
        self.ping_count = ping_count

    def check(self, container, target):
        result = self.executor.docker_exec(
            container,
            [
                "ping",
                "-c", str(self.ping_count),
                "-W", "2",
                target
            ]
        )

        return {
            "check": "connectivity",
            "source": container,
            "target": target,
            "success": result["success"],
            "output": result["stdout"],
            "error": result["stderr"]
        }

    def check_http(self, container, target, port=80):
        url = f"http://{target}:{port}"

        result = self.executor.docker_exec(
            container,
            [
                "curl",
                "-sS",
                "-o", "/dev/null",
                "-w", "%{http_code}",
                "--connect-timeout", "5",
                "--max-time", "10",
                url
            ]
        )

        http_code = result["stdout"].strip()

        return {
            "check": "http_connectivity",
            "source": container,
            "target": url,
            "success": result["success"] and http_code == "200",
            "http_code": http_code,
            "output": result["stdout"],
            "error": result["stderr"]
        }

