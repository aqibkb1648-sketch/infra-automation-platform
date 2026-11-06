use serde::Serialize;
use std::env;
use std::fs;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Serialize)]
struct SystemMetrics {
    hostname: String,
    uptime_seconds: Option<u64>,
    memory_total_kb: Option<u64>,
    memory_available_kb: Option<u64>,
    load_average: Option<String>,
    timestamp: u64,
}

fn read_memory_value(contents: &str, key: &str) -> Option<u64> {
    contents.lines().find_map(|line| {
        let mut parts = line.split_whitespace();

        if parts.next()? == key {
            parts.next()?.parse().ok()
        } else {
            None
        }
    })
}

fn collect_metrics() -> SystemMetrics {
    let hostname = fs::read_to_string("/etc/hostname")
        .unwrap_or_else(|_| "unknown".to_string())
        .trim()
        .to_string();

    let uptime_seconds = fs::read_to_string("/proc/uptime")
        .ok()
        .and_then(|data| {
            data.split_whitespace()
                .next()?
                .parse::<f64>()
                .ok()
                .map(|value| value as u64)
        });

    let memory = fs::read_to_string("/proc/meminfo").unwrap_or_default();

    let memory_total_kb = read_memory_value(&memory, "MemTotal:");
    let memory_available_kb = read_memory_value(&memory, "MemAvailable:");

    let load_average = fs::read_to_string("/proc/loadavg")
        .ok()
        .map(|value| value.trim().to_string());

    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();

    SystemMetrics {
        hostname,
        uptime_seconds,
        memory_total_kb,
        memory_available_kb,
        load_average,
        timestamp,
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.get(1).map(String::as_str) == Some("--version") {
        println!("infra-agent 1.0.0");
        return;
    }

    if args.get(1).map(String::as_str) == Some("--help") {
        println!("Usage: infra-agent [--json | --version | --help]");
        return;
    }

    let metrics = collect_metrics();

    if args.get(1).map(String::as_str) == Some("--json") {
        match serde_json::to_string_pretty(&metrics) {
            Ok(output) => println!("{}", output),
            Err(error) => {
                eprintln!("JSON error: {}", error);
                std::process::exit(1);
            }
        }
    } else {
        println!("Infrastructure System Metrics");
        println!("Hostname: {}", metrics.hostname);
        println!("Uptime: {:?} seconds", metrics.uptime_seconds);
        println!("Total Memory: {:?} KB", metrics.memory_total_kb);
        println!(
            "Available Memory: {:?} KB",
            metrics.memory_available_kb
        );
        println!("Load Average: {:?}", metrics.load_average);
        println!("Timestamp: {}", metrics.timestamp);
    }
}
