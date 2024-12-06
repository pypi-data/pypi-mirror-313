import re
from collections import defaultdict
import argparse
import os

# Parser class to support multiple formats
class LogParser:
    def __init__(self, log_format):
        self.log_format = log_format

    def parse_line(self, line):
        if self.log_format == "apache":
            return self.parse_apache(line)
        elif self.log_format == "nginx":
            return self.parse_nginx(line)
        elif self.log_format == "aws":
            return self.parse_aws(line)
        else:
            raise ValueError("Unsupported log format")

    def parse_apache(self, line):
        # Apache log format
        match = re.match(
            r'^(?P<ip>\S+) - - \[(?P<time>.*?)\] "(?P<method>\S+) (?P<endpoint>\S+) HTTP/\d\.\d" (?P<status>\d+) (?P<size>\d+)',
            line,
        )
        return match.groupdict() if match else None

    def parse_nginx(self, line):
        # Nginx log format
        match = re.match(
            r'^(?P<ip>\S+) - - \[(?P<time>.*?)\] "(?P<method>\S+) (?P<endpoint>\S+) HTTP/\d\.\d" (?P<status>\d+) (?P<size>\d+)',
            line,
        )
        return match.groupdict() if match else None

    def parse_aws(self, line):
        # AWS ALB log format
        match = re.match(
            r'^http \S+ app/\S+ (?P<ip>\S+):\d+ \S+:\d+ \S+ \S+ \S+ (?P<status>\d+) \S+ \S+ \S+ "(?P<method>\S+) (?P<endpoint>\S+) HTTP/\d\.\d"',
            line,
        )
        return match.groupdict() if match else None

# Function to parse log file incrementally
def parse_log_in_chunks(file_path, parser):
    ip_counts = defaultdict(int)
    endpoint_counts = defaultdict(int)
    failed_logins = defaultdict(int)

    with open(file_path, "r") as file:
        for line in file:
            data = parser.parse_line(line)
            if not data:
                continue

            ip = data.get("ip")
            endpoint = data.get("endpoint")
            status = data.get("status")

            if ip:
                ip_counts[ip] += 1
            if endpoint:
                endpoint_counts[endpoint] += 1
            if status and int(status) == 401:
                failed_logins[ip] += 1

    return ip_counts, endpoint_counts, failed_logins

# Main function to handle command-line arguments and execute parsing
def main():
    parser = argparse.ArgumentParser(description="LogSentinel - Multi-Format Log Analyzer")
    parser.add_argument("--file", type=str, required=True, help="Path to the log file")
    parser.add_argument(
        "--format",
        type=str,
        required=True,
        choices=["apache", "nginx", "aws"],
        help="Log file format (apache/nginx/aws)",
    )
    parser.add_argument("--threshold", type=int, default=10, help="Failed login threshold (default: 10)")
    args = parser.parse_args()

    # Initialize parser
    log_parser = LogParser(args.format)

    # Parse logs
    print(f"Parsing {args.format} log file: {args.file}")
    ip_counts, endpoint_counts, failed_logins = parse_log_in_chunks(args.file, log_parser)

    # Output results
    print("\nRequests per IP Address:")
    for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{ip:<20}{count:<15}")

    print("\nMost Frequently Accessed Endpoints:")
    for endpoint, count in sorted(endpoint_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{endpoint:<20}{count:<15}")

    print("\nSuspicious Activity Detected:")
    for ip, count in failed_logins.items():
        if count > args.threshold:
            print(f"{ip:<20}{count:<15}")

if __name__ == "__main__":
    main()
