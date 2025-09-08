import argparse
from insightlog.lib import InsightLogAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Analyze server log files (nginx, apache2, auth)")
    parser.add_argument('--service', required=True, choices=['nginx', 'apache2', 'auth'], help='Type of log to analyze')
    parser.add_argument('--logfile', required=True, help='Path to the log file')
    parser.add_argument('--filter', required=False, default=None, help='String to filter log lines')
    parser.add_argument('--export', required=False, choices=['csv', 'json'], help='Export results to CSV or JSON')
    parser.add_argument('--export-path', required=False, help='Path to export file (default: export.csv or export.json)')
    args = parser.parse_args()

    analyzer = InsightLogAnalyzer(args.service, filepath=args.logfile)
    if args.filter:
        analyzer.add_filter(args.filter)

    if args.export:
        export_path = args.export_path
        if not export_path:
            export_path = f"export.{args.export}"
        if args.export == 'csv':
            analyzer.export_to_csv(export_path)
        elif args.export == 'json':
            analyzer.export_to_json(export_path)
    else:
        requests = analyzer.get_requests()
        for req in requests:
            print(req)

if __name__ == '__main__':
    main() 