class RoutingChecker:
    def __init__(self, executor):
        self.executor = executor

    def collect(self, container):
        result = self.executor.docker_exec(
            container,
            ["ip", "route", "show"]
        )

        return {
            "check": "routing",
            "success": result["success"],
            "routes": result["stdout"].splitlines(),
            "error": result["stderr"]
        }
