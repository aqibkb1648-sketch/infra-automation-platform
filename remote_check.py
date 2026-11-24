import paramiko
import socket
import json
from datetime import datetime, timezone

HOST = "172.20.20.4"
USERNAME = "aqib_kb"
KEY_FILE = "/home/aqib_kb/.ssh/id_ed25519"

COMMANDS = ["hostname", "uptime", "df -h"]

report = {
    "server": HOST,
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "status": "UNKNOWN",
    "checks": [],
}

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

try:
    print(f"Connecting to {HOST}...")

    ssh.connect(
        hostname=HOST,
        port=22,
        username=USERNAME,
        key_filename=KEY_FILE,
        timeout=10,
        banner_timeout=10,
        auth_timeout=10,
    )

    print("SSH connection successful!")
    report["status"] = "CONNECTED"

    for command in COMMANDS:
        print(f"\nRunning: {command}")

        stdin, stdout, stderr = ssh.exec_command(
            command,
            timeout=15,
        )

        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        check = {
            "command": command,
            "exit_code": exit_code,
            "status": "PASS" if exit_code == 0 else "FAIL",
            "output": output,
            "error": error,
        }

        report["checks"].append(check)

        print(f"Exit code: {exit_code}")
        print(output if exit_code == 0 else error)

    if any(check["status"] == "FAIL" for check in report["checks"]):
        report["status"] = "DEGRADED"
    else:
        report["status"] = "HEALTHY"

except paramiko.AuthenticationException:
    report["status"] = "AUTHENTICATION_FAILED"
    print("ERROR: SSH authentication failed.")

except paramiko.SSHException as error:
    report["status"] = "SSH_ERROR"
    print(f"SSH ERROR: {error}")

except (socket.timeout, TimeoutError):
    report["status"] = "TIMEOUT"
    print("ERROR: SSH connection timed out.")

except OSError as error:
    report["status"] = "NETWORK_ERROR"
    print(f"NETWORK ERROR: {error}")

finally:
    if ssh.get_transport() and ssh.get_transport().is_active():
        ssh.close()

    with open("remote-health-report.json", "w") as file:
        json.dump(report, file, indent=4)

    print("\nSSH connection closed.")
    print("JSON report saved: remote-health-report.json")
    print("Overall status:", report["status"])