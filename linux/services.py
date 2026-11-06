class ServiceChecker:

    def __init__(self, executor):
        self.executor = executor

    def check(self, container, service_name, port, protocol="tcp"):
        protocol = protocol.lower()

        if protocol not in ("tcp", "http", "https"):
            return {
                "check": "service",
                "service": service_name,
                "port": port,
                "protocol": protocol,
                "success": False,
                "error": "Unsupported protocol."
            }

        if protocol == "tcp":
            command = [
                "sh", "-c",
                f"nc -z -w 3 127.0.0.1 {int(port)}"
            ]
        else:
            scheme = protocol
            command = [
                "curl",
                "-k",
                "-sS",
                "-o", "/dev/null",
                "--connect-timeout", "3",
                "-w", "%{http_code}",
                f"{scheme}://127.0.0.1:{int(port)}"
            ]

        result = self.executor.docker_exec(
            container,
            command
        )

        return {
            "check": "service",
            "service": service_name,
            "port": port,
            "protocol": protocol,
            "success": result["success"],
            "output": result["stdout"],
            "error": result["stderr"]
        }
