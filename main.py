import argparse
from insightlog.lib import InsightLogAnalyzer
from datetime import datetime
import json

def main():
    parser = argparse.ArgumentParser(description="Analyze server log files (nginx, apache2, auth)")
    parser.add_argument('--service', required=True, choices=['nginx', 'apache2', 'auth'], help='Type of log to analyze')
    parser.add_argument('--logfile', required=True, help='Path to the log file')
    parser.add_argument('--filter', required=False, default=None, help='String to filter log lines')
    parser.add_argument('--output', required=False, default='text', choices=['text', 'csv', 'json'], help='Output format (text, csv, json)')
    parser.add_argument('--loglevel', required=False, default=None, help='Log level to filter (e.g., ERROR, WARNING)')
    parser.add_argument('--start', required=False, default=None, help='Start time for time range filter (ISO 8601, e.g., 2025-09-10T00:00:00)')
    parser.add_argument('--end', required=False, default=None, help='End time for time range filter (ISO 8601, e.g., 2025-09-10T23:59:59)')
    args = parser.parse_args()

    analyzer = InsightLogAnalyzer(args.service, filepath=args.logfile)
    if args.filter:
        analyzer.add_filter(args.filter)
    if args.loglevel:
        analyzer.add_log_level_filter(args.loglevel)
    if args.start and args.end:
        try:
            start_dt = datetime.fromisoformat(args.start)
            end_dt = datetime.fromisoformat(args.end)
            analyzer.add_time_range_filter(start_dt, end_dt)
        except Exception as e:
            print(f"Invalid time range: {e}")
    requests = analyzer.get_requests()

    if args.output == 'csv':
        # Export to CSV (stub)
        csv_path = args.logfile + '.csv'
        analyzer.export_to_csv(csv_path)
        print(f"Exported to {csv_path}")
    elif args.output == 'json':
        print(json.dumps(requests, indent=2))
    else:
        for req in requests:
            print(req)

if __name__ == '__main__':
    main() 