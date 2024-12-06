import json
from pathlib import Path
import jinja2
from typing import Any, Dict, List


class MetricsFormatter:
    HTML_ARROW = " &rarr; "  # HTML arrow entity

    @staticmethod
    def format_time(seconds: float) -> str:
        """Format time in seconds to a readable string."""
        if seconds < 0.1:
            return f"{seconds * 1000:.2f} ms"
        return f"{seconds:.2f} s"

    @staticmethod
    def format_count(value: int) -> str:
        """Format count with a thousand separators."""
        return f"{value:,}"

    @staticmethod
    def format_percentage(value: float) -> str:
        """Format float as percentage."""
        return f"{value:.2f}%"

    @staticmethod
    def format_sequence_with_probability(data: list) -> Dict[str, Any]:
        """Format sequence with probability into a readable structure."""
        sequence, probability = data
        return {
            "sequence": MetricsFormatter.HTML_ARROW.join(sequence),
            "probability": f"{probability * 100:.1f}%",
            "steps": len(sequence)
        }

    @staticmethod
    def format_self_distances(distances: Dict[str, int]) -> Dict[str, str]:
        """Format self distances into a more readable structure."""
        return {
            activity: f"{distance} steps"
            for activity, distance in distances.items()
        }

    @staticmethod
    def format_self_distance_witnesses(witnesses: Dict[str, List[List[str]]]) -> Dict[str, str]:
        """Format self distance witnesses into a readable structure."""
        return {
            activity: [MetricsFormatter.HTML_ARROW.join(path) for path in paths]
            for activity, paths in witnesses.items()
        }

    @staticmethod
    def format_activities_count(counts: Dict[str, int]) -> Dict[str, str]:
        """Format activity counts with percentage of total."""
        total = sum(counts.values())
        return {
            activity: f"{count:,} ({(count / total) * 100:.1f}%)"
            for activity, count in counts.items()
        }

    @staticmethod
    def format_activities_time(times: Dict[str, float]) -> Dict[str, str]:
        """Format activities time."""
        return {
            activity: MetricsFormatter.format_time(duration)
            for activity, duration in times.items()
        }

    @staticmethod
    def format_metric(key: str, value: Any) -> Any:
        """Format a metric based on its key and value type."""
        if isinstance(value, dict):
            if key == "minimum_self_distances":
                return MetricsFormatter.format_self_distances(value)
            elif key == "self_distance_witnesses":
                return MetricsFormatter.format_self_distance_witnesses(value)
            elif key == "activities_count":
                return MetricsFormatter.format_activities_count(value)
            elif key == "activities_sum_service_time":
                return MetricsFormatter.format_activities_time(value)
            elif key == "rework_counts":
                return {activity: MetricsFormatter.format_count(count)
                        for activity, count in value.items()}
        elif isinstance(value, list) and key == "sequence_with_probability":
            return MetricsFormatter.format_sequence_with_probability(value)
        elif isinstance(value, (int, float)):
            if key == "case_duration":
                return MetricsFormatter.format_time(value)
            elif "probability" in key.lower():
                return MetricsFormatter.format_percentage(value)
            else:
                return MetricsFormatter.format_count(value)
        return value


class CaseArchitectureComparisonReport:
    def __init__(self, base_paths, case_ids):
        self.base_paths = base_paths
        self.case_ids = case_ids
        self.infrastructures_data = {}
        self.report_dir = Path("case_comparison_report")
        self.formatter = MetricsFormatter()

    def load_data(self):
        for base_path in self.base_paths:
            infra_name = Path(base_path).name
            self.infrastructures_data[infra_name] = {}

            # Load data for each case ID
            for case_id in self.case_ids:
                case_report_path = Path(base_path) / "reports" / "cases" / f"{case_id}_report.json"
                print(f"Trying to access: {case_report_path.absolute()}")
                print(f"File exists: {case_report_path.exists()}")
                if case_report_path.exists():
                    with open(case_report_path, 'r') as f:
                        raw_data = json.load(f)
                        self.infrastructures_data[infra_name][f'case_{case_id}'] = {
                            key: self.formatter.format_metric(key, value)
                            for key, value in raw_data.items()
                        }
                else:
                    print(f"Warning: Case {case_id} not found in {infra_name}")
                    self.infrastructures_data[infra_name][f'case_{case_id}'] = None

    def generate_report(self):
        self.report_dir.mkdir(exist_ok=True)

        # Create comparison data structure for each case
        case_metrics_comparison = {}
        for case_id in self.case_ids:
            case_key = f'case_{case_id}'
            case_metrics_comparison[case_id] = {}

            # Get all possible metrics from the first infrastructure that has this case
            first_infra_with_case = next(
                (infra for infra in self.infrastructures_data.values()
                 if case_key in infra and infra[case_key] is not None),
                None
            )

            if first_infra_with_case:
                for metric in first_infra_with_case[case_key].keys():
                    case_metrics_comparison[case_id][metric] = []
                    for infra in self.infrastructures_data:
                        case_data = self.infrastructures_data[infra].get(case_key)
                        if case_data:
                            case_metrics_comparison[case_id][metric].append(case_data.get(metric))
                        else:
                            case_metrics_comparison[case_id][metric].append("N/A")

        env = jinja2.Environment()
        template = env.from_string(self.get_template())
        html_content = template.render(
            case_metrics_comparison=case_metrics_comparison,
            case_ids=self.case_ids,
            infrastructures=list(self.infrastructures_data.keys())
        )

        with open(self.report_dir / "index.html", 'w') as f:
            f.write(html_content)

        print(f"Report generated at {self.report_dir}/index.html")

    @staticmethod
    def get_template():
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Case Comparison Report</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .metrics-table th {
            position: sticky;
            top: 0;
            background-color: #f8fafc;
            z-index: 10;
        }

        .metrics-row:nth-child(even) {
            background-color: #f8fafc;
        }

        .metrics-cell {
            max-width: 300px;
            overflow: auto;
        }

        .case-card {
            height: calc(100vh - 2rem);
            overflow-y: auto;
        }
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Case Comparison Report</h1>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {% for case_id in case_ids %}
            <div class="bg-white rounded-lg shadow case-card">
                <div class="sticky top-0 bg-white p-4 border-b z-20">
                    <h2 class="text-xl font-bold">Case {{ case_id }}</h2>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full metrics-table">
                        <thead>
                            <tr>
                                <th class="px-4 py-2 text-left border-b">Metric</th>
                                {% for infra in infrastructures %}
                                <th class="px-4 py-2 text-left border-b">{{ infra }}</th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for metric, values in case_metrics_comparison[case_id].items() %}
                            <tr class="metrics-row hover:bg-gray-50">
                                <td class="px-4 py-2 border-b font-medium">{{ metric }}</td>
                                {% for value in values %}
                                <td class="px-4 py-2 border-b metrics-cell">
                                    {% if value is mapping %}
                                        {% for k, v in value.items() %}
                                        <div class="mb-2">
                                            <strong>{{ k }}:</strong>
                                            {% if v is mapping %}
                                                <div class="pl-4">
                                                    {% for sub_k, sub_v in v.items() %}
                                                    <div><em>{{ sub_k }}:</em> {{ sub_v }}</div>
                                                    {% endfor %}
                                                </div>
                                            {% else %}
                                                {{ v }}
                                            {% endif %}
                                        </div>
                                        {% endfor %}
                                    {% else %}
                                        {{ value }}
                                    {% endif %}
                                </td>
                                {% endfor %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""