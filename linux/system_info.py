class SystemInfo:
    def __init__(self, executor):
        self.executor = executor

    def collect(self, container):
        commands = {
            "hostname": ["hostname"],
            "uptime": ["uptime"],
            "memory": ["sh", "-c", "free -h || cat /proc/meminfo"],
            "cpu": ["sh", "-c", "cat /proc/loadavg"]
        }

        results = {}

        for name, command in commands.items():
            result = self.executor.docker_exec(container, command)

            results[name] = {
                "success": result["success"],
                "output": result["stdout"],
                "error": result["stderr"]
            }

        return {
            "check": "system_info",
            "success": all(item["success"] for item in results.values()),
            "details": results
        }
