# Metasploit Framework: Comprehensive Documentation

## 1. Database & Environment Setup
Before beginning, ensure the PostgreSQL database is initialized so that scan results are persisted and accessible for later modules.
- **Initialize Database**: `msfdb init`
- **Check Status**: `db_status`
- **List Discovered Hosts**: `hosts`
- **List Discovered Services**: `services`

## 2. Port Scanning (Auxiliary Modules)
Auxiliary modules are used for scanning, discovery, and enumeration.
- **TCP Connect Scan**: `use auxiliary/scanner/portscan/tcp`
- **SYN Scan (Faster/Stealthier)**: `use auxiliary/scanner/portscan/syn` (Requires root/admin)
- **UDP Scan**: `use auxiliary/scanner/portscan/udp`

### Common Configuration Options
| Option | Description | Example |
| :--- | :--- | :--- |
| RHOSTS | Target IP or CIDR range | `set RHOSTS 192.168.1.0/24` |
| PORTS | Ports to scan | `set PORTS 1-1024` |
| THREADS | Concurrent threads | `set THREADS 50` |
| VERBOSE | Display detailed output | `set VERBOSE true` |

## 3. Exploit Modules & Workflow
The standard workflow for exploitation follows the "Use, Set, Run" pattern:
1. **Search**: `search <keyword>`
2. **Select Module**: `use <module_path>`
3. **Show Options**: `show options`
4. **Configure**: `set <VARIABLE> <VALUE>`
5. **Execute**: `exploit`

## 4. Payload Selection
Payloads define what happens after the exploit is successful.
- **List Payloads**: `show payloads`
- **Reverse TCP Shell**: `windows/x64/meterpreter/reverse_tcp`
- **Payload Configuration**: Always match `LHOST` (your local IP) and `LPORT` (your listener port) with the payload settings.

## 5. Nmap Integration
For faster results, you can run Nmap directly from the Metasploit console, which automatically imports results into the database.
- **Command**: `db_nmap -sS -p- <target_ip>`

## 6. Security & Ethics
- **Scope**: Never scan systems without explicit, written authorization.
- **Disruption**: Port scanning can be noisy and potentially cause instability in sensitive network environments.