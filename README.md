
# Infrastructure Automation Platform

A local infrastructure monitoring and automation platform built with Python, Bash, Rust, Docker, and Containerlab.

The platform collects infrastructure health information, performs network and service checks, monitors Linux resources, and generates structured JSON reports.

## Features

- YAML-based infrastructure inventory
- Docker container status monitoring
- DNS resolution checks
- Network connectivity checks
- Cross-network connectivity testing
- HTTP connectivity verification
- Routing table inspection
- TCP service checks
- Linux system information collection
- Disk storage monitoring
- JSON health reports
- Application logging
- Rust-based system metrics agent
- Bash infrastructure and service management scripts
- Unit testing with Python unittest

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main controller and orchestration |
| Bash | Infrastructure automation scripts |
| Rust | System metrics collection |
| Docker | Container runtime |
| Containerlab | Network lab environment |
| YAML | Configuration and inventory |
| JSON | Health reports |
| Linux | Operating environment |

## Project Structure

```text
infra-automation-platform/
├── config/
├── controller/
├── networking/
├── linux/
├── scripts/
├── rust-agent/
├── reporting/
├── logs/
├── reports/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Linux or WSL Ubuntu
- Python 3
- Docker
- Containerlab
- Rust and Cargo
- Git

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd infra-automation-platform
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Build the Rust agent:

```bash
cd rust-agent
cargo build --release
cd ..
```

## Lab Environment

This project currently uses a local three-node Containerlab environment:

- client1
- router1
- server1

The lab provides a practical environment for testing DNS, routing, connectivity, and HTTP communication.

Deploy the lab using your Containerlab topology file:

```bash
sudo containerlab deploy --reconfigure -t ~/containerlab/lab01/practice.clab.yml
```

Make sure the lab containers are running before starting the platform.

## Usage

Run infrastructure checks:

```bash
python3 main.py
```

Display application version:

```bash
python3 main.py --version
```

The platform collects available infrastructure information and generates a JSON health report.

## Running Tests

Run the complete test suite:

```bash
python3 -m unittest discover -s tests -v
```

## Reports and Logs

Generated JSON reports are stored in:

```text
reports/
```

Application logs are stored in:

```text
logs/
```

Each report contains collected infrastructure check results and a generation timestamp.

## Bash Scripts

The `scripts/` directory contains automation utilities for:

- Infrastructure health checks
- Service management
- Backup operations

## Rust Agent

The Rust agent collects host-level system metrics and supports structured JSON output.

It is built separately using Cargo and executed by the Python controller.

## Current Scope

This version is designed and tested for a local WSL Ubuntu and Containerlab environment.

It focuses on infrastructure monitoring, Linux diagnostics, network troubleshooting, and automation fundamentals.

Remote SSH and public cloud integrations are not included in the current version.

## License

Add a license before distributing this project publicly.

