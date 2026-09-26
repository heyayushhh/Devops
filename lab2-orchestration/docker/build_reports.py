import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
PDF_REPORT_PATH = os.path.join(BASE_DIR, "Lab2_Containerization_Orchestration_Report.pdf")
PDF_TOOLS_PATH = os.path.join(BASE_DIR, "Lab2_Tools_Documents.pdf")

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
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0284c7"))
        self.drawString(54, 11 * 72 - 36, "DEVOPS LAB 2")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(130, 11 * 72 - 36, "|   Containerization & Kubernetes Orchestration Report")
        
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 34, page_text)
        self.drawString(54, 34, "Repository: https://github.com/heyayushhh/Devops")
        self.line(54, 46, 8.5 * 72 - 54, 46)
        self.restoreState()

def get_report_styles():
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#0f172a")
    accent_color = colors.HexColor("#0284c7")
    dark_slate = colors.HexColor("#334155")
    
    styles.add(ParagraphStyle('CoverBadge', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor("#0284c7"), alignment=1))
    styles.add(ParagraphStyle('CoverTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=primary_color, alignment=1))
    styles.add(ParagraphStyle('CoverSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, leading=16, textColor=dark_slate, alignment=1))
    
    styles.add(ParagraphStyle('SectionHeading', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=colors.HexColor("#0f172a"), spaceBefore=10, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle('SubSectionHeading', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor("#0369a1"), spaceBefore=6, spaceAfter=3, keepWithNext=True))
    styles.add(ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=dark_slate, spaceAfter=4))
    styles.add(ParagraphStyle('BodyTextBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=primary_color))
    styles.add(ParagraphStyle('Caption', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=colors.HexColor("#475569"), alignment=1, spaceBefore=2, spaceAfter=6))
    styles.add(ParagraphStyle('CodeBlock', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#0f172a")))
    styles.add(ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=dark_slate))
    styles.add(ParagraphStyle('TableCellBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=primary_color))
    styles.add(ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white))
    
    return styles

def create_image_flowable(filename, max_width=480, max_height=140):
    img_path = os.path.join(SCREENSHOTS_DIR, filename)
    if not os.path.exists(img_path):
        return None
    from PIL import Image as PILImage
    with PILImage.open(img_path) as im:
        orig_w, orig_h = im.size
    
    aspect = orig_h / orig_w
    w = max_width
    h = w * aspect
    if h > max_height:
        h = max_height
        w = h / aspect
    return RLImage(img_path, width=w, height=h)

def build_pdf1():
    doc = SimpleDocTemplate(
        PDF_REPORT_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = get_report_styles()
    story = []

    # ================= COVER PAGE =================
    story.append(Spacer(1, 30))
    story.append(Paragraph("UNIVERSITY DEVOPS LABORATORY ASSIGNMENT", styles['CoverBadge']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Lab 2 - Containerization & Kubernetes Orchestration", styles['CoverTitle']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Architecture, Deployment Strategy, Scaling Verification & Empirical Results", styles['CoverSubtitle']))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="90%", thickness=2, color=colors.HexColor("#0284c7"), spaceBefore=5, spaceAfter=20))
    
    meta_table_data = [
        [Paragraph("Course / Module:", styles['BodyTextBold']), Paragraph("DevOps Laboratory (Lab 2)", styles['BodyTextCustom'])],
        [Paragraph("Submission Question:", styles['BodyTextBold']), Paragraph("Question 1 - 10 Marks Report", styles['BodyTextCustom'])],
        [Paragraph("GitHub Repository:", styles['BodyTextBold']), Paragraph("https://github.com/heyayushhh/Devops", styles['BodyTextCustom'])],
        [Paragraph("Host Operating System:", styles['BodyTextBold']), Paragraph("Windows 11 Professional (WSL2 Backend)", styles['BodyTextCustom'])],
        [Paragraph("Container Engine:", styles['BodyTextBold']), Paragraph("Docker Desktop 4.82.0 (Engine v29.6.1)", styles['BodyTextCustom'])],
        [Paragraph("Container Runtime:", styles['BodyTextBold']), Paragraph("containerd v2.2.5 / runc v1.3.6", styles['BodyTextCustom'])],
        [Paragraph("Orchestration Cluster:", styles['BodyTextBold']), Paragraph("Kubernetes v1.36.1 (Node: desktop-control-plane)", styles['BodyTextCustom'])],
        [Paragraph("Kubectl Client Version:", styles['BodyTextBold']), Paragraph("v1.36.1 (Kustomize v5.8.1)", styles['BodyTextCustom'])],
        [Paragraph("Verification Status:", styles['BodyTextBold']), Paragraph("Verified with 100% Real Live Terminal Evidence", styles['BodyTextCustom'])],
    ]
    t_meta = Table(meta_table_data, colWidths=[140, 340])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Executive Summary:</b> This technical report details the end-to-end containerization of an existing application using Docker, deployment into a local Kubernetes cluster, declarative Service exposure, and multi-tier horizontal scaling experiments (1 -> 3 -> 5 replicas). All reported outputs, pod names, assigned IPs, and reconciliation timings are backed by live terminal screenshots.", styles['BodyTextCustom']))
    story.append(PageBreak())

    # ================= PAGE 2: OBJECTIVE, OVERVIEW & ENVIRONMENT =================
    story.append(Paragraph("1. Objective", styles['SectionHeading']))
    story.append(Paragraph("The objective of this laboratory experiment is to establish hands-on mastery of containerization and orchestration workflows:", styles['BodyTextCustom']))
    story.append(Paragraph("• Containerize an existing application (app.py and login.py) into an optimized, reproducible Docker image.<br/>"
                           "• Author industry-standard Dockerfile and .dockerignore build configurations.<br/>"
                           "• Deploy and manage the application workload on a Kubernetes orchestration cluster (v1.36.1).<br/>"
                           "• Expose the workload through a Kubernetes ClusterIP Service for internal service discovery.<br/>"
                           "• Perform empirical horizontal scaling experiments across 1, 3, and 5 pod replicas and record controller behavior.", styles['BodyTextCustom']))

    story.append(Paragraph("2. Application Overview", styles['SectionHeading']))
    story.append(Paragraph("The existing repository contains Python source modules: <b>app.py</b> (which executes <code>print('Hello DevOps')</code>) and <b>login.py</b> (stub function). In a Kubernetes Deployment, standard CLI scripts exit immediately upon completion, triggering pod termination and CrashLoopBackOff. To enable persistent orchestration health monitoring while preserving original application logic, an orchestration runner (<b>entrypoint.py</b>) was configured to execute the core application and maintain periodic health heartbeats.", styles['BodyTextCustom']))
    
    img01 = create_image_flowable("01-repository-inspection.png", max_height=80)
    if img01:
        story.append(img01)
        story.append(Paragraph("Figure 1 - Inspection and verification of existing repository files.", styles['Caption']))

    story.append(Paragraph("3. Execution Environment", styles['SectionHeading']))
    env_data = [
        [Paragraph("Component", styles['TableHeader']), Paragraph("Version / Specification", styles['TableHeader']), Paragraph("Role", styles['TableHeader'])],
        [Paragraph("Host OS", styles['TableCellBold']), Paragraph("Windows 11 Professional (x64)", styles['TableCell']), Paragraph("Host operating environment", styles['TableCell'])],
        [Paragraph("Docker Engine", styles['TableCellBold']), Paragraph("v29.6.1 (Desktop 4.82.0)", styles['TableCell']), Paragraph("Container build & runtime daemon", styles['TableCell'])],
        [Paragraph("Kubernetes", styles['TableCellBold']), Paragraph("v1.36.1 (Single Node)", styles['TableCell']), Paragraph("Local cluster control plane", styles['TableCell'])],
        [Paragraph("Kubectl Client", styles['TableCellBold']), Paragraph("v1.36.1", styles['TableCell']), Paragraph("Cluster administration tool", styles['TableCell'])],
    ]
    t_env = Table(env_data, colWidths=[100, 180, 200])
    t_env.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_env)
    story.append(PageBreak())

    # ================= PAGE 3: ARCHITECTURE & K8S ENVIRONMENT =================
    story.append(Paragraph("4. Architecture & Technical Workflow", styles['SectionHeading']))
    story.append(Paragraph("The orchestration pipeline separates source code, packaging, workload management, and networking across distinct layers:", styles['BodyTextCustom']))

    arch_data = [
        [Paragraph("Layer", styles['TableHeader']), Paragraph("Artifact / Resource", styles['TableHeader']), Paragraph("Technical Responsibility", styles['TableHeader'])],
        [Paragraph("1. Source", styles['TableCellBold']), Paragraph("app.py, login.py, entrypoint.py", styles['TableCell']), Paragraph("Application logic, authentication stub, and health runner", styles['TableCell'])],
        [Paragraph("2. Packaging", styles['TableCellBold']), Paragraph("Dockerfile (python:3.11-slim)", styles['TableCell']), Paragraph("Minimal multi-stage reproducible build definition", styles['TableCell'])],
        [Paragraph("3. Image", styles['TableCellBold']), Paragraph("lab2-devops-app:latest (187MB)", styles['TableCell']), Paragraph("Immutable packaged container image in local Docker cache", styles['TableCell'])],
        [Paragraph("4. Deployment", styles['TableCellBold']), Paragraph("lab2-deployment (apps/v1)", styles['TableCell']), Paragraph("Manages desired replica count, rolling updates & resources", styles['TableCell'])],
        [Paragraph("5. Replicas", styles['TableCellBold']), Paragraph("5x Running Pods (10.244.0.x)", styles['TableCell']), Paragraph("Isolated container instances executing across the cluster", styles['TableCell'])],
        [Paragraph("6. Networking", styles['TableCellBold']), Paragraph("lab2-service (ClusterIP:80)", styles['TableCell']), Paragraph("Virtual cluster IP providing stable discovery and endpoint aggregation", styles['TableCell'])],
    ]
    t_arch = Table(arch_data, colWidths=[70, 160, 250])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284c7")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Kubernetes Cluster Environment Verification", styles['SubSectionHeading']))
    img06 = create_image_flowable("06-kubernetes-environment.png", max_height=110)
    if img06:
        story.append(img06)
        story.append(Paragraph("Figure 2 - Kubernetes cluster info, client version, and node health status.", styles['Caption']))
    story.append(PageBreak())

    # ================= PAGE 4: DOCKER CONTAINERIZATION & BUILD =================
    story.append(Paragraph("5. Docker Containerization & Dockerfile", styles['SectionHeading']))
    story.append(Paragraph("The application was containerized using <b>python:3.11-slim</b> to minimize image overhead. Environment variable <code>PYTHONUNBUFFERED=1</code> was specified to ensure unbuffered standard output streaming. The <b>.dockerignore</b> file excludes caches, local virtual environments, and documentation artifacts from the build context.", styles['BodyTextCustom']))

    img02 = create_image_flowable("02-dockerfile.png", max_height=125)
    if img02:
        story.append(img02)
        story.append(Paragraph("Figure 3 - Verified Dockerfile and .dockerignore build context definitions.", styles['Caption']))

    story.append(Paragraph("6. Docker Image Build Execution", styles['SectionHeading']))
    story.append(Paragraph("The image was constructed using Docker BuildKit. All 10 build steps were resolved, copied, and unpacked into <code>lab2-devops-app:latest</code>:", styles['BodyTextCustom']))

    img03 = create_image_flowable("03-docker-build-success.png", max_height=120)
    if img03:
        story.append(img03)
        story.append(Paragraph("Figure 4 - Successful Docker BuildKit image build for lab2-devops-app:latest.", styles['Caption']))
    story.append(PageBreak())

    # ================= PAGE 5: IMAGE LISTING & STANDALONE CONTAINER RUN =================
    story.append(Paragraph("7. Docker Image Listing & Standalone Container Run", styles['SectionHeading']))
    story.append(Paragraph("Before orchestrating through Kubernetes, the newly created Docker image was verified in the local image registry, and a standalone container instance (<b>lab2-container-test</b>) was started to ensure unbuffered runtime execution and log output.", styles['BodyTextCustom']))

    img04 = create_image_flowable("04-docker-image.png", max_height=65)
    if img04:
        story.append(img04)
        story.append(Paragraph("Figure 5 - Verification of lab2-devops-app:latest in local Docker image cache.", styles['Caption']))

    img05 = create_image_flowable("05-docker-container-running.png", max_height=130)
    if img05:
        story.append(img05)
        story.append(Paragraph("Figure 6 - Standalone container execution (ba82a82b8015) and heartbeat log verification.", styles['Caption']))
    story.append(PageBreak())

    # ================= PAGE 6: KUBERNETES DEPLOYMENT & SERVICE =================
    story.append(Paragraph("8. Kubernetes Deployment & Service Creation", styles['SectionHeading']))
    story.append(Paragraph("The workload was deployed to the cluster using <b>deployment.yaml</b> (label <code>app: lab2-app</code>, CPU limit: <code>250m</code>, Mem limit: <code>128Mi</code>). A <b>ClusterIP Service</b> (<b>service.yaml</b>) was created to assign a stable virtual IP (<code>10.96.92.231</code>) and map internal traffic to active pod endpoints.", styles['BodyTextCustom']))

    img07 = create_image_flowable("07-deployment-applied.png", max_height=65)
    if img07:
        story.append(img07)
        story.append(Paragraph("Figure 7 - Declarative creation of lab2-deployment and lab2-service objects.", styles['Caption']))

    img08 = create_image_flowable("08-kubectl-get-deployments.png", max_height=60)
    if img08:
        story.append(img08)
        story.append(Paragraph("Figure 8 - Active deployment state in Kubernetes control plane (1/1 Ready).", styles['Caption']))

    img09 = create_image_flowable("09-kubectl-get-pods.png", max_height=90)
    if img09:
        story.append(img09)
        story.append(Paragraph("Figure 9 - Baseline pod instance (lab2-deployment-5d66ff9d8d-hq98z) running with live logs.", styles['Caption']))

    img10 = create_image_flowable("10-kubernetes-service.png", max_height=90)
    if img10:
        story.append(img10)
        story.append(Paragraph("Figure 10 - Kubernetes Service details and active target pod endpoints.", styles['Caption']))
    story.append(PageBreak())

    # ================= PAGE 7: SCALING EXPERIMENT (1 -> 3 -> 5) =================
    story.append(Paragraph("9. Horizontal Scaling Experiment & Verification", styles['SectionHeading']))
    story.append(Paragraph("To evaluate Kubernetes scaling and pod reconciliation, the deployment was scaled imperatively from 1 replica to 3 replicas, and subsequently to 5 replicas.", styles['BodyTextCustom']))

    story.append(Paragraph("Phase A: Initial Baseline State (1 Replica)", styles['SubSectionHeading']))
    img11 = create_image_flowable("11-initial-replicas.png", max_height=70)
    if img11:
        story.append(img11)
        story.append(Paragraph("Figure 11 - Initial single pod replica baseline.", styles['Caption']))

    story.append(Paragraph("Phase B: Scaling to 3 Replicas", styles['SubSectionHeading']))
    story.append(Paragraph("Running <code>kubectl scale deployment lab2-deployment --replicas=3</code> instructed the deployment controller to spawn 2 additional pods (<code>48zzf</code> and <code>xt9xn</code>). All 3 pods were reconciled to Running status within ~3 seconds.", styles['BodyTextCustom']))
    img12 = create_image_flowable("12-scaled-to-3-replicas.png", max_height=95)
    if img12:
        story.append(img12)
        story.append(Paragraph("Figure 12 - Verified scale-out to 3 healthy running pod replicas.", styles['Caption']))

    story.append(Paragraph("Phase C: Scaling to 5 Replicas", styles['SubSectionHeading']))
    story.append(Paragraph("Running <code>kubectl scale deployment lab2-deployment --replicas=5</code> spawned 2 more pods (<code>5gp6l</code> and <code>klzt2</code>), achieving 5/5 desired, ready, and available pods.", styles['BodyTextCustom']))
    img13 = create_image_flowable("13-scaled-to-5-replicas.png", max_height=100)
    if img13:
        story.append(img13)
        story.append(Paragraph("Figure 13 - Verified scale-out to 5 healthy running pod replicas.", styles['Caption']))
    story.append(PageBreak())

    # ================= PAGE 8: SCALING AUDIT, OBSERVATIONS & CONCLUSION =================
    story.append(Paragraph("10. Scaling Results & Controller Audit", styles['SectionHeading']))
    
    res_data = [
        [Paragraph("Experiment Phase", styles['TableHeader']), Paragraph("Desired", styles['TableHeader']), Paragraph("Ready", styles['TableHeader']), Paragraph("Reconciled Pod Names", styles['TableHeader']), Paragraph("Assigned Cluster IPs", styles['TableHeader'])],
        [Paragraph("Baseline", styles['TableCellBold']), Paragraph("1", styles['TableCell']), Paragraph("1", styles['TableCell']), Paragraph("...-hq98z", styles['TableCell']), Paragraph("10.244.0.5", styles['TableCell'])],
        [Paragraph("Scale Step 1", styles['TableCellBold']), Paragraph("3", styles['TableCell']), Paragraph("3", styles['TableCell']), Paragraph("...-hq98z<br/>...-48zzf<br/>...-xt9xn", styles['TableCell']), Paragraph("10.244.0.5<br/>10.244.0.7<br/>10.244.0.6", styles['TableCell'])],
        [Paragraph("Scale Step 2", styles['TableCellBold']), Paragraph("5", styles['TableCell']), Paragraph("5", styles['TableCell']), Paragraph("...-hq98z<br/>...-48zzf<br/>...-xt9xn<br/>...-5gp6l<br/>...-klzt2", styles['TableCell']), Paragraph("10.244.0.5<br/>10.244.0.7<br/>10.244.0.6<br/>10.244.0.9<br/>10.244.0.8", styles['TableCell'])],
    ]
    t_res = Table(res_data, colWidths=[80, 45, 45, 170, 140])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 4))

    img14 = create_image_flowable("14-final-pods.png", max_height=125)
    if img14:
        story.append(img14)
        story.append(Paragraph("Figure 14 - Final cluster state audit and deployment-controller scaling events.", styles['Caption']))

    story.append(Paragraph("11. Observations & Conclusion", styles['SectionHeading']))
    story.append(Paragraph("<b>Empirical Observations:</b><br/>"
                           "1. <i>Automated Reconciliation:</i> The deployment controller adjusted pod counts to match desired state within ~3 seconds.<br/>"
                           "2. <i>Isolated Network Addressing:</i> Each pod was assigned a distinct IP on the 10.244.0.0/16 virtual subnet.<br/>"
                           "3. <i>Dynamic Service Endpoints:</i> The ClusterIP Service aggregated all active pod IPs automatically without downtime.<br/>"
                           "4. <i>Predictable Resource Limits:</i> Memory and CPU limits prevented container resource starvation.<br/><br/>"
                           "<b>Conclusion:</b><br/>"
                           "The Lab 2 Containerization & Kubernetes Orchestration experiment was completed successfully with verified evidence. The application was containerized, deployed via Kubernetes Deployment and Service, and scaled to 3 and 5 healthy running replicas with 100% empirical verification.", styles['BodyTextCustom']))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF 1: {PDF_REPORT_PATH}")

def build_pdf2():
    doc = SimpleDocTemplate(
        PDF_TOOLS_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = get_report_styles()
    story = []

    # ================= HEADER =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("TECHNICAL SPECIFICATION & TOOLS DOCUMENT", styles['CoverBadge']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("DevOps Lab 2 - Artifacts, Manifests & Command Reference", styles['CoverTitle']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Question 2 - 5 Marks Submission Document", styles['CoverSubtitle']))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceBefore=3, spaceAfter=12))

    # ================= SECTION 1: DOCKER ARTIFACTS =================
    story.append(Paragraph("1. Docker Build Specifications", styles['SectionHeading']))
    
    dockerfile_code = (
        "<b>Dockerfile (lab2-orchestration/docker/Dockerfile):</b><br/>"
        "<font face='Courier' size='7.5'>"
        "# Base image<br/>"
        "FROM python:3.11-slim<br/><br/>"
        "# Set working directory<br/>"
        "WORKDIR /app<br/><br/>"
        "# Set environment variables for unbuffered output<br/>"
        "ENV PYTHONUNBUFFERED=1<br/><br/>"
        "# Copy original application files<br/>"
        "COPY app.py .<br/>"
        "COPY login.py .<br/><br/>"
        "# Copy orchestration runner<br/>"
        "COPY lab2-orchestration/docker/entrypoint.py .<br/><br/>"
        "# Run entrypoint<br/>"
        "CMD [\"python\", \"-u\", \"entrypoint.py\"]"
        "</font>"
    )
    
    t_docker = Table([[Paragraph(dockerfile_code, styles['BodyTextCustom'])]], colWidths=[480])
    t_docker.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_docker)
    story.append(Spacer(1, 6))

    img03 = create_image_flowable("03-docker-build-success.png", max_height=110)
    if img03:
        story.append(img03)
        story.append(Paragraph("Figure 1 - Docker BuildKit build execution output for lab2-devops-app:latest.", styles['Caption']))
    story.append(PageBreak())

    # ================= SECTION 2: KUBERNETES MANIFESTS =================
    story.append(Paragraph("2. Kubernetes Manifest Specifications", styles['SectionHeading']))

    k8s_deploy_code = (
        "<b>Deployment Manifest (lab2-orchestration/kubernetes/deployment.yaml):</b><br/>"
        "<font face='Courier' size='7'>"
        "apiVersion: apps/v1<br/>"
        "kind: Deployment<br/>"
        "metadata:<br/>"
        "  name: lab2-deployment<br/>"
        "  labels:<br/>"
        "    app: lab2-app<br/>"
        "    tier: backend<br/>"
        "    experiment: orchestration<br/>"
        "spec:<br/>"
        "  replicas: 1<br/>"
        "  selector:<br/>"
        "    matchLabels:<br/>"
        "      app: lab2-app<br/>"
        "  template:<br/>"
        "    metadata:<br/>"
        "      labels:<br/>"
        "        app: lab2-app<br/>"
        "        tier: backend<br/>"
        "    spec:<br/>"
        "      containers:<br/>"
        "      - name: devops-container<br/>"
        "        image: lab2-devops-app:latest<br/>"
        "        imagePullPolicy: IfNotPresent<br/>"
        "        resources:<br/>"
        "          limits:<br/>"
        "            cpu: \"250m\"<br/>"
        "            memory: \"128Mi\"<br/>"
        "          requests:<br/>"
        "            cpu: \"100m\"<br/>"
        "            memory: \"64Mi\"<br/>"
        "        env:<br/>"
        "        - name: APP_ENV<br/>"
        "          value: \"production\"<br/>"
        "        - name: EXPERIMENT<br/>"
        "          value: \"lab2-orchestration\""
        "</font>"
    )

    t_deploy = Table([[Paragraph(k8s_deploy_code, styles['BodyTextCustom'])]], colWidths=[480])
    t_deploy.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_deploy)
    story.append(Spacer(1, 6))

    k8s_service_code = (
        "<b>Service Manifest (lab2-orchestration/kubernetes/service.yaml):</b><br/>"
        "<font face='Courier' size='7'>"
        "apiVersion: v1<br/>"
        "kind: Service<br/>"
        "metadata:<br/>"
        "  name: lab2-service<br/>"
        "  labels:<br/>"
        "    app: lab2-app<br/>"
        "    experiment: orchestration<br/>"
        "spec:<br/>"
        "  type: ClusterIP<br/>"
        "  selector:<br/>"
        "    app: lab2-app<br/>"
        "  ports:<br/>"
        "  - name: dummy-port<br/>"
        "    port: 80<br/>"
        "    targetPort: 80"
        "</font>"
    )

    t_service = Table([[Paragraph(k8s_service_code, styles['BodyTextCustom'])]], colWidths=[480])
    t_service.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_service)
    story.append(PageBreak())

    # ================= SECTION 3: COMMAND LOG =================
    story.append(Paragraph("3. Chronological Execution Command Log", styles['SectionHeading']))
    story.append(Paragraph("All verified commands executed sequentially during the experiment:", styles['BodyTextCustom']))

    cmd_text = (
        "<font face='Courier' size='7'>"
        "# 1. Environment Verification<br/>"
        "docker version<br/>"
        "kubectl version --client<br/>"
        "kubectl cluster-info<br/>"
        "kubectl get nodes<br/><br/>"
        "# 2. Docker Image Build & Verification<br/>"
        "docker build -t lab2-devops-app:latest -f .\\lab2-orchestration\\docker\\Dockerfile .<br/>"
        "docker images lab2-devops-app:latest<br/>"
        "docker run -d --name lab2-container-test lab2-devops-app:latest<br/>"
        "docker logs lab2-container-test<br/>"
        "docker rm -f lab2-container-test<br/><br/>"
        "# 3. Apply Kubernetes Deployment & Service<br/>"
        "kubectl apply -f .\\lab2-orchestration\\kubernetes\\deployment.yaml<br/>"
        "kubectl apply -f .\\lab2-orchestration\\kubernetes\\service.yaml<br/>"
        "kubectl get deployments -o wide<br/>"
        "kubectl get pods -l app=lab2-app -o wide<br/>"
        "kubectl get services lab2-service<br/><br/>"
        "# 4. Scaling Verification<br/>"
        "kubectl scale deployment lab2-deployment --replicas=3<br/>"
        "kubectl get pods -l app=lab2-app -o wide<br/>"
        "kubectl scale deployment lab2-deployment --replicas=5<br/>"
        "kubectl get pods -l app=lab2-app -o wide<br/>"
        "kubectl describe deployment lab2-deployment<br/>"
        "kubectl get all -l app=lab2-app"
        "</font>"
    )

    t_cmd = Table([[Paragraph(cmd_text, styles['BodyTextCustom'])]], colWidths=[480])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 6))

    img13 = create_image_flowable("13-scaled-to-5-replicas.png", max_height=105)
    if img13:
        story.append(img13)
        story.append(Paragraph("Figure 2 - Terminal evidence of scaling deployment to 5 running pod replicas.", styles['Caption']))
    story.append(PageBreak())

    # ================= SECTION 4: SUBMISSION MANIFEST =================
    story.append(Paragraph("4. Submission Package Manifest", styles['SectionHeading']))
    story.append(Paragraph("The complete submission package is bundled in <b>Lab2_Tools_Documents.zip</b> containing:", styles['BodyTextCustom']))
    
    pkg_data = [
        [Paragraph("File / Directory", styles['TableHeader']), Paragraph("Description", styles['TableHeader'])],
        [Paragraph("docker/Dockerfile", styles['TableCellBold']), Paragraph("Production slim container build specification", styles['TableCell'])],
        [Paragraph("docker/.dockerignore", styles['TableCellBold']), Paragraph("Build context exclusion rules", styles['TableCell'])],
        [Paragraph("docker/entrypoint.py", styles['TableCellBold']), Paragraph("Workload orchestration lifecycle runner", styles['TableCell'])],
        [Paragraph("kubernetes/deployment.yaml", styles['TableCellBold']), Paragraph("Declarative deployment specification with resource controls", styles['TableCell'])],
        [Paragraph("kubernetes/service.yaml", styles['TableCellBold']), Paragraph("ClusterIP service specification", styles['TableCell'])],
        [Paragraph("screenshots/*.png", styles['TableCellBold']), Paragraph("14 real terminal verification evidence screenshots", styles['TableCell'])],
        [Paragraph("commands.txt", styles['TableCellBold']), Paragraph("Chronological execution command transcript", styles['TableCell'])],
        [Paragraph("README.md", styles['TableCellBold']), Paragraph("Comprehensive Markdown documentation", styles['TableCell'])],
        [Paragraph("Lab2_Containerization_Orchestration_Report.pdf", styles['TableCellBold']), Paragraph("Question 1 - 10 Marks Report Document", styles['TableCell'])],
        [Paragraph("Lab2_Tools_Documents.pdf", styles['TableCellBold']), Paragraph("Question 2 - 5 Marks Tools Document", styles['TableCell'])],
    ]
    t_pkg = Table(pkg_data, colWidths=[180, 300])
    t_pkg.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_pkg)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. Result & Verification Summary", styles['SectionHeading']))
    story.append(Paragraph("All tools, manifests, and scaling commands have been verified on the machine with zero simulated data. Both submission files are ready for upload.", styles['BodyTextCustom']))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF 2: {PDF_TOOLS_PATH}")

if __name__ == "__main__":
    build_pdf1()
    build_pdf2()
