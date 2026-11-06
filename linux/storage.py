class StorageChecker:
    def __init__(self, executor):
        self.executor = executor

    def collect(self, container):
        result = self.executor.docker_exec(
            container,
            ["df", "-h"]
        )

        return {
            "check": "storage",
            "success": result["success"],
            "usage": result["stdout"].splitlines(),
            "error": result["stderr"]
        }
