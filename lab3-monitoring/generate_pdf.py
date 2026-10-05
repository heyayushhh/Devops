import os
import sys
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = r"C:\Users\hp\Desktop\New folder\Devops\lab3-monitoring\Lab3_Monitoring_Prometheus_Grafana_Report.pdf"
SCREENSHOT_DIR = r"C:\Users\hp\Desktop\New folder\Devops\lab3-monitoring\screenshots"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "DevOps Lab 3 — Prometheus & Grafana Monitoring Report")
            self.drawRightString(612 - 54, 750, "heyayushhh/Devops")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)

        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 32, "Confidential — Academic & Laboratory DevOps Evaluation")
        self.drawRightString(612 - 54, 32, page_text)
        self.restoreState()


def get_scaled_image(img_path, max_width=490, max_height=250):
    if not os.path.exists(img_path):
        return None
    try:
        with PILImage.open(img_path) as im:
            w, h = im.size
            ratio = min(max_width / w, max_height / h)
            return RLImage(img_path, width=w * ratio, height=h * ratio)
    except Exception as e:
        print(f"Error loading image {img_path}: {e}")
        return None


def generate_report():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1A365D')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4A5568')
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2D3748'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1A202C')
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#718096'),
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=10
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#2D3748')
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("LAB 3 — MONITORING & OBSERVABILITY REPORT", title_style))
    story.append(Paragraph("Prometheus Metrics Collection & Grafana Visualization Pipeline", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2B6CB0'), spaceBefore=2, spaceAfter=10))

    # Meta table
    meta_data = [
        [Paragraph("<b>Course:</b> DevOps Engineering", table_cell_style), Paragraph("<b>Assignment:</b> Lab 3 — Q1 (5 Marks)", table_cell_style)],
        [Paragraph("<b>Repository:</b> heyayushhh/Devops", table_cell_style), Paragraph("<b>Target Application:</b> Python Microservice", table_cell_style)],
        [Paragraph("<b>Metrics Server:</b> Prometheus v2.51.0", table_cell_style), Paragraph("<b>Dashboard Platform:</b> Grafana v10.4.1", table_cell_style)],
        [Paragraph("<b>Evaluation Status:</b> Fully Verified & Operational", table_cell_style), Paragraph("<b>Date:</b> October 2026", table_cell_style)]
    ]
    meta_table = Table(meta_data, colWidths=[240, 250])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#EDF2F7')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Objective
    story.append(Paragraph("1. Objective", h1_style))
    story.append(Paragraph(
        "The objective of Lab 3 is to design, deploy, and verify an end-to-end monitoring pipeline using Prometheus and Grafana. "
        "The system collects real metrics from a live Python target application, stores time-series data, and renders interactive operational dashboards.",
        body_style
    ))

    # Section 2: Environment
    story.append(Paragraph("2. System Environment", h1_style))
    story.append(Paragraph(
        "The environment was inspected to guarantee strict resource isolation, preserving existing Lab 2 and Lab 3 components without port conflicts or container collisions.",
        body_style
    ))
    
    img01 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "01_environment.png"), max_height=180)
    if img01:
        story.append(img01)
        story.append(Paragraph("Figure 1: Host environment, Docker daemon, and Git repository state verification.", caption_style))

    # Section 3: Monitoring Architecture
    story.append(Paragraph("3. Monitoring Architecture", h1_style))
    story.append(Paragraph(
        "The architecture establishes a closed-loop monitoring pipeline on an isolated bridge network (<code>lab3-monitoring-net</code>). "
        "The Python target application exposes metrics over HTTP on port 8000. Prometheus periodically scrapes <code>/metrics</code> every 5 seconds on port 9090, "
        "and Grafana queries Prometheus via PromQL to power dynamic visualization panels on port 3000.",
        body_style
    ))

    arch_data = [
        [Paragraph("Pipeline Stage", table_header_style), Paragraph("Component", table_header_style), Paragraph("Port / Network", table_header_style), Paragraph("Protocol / Function", table_header_style)],
        [Paragraph("1. Metric Producer", table_cell_style), Paragraph("<code>lab3-monitoring-app</code>", table_cell_style), Paragraph("8000 / <code>lab3-monitoring-net</code>", table_cell_style), Paragraph("Python Prometheus Client Exposition", table_cell_style)],
        [Paragraph("2. Metric Ingestion", table_cell_style), Paragraph("<code>lab3-prometheus</code>", table_cell_style), Paragraph("9090 / <code>lab3-monitoring-net</code>", table_cell_style), Paragraph("HTTP Scrape (5s interval) & TSDB Storage", table_cell_style)],
        [Paragraph("3. Visualization", table_cell_style), Paragraph("<code>lab3-grafana</code>", table_cell_style), Paragraph("3000 / <code>lab3-monitoring-net</code>", table_cell_style), Paragraph("PromQL Queries & Live Dashboards", table_cell_style)]
    ]
    arch_table = Table(arch_data, colWidths=[100, 120, 130, 140])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    img02 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "02_monitoring_project.png"), max_height=170)
    if img02:
        story.append(img02)
        story.append(Paragraph("Figure 2: Isolated Lab 3 monitoring workspace directory structure.", caption_style))

    # Page Break for clean reading
    story.append(PageBreak())

    # Section 4 & 5: Target Application & Metrics Exposed
    story.append(Paragraph("4. Target Application & Metrics Exposition", h1_style))
    story.append(Paragraph(
        "A lightweight Python microservice was constructed utilizing the official <code>prometheus_client</code> library. "
        "It provides standard service endpoints (<code>/</code>, <code>/health</code>, <code>/api/data</code>, <code>/api/error</code>) "
        "and publishes live telemetry on <code>/metrics</code> without fabricated or static values.",
        body_style
    ))

    metrics_table_data = [
        [Paragraph("Metric Identifier", table_header_style), Paragraph("Type", table_header_style), Paragraph("Labels", table_header_style), Paragraph("Semantic Purpose", table_header_style)],
        [Paragraph("<code>http_requests_total</code>", table_cell_style), Paragraph("Counter", table_cell_style), Paragraph("<code>method, endpoint, status</code>", table_cell_style), Paragraph("Tracks cumulative request count across all routes and responses.", table_cell_style)],
        [Paragraph("<code>http_request_duration_seconds</code>", table_cell_style), Paragraph("Histogram", table_cell_style), Paragraph("<code>method, endpoint</code>", table_cell_style), Paragraph("Records request execution latency distribution in seconds.", table_cell_style)],
        [Paragraph("<code>app_uptime_seconds</code>", table_cell_style), Paragraph("Gauge", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Monitors continuous service uptime in seconds.", table_cell_style)],
        [Paragraph("<code>up</code>", table_cell_style), Paragraph("Gauge", table_cell_style), Paragraph("<code>job, instance</code>", table_cell_style), Paragraph("Core Prometheus health probe indicating liveness (1 = UP).", table_cell_style)]
    ]
    m_table = Table(metrics_table_data, colWidths=[140, 60, 110, 180])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 8))

    img03 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "03_target_application.png"), max_height=140)
    if img03:
        story.append(img03)
        story.append(Paragraph("Figure 3: Target Application JSON response on root endpoint (Port 8000).", caption_style))

    img04 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "04_metrics_endpoint.png"), max_height=140)
    if img04:
        story.append(img04)
        story.append(Paragraph("Figure 4: Raw Prometheus exposition-format metrics published at /metrics.", caption_style))

    # Page Break
    story.append(PageBreak())

    # Section 6 & 7: Prometheus Setup & Target Verification
    story.append(Paragraph("5. Prometheus Setup & Target Scraping", h1_style))
    story.append(Paragraph(
        "Prometheus was configured with a custom scrape configuration (<code>prometheus.yml</code>) targeting <code>lab3-monitoring-app:8000</code>. "
        "The scrape interval was set to 5 seconds to provide high-frequency metric collection for accurate rate calculations.",
        body_style
    ))

    img06 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "06_prometheus_target_up.png"), max_height=170)
    if img06:
        story.append(img06)
        story.append(Paragraph("Figure 5: Prometheus Web UI Targets page verifying target state is UP (1/1 up).", caption_style))

    story.append(Paragraph("6. PromQL Query Evaluation", h1_style))
    story.append(Paragraph(
        "Realistic traffic was dispatched against all microservice endpoints. Prometheus evaluated PromQL expressions "
        "including request sums grouped by endpoint, status code distributions, and application uptime:",
        body_style
    ))

    img07 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "07_prometheus_query.png"), max_height=170)
    if img07:
        story.append(img07)
        story.append(Paragraph("Figure 6: PromQL metric evaluation and command line verification.", caption_style))

    # Page Break
    story.append(PageBreak())

    # Section 8 & 9: Grafana Setup & Dashboard Visualization
    story.append(Paragraph("7. Grafana Datasource & Dashboard Setup", h1_style))
    story.append(Paragraph(
        "Grafana was deployed on port 3000 with automated provisioning for both data sources and dashboards. "
        "The Prometheus data source was configured with proxy access to <code>http://lab3-prometheus:9090</code>.",
        body_style
    ))

    img09 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "09_grafana_datasource.png"), max_height=160)
    if img09:
        story.append(img09)
        story.append(Paragraph("Figure 7: Grafana Data Sources interface showing Prometheus connected and healthy.", caption_style))

    story.append(Paragraph("8. Real-Time Grafana Dashboard Panels", h1_style))
    story.append(Paragraph(
        "The production dashboard (<i>Lab 3 — Application Monitoring</i>) comprises 8 specialized panels providing comprehensive operational insight:",
        body_style
    ))

    dash_panels_data = [
        [Paragraph("Panel Title", table_header_style), Paragraph("Visualization Type", table_header_style), Paragraph("PromQL Expression", table_header_style)],
        [Paragraph("Application Availability", table_cell_style), Paragraph("Stat (Threshold Color)", table_cell_style), Paragraph("<code>up{job=\"lab3-monitoring-app\"}</code>", table_cell_style)],
        [Paragraph("Total HTTP Requests", table_cell_style), Paragraph("Stat with Sparkline", table_cell_style), Paragraph("<code>sum(http_requests_total{job=\"lab3-monitoring-app\"})</code>", table_cell_style)],
        [Paragraph("Application Uptime", table_cell_style), Paragraph("Stat (Seconds Unit)", table_cell_style), Paragraph("<code>app_uptime_seconds{job=\"lab3-monitoring-app\"}</code>", table_cell_style)],
        [Paragraph("Current Request Rate", table_cell_style), Paragraph("Stat (reqps Unit)", table_cell_style), Paragraph("<code>sum(rate(http_requests_total{job=\"...\"}[1m]))</code>", table_cell_style)],
        [Paragraph("HTTP Request Rate by Endpoint", table_cell_style), Paragraph("Time Series Graph", table_cell_style), Paragraph("<code>sum(rate(http_requests_total{...}[1m])) by (endpoint)</code>", table_cell_style)],
        [Paragraph("Cumulative Requests by Endpoint", table_cell_style), Paragraph("Bar Chart", table_cell_style), Paragraph("<code>sum(http_requests_total{...}) by (endpoint)</code>", table_cell_style)],
        [Paragraph("Requests Breakdown by Status", table_cell_style), Paragraph("Donut Pie Chart", table_cell_style), Paragraph("<code>sum(http_requests_total{...}) by (status)</code>", table_cell_style)],
        [Paragraph("Average Request Latency", table_cell_style), Paragraph("Time Series Graph", table_cell_style), Paragraph("<code>sum(rate(..._sum[1m])) / sum(rate(..._count[1m]))</code>", table_cell_style)]
    ]
    dp_table = Table(dash_panels_data, colWidths=[140, 110, 240])
    dp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(dp_table)
    story.append(Spacer(1, 10))

    # Page Break
    story.append(PageBreak())

    story.append(Paragraph("9. Live Metrics Demonstration & Verification", h1_style))
    story.append(Paragraph(
        "Live traffic generated against the microservice immediately reflected in the Grafana dashboard. "
        "All visual panels displayed non-empty values, active time series curves, and proportional status code breakdowns.",
        body_style
    ))

    img10 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "10_grafana_dashboard.png"), max_height=200)
    if img10:
        story.append(img10)
        story.append(Paragraph("Figure 8: Grafana Dashboard overview displaying live Prometheus metric telemetry.", caption_style))

    img11 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "11_grafana_real_metrics.png"), max_height=200)
    if img11:
        story.append(img11)
        story.append(Paragraph("Figure 9: Close-up of live Grafana metrics: Availability (UP), Request Rate, Status Donut, and Latency.", caption_style))

    # Page Break
    story.append(PageBreak())

    story.append(Paragraph("10. Full Stack Health Audit", h1_style))
    story.append(Paragraph(
        "A complete audit confirmed all three containers are healthy, connected to <code>lab3-monitoring-net</code>, and operating without errors.",
        body_style
    ))

    img12 = get_scaled_image(os.path.join(SCREENSHOT_DIR, "12_monitoring_stack_final.png"), max_height=180)
    if img12:
        story.append(img12)
        story.append(Paragraph("Figure 10: End-to-end monitoring stack container status and health audit.", caption_style))

    story.append(Paragraph("11. Key Observations & Takeaways", h1_style))
    story.append(Paragraph(
        "1. <b>Push vs Pull Telemetry:</b> Prometheus's pull-based polling model simplifies service discovery in containerized environments by requiring microservices to expose only an unauthenticated lightweight endpoint (<code>/metrics</code>).<br/>"
        "2. <b>Multi-Dimensional Labeling:</b> Adding labels such as <code>endpoint</code> and <code>status</code> enables flexible aggregation in PromQL, such as separating standard traffic from errors.<br/>"
        "3. <b>Zero-Touch Provisioning:</b> Infrastructure-as-code provisioning in Grafana guarantees identical visualization environments across staging and production deployments.",
        body_style
    ))

    story.append(Paragraph("12. Conclusion", h1_style))
    story.append(Paragraph(
        "The Lab 3 monitoring assignment has been successfully implemented and validated. The end-to-end telemetry pipeline "
        "(<b>Target Application &rarr; /metrics &rarr; Prometheus &rarr; PromQL &rarr; Grafana</b>) is fully functional, robust, and verified with genuine operational metrics.",
        body_style
    ))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated PDF Report at: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")

if __name__ == '__main__':
    generate_report()
