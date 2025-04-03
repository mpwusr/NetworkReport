# Network Packet Analysis Report Generator

This Python script generates a comprehensive PDF report analyzing network packet captures stored in CSV format (e.g., from Wireshark exports). It processes multiple CSV files, performs protocol-specific analysis, and creates visualizations and tabulated summaries.

## Features
- **ARP Analysis**
  - Detects duplicate ARP requests
  - Identifies unanswered ARP requests
- **ICMP Analysis**
  - Maps reachability between source/destination pairs
  - Identifies error packets (unreachable, time exceeded, redirect)
- **VLAN Analysis**
  - Summarizes VLAN traffic
  - Checks VLAN ID consistency
- **Capture Summary**
  - Compares packet counts across files and protocols
- **Visualization**
  - Optional trend graph of protocol counts across captures
- **PDF Report**
  - Professional formatting with headers and tables
  - Configurable row limits for readability
  - Embedded graph option

## Requirements
```bash
pip install pandas matplotlib fpdf
