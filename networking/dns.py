
class DNSChecker:

    def __init__(self, executor, timeout=5):
        self.executor = executor
        self.timeout = timeout

    def check(self, container, hostname):
        result = self.executor.docker_exec(
            container,
            [
                "getent",
                "ahostsv4",
                hostname
            ]
        )

        return {
            "check": "dns",
            "hostname": hostname,
            "timeout": self.timeout,
            "success": result["success"],
            "resolved_addresses": result["stdout"].splitlines(),
            "error": result["stderr"]
        }

