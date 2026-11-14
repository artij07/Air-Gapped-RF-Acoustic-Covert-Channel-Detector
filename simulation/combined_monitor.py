
import json
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports"

console = Console()


def load_report(filename):
    path = REPORT_DIR / filename

    with open(path, "r") as file:
        return json.load(file)


def main():
    rf_results = load_report("rf_detection_report.json")
    acoustic_results = load_report("acoustic_detection_report.json")

    rf_status = rf_results["suspicious_rf.csv"]["status"]
    acoustic_status = acoustic_results["suspicious_audio.wav"]["status"]

    overall_status = (
        "THREAT DETECTED"
        if rf_status == "SUSPICIOUS"
        or acoustic_status == "SUSPICIOUS"
        else "NORMAL"
    )

    table = Table(title="AETHERHOUND SENSOR MONITOR")
    table.add_column("Sensor", style="cyan")
    table.add_column("Detection Status", style="white")

    table.add_row("Virtual SDR / RF", rf_status)
    table.add_row("Virtual Microphone", acoustic_status)

    console.print(
        Panel(
            f"[bold red]{overall_status}[/bold red]"
            if overall_status == "THREAT DETECTED"
            else f"[bold green]{overall_status}[/bold green]",
            title="SYSTEM STATUS"
        )
    )

    console.print(table)

    combined_report = {
        "timestamp": datetime.now().isoformat(),
        "rf_status": rf_status,
        "acoustic_status": acoustic_status,
        "overall_status": overall_status
    }

    output_path = REPORT_DIR / "combined_detection_report.json"

    with open(output_path, "w") as file:
        json.dump(combined_report, file, indent=4)

    console.print(
        f"\n[green]Combined report saved: {output_path}[/green]"
    )


if __name__ == "__main__":
    main()
