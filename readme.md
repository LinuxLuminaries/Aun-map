# AuN-map

The Nmap Automation Tool is a multithreaded script designed to efficiently run multiple Nmap scans on a target URL or IP address. It simplifies the process of vulnerability assessment by automating common Nmap commands, ensuring fast and organized outputs.

## Prerequisites

Run the script with the following arguments:

`*`Python 3.6 or later

`*`Nmap installed on your system

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install rich.

```bash
pip install rich
```

## Usage
Run the script with the following arguments to scan a target:
```
python aun-map.py -u <TARGET_URL_OR_IP>
```



## Nmap Commands Executed

The tool executes the following Nmap scans:

`*` Vulnerability Scan: nmap -d -Pn --script vuln

`*` HTTP Slowloris Check: nmap --script http-slowloris-check

`*` SSL DH Params Check: nmap --script ssl-dh-params

`*` SSL Cipher Enumeration: nmap -sV --script ssl-enum-ciphers -p 443

`*` Full Port Scan: nmap -p-


## Output

Each scan’s output is saved in the nmap/ directory with filenames corresponding to the target and the scan type, e.g., example.com_nmap-vuln.txt.

## Key Highlights

`*` Efficient and Parallel Execution: Reduces the time taken for scanning by running tasks in parallel.

`*` Real-Time Feedback: Displays progress for each scan in real-time.

`*` Graceful Exit: Stops all scans cleanly when interrupted.

## License

[MIT](https://choosealicense.com/licenses/mit/)
