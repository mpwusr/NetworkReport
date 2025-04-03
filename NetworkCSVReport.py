"""
Network Report Generator (Enhanced Version)
"""

import glob
import os

import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

# -------------------- CONFIG --------------------
CSV_FOLDER = './csvs'              # Input folder for CSVs
PDF_OUTPUT = './network_analysis_report.pdf'  # PDF output path
MAX_ROWS_PER_TABLE = 50            # Max rows per table
REPORT_TITLE = "Network Packet Analysis Report"
INCLUDE_GRAPH = True               # Embed capture trend graph in PDF
# ------------------------------------------------

# -------------------- LOAD CSV --------------------
csv_files = glob.glob(os.path.join(CSV_FOLDER, '*.csv'))
if not csv_files:
    raise Exception("No CSV files found in ./csvs directory")

combined_data = []
for file in csv_files:
    df = pd.read_csv(file)
    df['source_file'] = os.path.basename(file)
    combined_data.append(df)

df_combined = pd.concat(combined_data, ignore_index=True)

# -------------------- ANALYSIS --------------------

# ARP
arp_data = df_combined[df_combined['Protocol'].str.contains('ARP', na=False)]
arp_requests = arp_data[arp_data['Info'].str.contains('Who has', na=False)].copy()
arp_requests['Target_IP'] = arp_requests['Info'].str.extract(r'Who has ([0-9\.]+)')
arp_responses = arp_data[arp_data['Info'].str.contains('is at', na=False)].copy()
arp_responses['Target_IP'] = arp_responses['Info'].str.extract(r'([0-9\.]+) is at')
arp_duplicates = arp_requests.groupby(['Target_IP']).size().reset_index(name='Request_Count')
arp_duplicates = arp_duplicates[arp_duplicates['Request_Count'] > 1]
arp_unanswered = arp_requests[~arp_requests['Target_IP'].isin(arp_responses['Target_IP'])]

# ICMP
icmp_data = df_combined[df_combined['Protocol'].str.contains('ICMP', na=False)]
icmp_summary = icmp_data.groupby(['Source', 'Destination']).size().reset_index(name='ICMP_Packets')
icmp_errors = icmp_data[icmp_data['Info'].str.contains('unreachable|time exceeded|redirect', case=False, na=False)]

# VLAN
vlan_data = df_combined[df_combined['Info'].str.contains('vlan|802.1Q', case=False, na=False)]
vlan_summary = vlan_data.groupby(['Source', 'Destination']).size().reset_index(name='VLAN_Packets')
vlan_consistency = vlan_data['Info'].str.extract(r'vlan (\d+)').value_counts().reset_index(name='Count')

# Capture Summary
capture_summary = df_combined.groupby(['source_file', 'Protocol']).size().reset_index(name='Packet_Count')

# -------------------- VISUALIZATION --------------------
if INCLUDE_GRAPH:
    plt.figure(figsize=(10,5))
    for proto in capture_summary['Protocol'].unique():
        subset = capture_summary[capture_summary['Protocol'] == proto]
        plt.plot(subset['source_file'], subset['Packet_Count'], marker='o', label=proto)
    plt.title("Protocol Counts Over Captures")
    plt.xlabel("Capture File")
    plt.ylabel("Packet Count")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('capture_trend.png')

# -------------------- PDF GENERATION --------------------
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, REPORT_TITLE, ln=True, align="C")
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(3)

    def chapter_body(self, body):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, body)
        self.ln()

    def table_from_dataframe(self, df, title):
        self.chapter_title(title)
        if df.empty:
            self.chapter_body("No data available.")
            return
        self.set_font("Arial", "", 8)
        effective_page_width = self.w - 2 * self.l_margin
        col_width = effective_page_width / len(df.columns)
        for col in df.columns:
            self.cell(col_width, 8, str(col)[:15], border=1)
        self.ln()
        for i in range(min(len(df), MAX_ROWS_PER_TABLE)):
            for col in df.columns:
                self.cell(col_width, 8, str(df.iloc[i][col])[:15], border=1)
            self.ln()
        if len(df) > MAX_ROWS_PER_TABLE:
            self.chapter_body(f"... Table truncated to {MAX_ROWS_PER_TABLE} rows for readability.")
        self.ln(5)

pdf = PDFReport()
pdf.add_page()
pdf.chapter_title("Summary")
pdf.chapter_body("This report includes:\n- ARP Duplicate Detection\n- ICMP Reachability & Error Analysis\n- VLAN Summary\n- Capture Comparison\n- Automatic Graphs\n\nAutomatically generated from provided CSVs.")

# -------------------- Insert Data --------------------
pdf.table_from_dataframe(arp_duplicates, "ARP Duplicate Detection")
pdf.table_from_dataframe(arp_unanswered, "ARP Unanswered Requests")
pdf.table_from_dataframe(icmp_summary, "ICMP Reachability Map")
pdf.table_from_dataframe(icmp_errors, "ICMP Errors Detected")
pdf.table_from_dataframe(vlan_summary, "VLAN Summary")
pdf.table_from_dataframe(vlan_consistency, "VLAN ID Consistency Check")
pdf.table_from_dataframe(capture_summary, "Capture Comparison Summary")

# Embed graph if available
if INCLUDE_GRAPH and os.path.exists("capture_trend.png"):
    pdf.image("capture_trend.png", w=pdf.w - 40)

pdf.output(PDF_OUTPUT)
print(f"Report saved to {PDF_OUTPUT}")
