# Network Packet Analysis Report Generator

This Python script generates a comprehensive PDF report analyzing network packet captures. It processes CSV files (converted from Wireshark PCAP files), performs protocol-specific analysis, and creates visualizations and tabulated summaries.

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

## Usage
### Step 1: Convert PCAP Files to CSV
1. Open your PCAP file(s) in Wireshark
2. Go to `File > Export Objects > Export Packet Dissections > As CSV...`
3. Select desired fields (minimum: `Protocol`, `Source`, `Destination`, `Info`)
4. Save each file into the `csvs/` directory
   - Example: `capture1.csv`, `capture2.csv`, etc.

### Step 2: Generate the Report
1. Ensure your CSV files are in the `csvs/` directory
2. Run the script:
```bash
python network_report_generator.py
```
3. Find the output PDF at `network_analysis_report.pdf`

## Configuration
Edit these variables in the script:
- `CSV_FOLDER`: Directory containing CSV files (default: `./csvs`)
- `PDF_OUTPUT`: Output PDF path (default: `./network_analysis_report.pdf`)
- `MAX_ROWS_PER_TABLE`: Maximum rows per table (default: 50)
- `REPORT_TITLE`: PDF report title
- `INCLUDE_GRAPH`: Toggle graph inclusion (default: True)

## Input Format
- **PCAP Files**: Captured network traffic (e.g., from Wireshark)
- **CSV Files**: Exported from Wireshark with at least:
  - `Protocol`: Protocol type (e.g., ARP, ICMP)
  - `Source`: Source IP
  - `Destination`: Destination IP
  - `Info`: Packet information/details

## Output
- **PDF Report** containing:
  - Summary section
  - Tables for each analysis type
  - Optional embedded trend graph
- **Console Output**: Confirmation of report generation
- **Temporary File**: `capture_trend.png` (if graph enabled)

## Script Structure
1. **CSV Loading**: Combines multiple CSV files
2. **Analysis**: Processes ARP, ICMP, and VLAN data
3. **Visualization**: Generates protocol trend graph (optional)
4. **PDF Generation**: Creates formatted report with tables and graph

## Example Workflow
1. Capture network traffic in Wireshark and save as `capture1.pcap`
2. Export to `csvs/capture1.csv` with required fields
3. Repeat for additional captures
4. Run the script:
```
Report saved to ./network_analysis_report.pdf
```
The PDF will include sections like:
- ARP Duplicate Detection
- ICMP Reachability Map
- VLAN Summary
- Capture Comparison Summary

## Notes
- Ensure Wireshark CSV exports include the required columns
- Place CSV files in the specified folder, or the script will raise an exception
- Large datasets may be truncated in tables for readability (configurable via `MAX_ROWS_PER_TABLE`)
- Graph generation requires sufficient data variation for meaningful visualization

## License
This project is open-source and available under the MIT License.
```

### Key Additions
- Added a section under **Usage** explaining how to convert PCAP files to CSV using Wireshark.
- Mentioned Wireshark as a requirement for PCAP-to-CSV conversion.
- Updated **Input Format** to clarify that PCAP files are the initial input, converted to CSV.
- Included an **Example Workflow** to tie the PCAP-to-CSV-to-report process together.

This version maintains the original structure while clearly integrating the PCAP-to-CSV workflow, making it accessible for users starting with Wireshark captures. Let me know if you'd like further refinements!
