import os
import argparse
import subprocess
import threading
import signal
import sys
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

stop_event = threading.Event()

def run_nmap(command, output_file, task_id, progress):
    try:
        with open(output_file, 'w') as f:
            process = subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT, shell=True)
            while process.poll() is None:
                if stop_event.is_set():
                    process.terminate()
                    progress.update(task_id, description=f"[red]Terminated: {command}[/red]")
                    return
                progress.update(task_id, advance=1)
            progress.update(task_id, completed=100, description=f"[green]Completed: {command}[/green]")
    except Exception as e:
        progress.update(task_id, description=f"[red]Error: {command}[/red]")
        print(f"[-] Error running command {command}: {e}")

def signal_handler(sig, frame):
    print("\n[!] Ctrl+C detected. Stopping all threads...")
    stop_event.set()
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Run multiple Nmap commands on a URL")
    parser.add_argument("-u", "--url", required=True, help="Target URL or IP address")
    args = parser.parse_args()
    url = args.url

    commands = {
        f"nmap -d -Pn --script vuln {url}": f"nmap/{url}_nmap-vuln.txt",
        f"nmap --script http-slowloris-check {url}": f"nmap/{url}_nmap-slowloris.txt",
        f"nmap --script ssl-dh-params {url}": f"nmap/{url}_nmap-ssl-dh.txt",
        f"nmap -sV --script ssl-enum-ciphers -p 443 {url}": f"nmap/{url}_nmap-ssl-ciphers.txt",
        f"nmap -p- {url}": f"nmap/{url}_nmap-all-ports.txt",
    }

    os.makedirs("nmap", exist_ok=True)
    signal.signal(signal.SIGINT, signal_handler)

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
    )

    threads = []
    with progress:
        for command, output_file in commands.items():
            task_id = progress.add_task(f"[cyan]Running: {command}[/cyan]", total=100)
            thread = threading.Thread(target=run_nmap, args=(command, output_file, task_id, progress))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    print("[+] All Nmap commands completed.")

if __name__ == "__main__":
    main()
