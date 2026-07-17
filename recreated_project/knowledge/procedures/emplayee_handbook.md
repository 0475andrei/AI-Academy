# Internal SOC Handbook

## NovaCore Security Operations Center - Analyst and Engineering Guide

### Version 5.0 (Restricted Internal Documentation)

***

# SOC Onboarding and Secure Provisioning

## Overview

The onboarding process for the NovaCore Security Operations Center (SOC) is strictly controlled to maintain the integrity of our Zero Trust architecture. Every Security Analyst, Incident Responder, and Threat Intelligence Engineer must adhere to these baseline protocols before accessing live monitoring environments.

The onboarding program is coordinated jointly by Identity and Access Management (IAM), Security Engineering, and the SOC Director. 

The standard onboarding timeline consists of the following phases:
* Pre-boarding background verification and clearance
* First day secure hardware provisioning
* First week IAM configuration and Privileged Access Management (PAM) enrollment
* First month monitored triage shadowing
* Ninety-day independent Incident Response (IR) evaluation

***

## Secure Workstation Provisioning

### Hardware Assignment

SOC personnel do not receive standard corporate laptops. All security staff are issued specialized hardware configured for isolated analysis and secure infrastructure management.

Threat Intelligence and Malware Analysts typically receive:
* Dell Precision Mobile Workstations (64GB RAM minimum)
* Hardware-level virtualization support enabled
* Air-gapped secondary machines for live malware detonation

Security Engineers and SOC Analysts typically receive:
* Lenovo ThinkPad P-Series
* Minimum 32 GB RAM
* Encrypted NVMe storage drives

The standard SOC workstation configuration includes:
* Full disk encryption (XTS-AES-256)
* Endpoint Detection and Response (EDR) agent with tamper protection
* Disabled USB mass storage mounting
* Virtual Machine software for isolated browser instances
* Dedicated VPN client restricted to split-tunneling

### First Login Procedure

On the first login:
1. Connect via the dedicated provisioning VLAN.
2. Authenticate using the temporary cryptographic token provided by IAM.
3. Establish a permanent passphrase (minimum 24 characters).
4. Register the assigned hardware security key (YubiKey/Titan).
5. Allow the automated compliance script to execute and verify firmware signatures.

***

## Access Control and Identity Management

### Corporate Identity and PAM

Analysts receive standard corporate accounts, but all access to production security tools, firewalls, and EDR consoles is governed by Privileged Access Management (PAM).

Standard operations require:
* Ephemeral credentials generated per session.
* Time-bound access grants for specific investigations.
* Mandatory Multi-Factor Authentication (MFA) for every privilege escalation.

### SSH Key Registration

Engineers accessing backend logging infrastructure must register SSH keys according to strict cryptographic standards:
* Ed25519 algorithm only (RSA is deprecated for SOC infrastructure).
* Keys must be protected by a secure passphrase.
* Keys are automatically rotated and revoked every 30 days.
* Forwarding of SSH agents is explicitly prohibited.

***

## Incident Response (IR) Protocols

### Triage Classification

Incidents are classified based on severity and potential impact to organizational assets. CYBriAN, our AI Cybersecurity Analyst, assists in initial automated triage.

#### Level 1: Low Priority
Examples: Suspicious spam emails, failed login attempts (below lockout threshold), anomalous but non-malicious network traffic.
Action: Automatically logged and resolved by CYBriAN or assigned to Tier 1 Analysts for verification.

#### Level 2: Medium Priority
Examples: Malware detected and quarantined by EDR, targeted phishing attempts, unusual lateral port scanning.
Action: Requires human verification. Tier 2 Analysts must isolate the affected endpoint and analyze the execution chain.

#### Level 3: High Priority
Examples: Verified credential theft, command and control (C2) beacons, unauthorized database access.
Action: Immediate containment. Network isolation of affected segments. Incident Commander is designated.

#### Level 4: Critical Priority (Active Breach)
Examples: Active ransomware encryption, confirmed data exfiltration, compromise of domain controllers.
Action: Full Incident Response mobilization. Implementation of network kill-switches. Executive leadership notification.

### Phishing and Email Threat Analysis

When a user reports a phishing email:
1. The email must be forwarded to the automated sandbox environment.
2. Analysts must extract Indicators of Compromise (IoCs), including header data, sender IP, and embedded URLs.
3. Domains must be checked against internal threat intelligence feeds.
4. Users must be instructed not to click any links and to delete the email immediately upon containment.

***

## Operational Security (OPSEC)

### Handling Indicators of Compromise (IoCs)

When sharing malicious IPs, domains, or file hashes, personnel must defang the data to prevent accidental execution or resolution.
* Example domain: `malicious[.]com`
* Example IP: `192[.]168[.]1[.]1`
* Example URL: `hxxps://attacker[.]net/payload`

### Traffic Light Protocol (TLP)

All threat intelligence reports generated by CYBriAN or human analysts must include a TLP classification:
* TLP:RED - Strictly for the designated recipients only.
* TLP:AMBER - Limited disclosure within the organization on a strict need-to-know basis.
* TLP:GREEN - Releasable within the sector and partner organizations.
* TLP:CLEAR - Unrestricted public release.

***

## Emergency Isolation Procedures

In the event of a confirmed Level 4 Critical Breach, Tier 3 Analysts and Incident Commanders are authorized to execute emergency containment protocols.

This includes:
* Terminating all external VPN connections.
* Null-routing malicious subnets at the perimeter firewall.
* Forcing a global password reset and session invalidation for all active directories.
* Disconnecting physical uplinks to affected data center segments.
