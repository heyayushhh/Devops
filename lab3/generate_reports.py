"""
Generate professional, high-quality PDF reports for Lab 3 using ReportLab.
"""
import os
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable

REPORTS_DIR = r"C:\Users\hp\Desktop\New folder\Devops\lab3\reports"
SCREENSHOTS_DIR = r"C:\Users\hp\Desktop\New folder\Devops\lab3\screenshots"
os.makedirs(REPORTS_DIR, exist_ok=True)


def build_pdf_ansible(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1E40AF'),
        spaceBefore=14,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1F2937'),
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#111827'),
        backColor=colors.HexColor('#F3F4F6'),
        borderPadding=6,
        spaceAfter=6
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Lab 3: Question 1 — Ansible Infrastructure & Configuration Automation", title_style))
    story.append(Paragraph("<b>Course:</b> DevOps Engineering &nbsp;|&nbsp; <b>Marks:</b> 5 Marks &nbsp;|&nbsp; <b>Evaluation:</b> Automated Playbook & Target Nodes", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=12))

    # 1. Objective
    story.append(Paragraph("1. Objective", h1_style))
    story.append(Paragraph(
        "The objective of this assignment is to configure infrastructure and automate application configuration using Ansible by writing modular playbooks and executing them against containerized target nodes. The implementation verifies declarative state management, role-based encapsulation, template-driven per-node configuration, and strict execution idempotency.",
        body_style
    ))

    # 2. Environment
    story.append(Paragraph("2. Environment & Tooling", h1_style))
    env_data = [
        ["Component", "Specification / Version", "Role in Architecture"],
        ["Operating System", "Microsoft Windows (Host)", "Host executing Docker Engine daemon"],
        ["Docker Engine", "v29.6.1 / API v1.55", "Container runtime hosting controller & nodes"],
        ["Ansible Core", "ansible-core v2.21.4 (Python 3.12.14)", "Automation engine inside controller container"],
        ["Ansible Collection", "community.docker v5.3.0", "Docker Engine API socket connection plugin"],
        ["Target Runtime", "python:3.12-slim (Debian Linux)", "Lightweight Linux nodes on lab3-net bridge"]
    ]
    t = Table(env_data, colWidths=[120, 180, 230])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # 3. Architecture & 4. Controller
    story.append(Paragraph("3. Architecture & Ansible Controller", h1_style))
    story.append(Paragraph(
        "Due to Windows lack of native POSIX system calls required by ansible-core, the controller runs as an ephemeral container (<code>lab3-ansible-controller:latest</code>). It mounts the host's Docker socket (<code>/var/run/docker.sock</code>), allowing the <code>community.docker.docker</code> connection plugin to communicate directly with target containers without requiring SSH daemons or open network ports.",
        body_style
    ))

    # 5. Target Nodes & 6. Inventory
    story.append(Paragraph("4. Target Nodes & Inventory Configuration", h1_style))
    story.append(Paragraph(
        "Two dedicated target nodes (<code>lab3-ansible-node1</code> and <code>lab3-ansible-node2</code>) run on the isolated bridge network <code>lab3-net</code>. Inventory variables customize port assignments and deployment tiers per host:",
        body_style
    ))
    story.append(Paragraph(
        "<code>[lab3_targets]<br/>"
        "lab3-ansible-node1 ansible_connection=community.docker.docker app_port=8081 app_env=staging<br/>"
        "lab3-ansible-node2 ansible_connection=community.docker.docker app_port=8082 app_env=production</code>",
        code_style
    ))

    # 7. Playbook & Role
    story.append(Paragraph("5. Playbook & Role-Based Application Configuration", h1_style))
    story.append(Paragraph(
        "The master playbook <code>site.yml</code> executes the <code>app_config</code> role containing the following modular components: "
        "<br/>• <b>Group & User creation:</b> Creates <code>lab3app</code> system service user and group."
        "<br/>• <b>Directory Hierarchy:</b> Creates <code>/opt/lab3app/bin</code>, <code>/etc/lab3app</code>, <code>/var/log/lab3app</code>, <code>/var/run/lab3app</code>."
        "<br/>• <b>Jinja2 Templating:</b> Generates customized <code>/etc/lab3app/app.conf</code> based on inventory variables."
        "<br/>• <b>Code Deployment:</b> Deploys <code>app.py</code>, <code>ctl.sh</code>, and <code>healthcheck.py</code>."
        "<br/>• <b>Service Daemon:</b> Starts the background HTTP microservice and verifies readiness with automated health checks.",
        body_style
    ))

    # 8. Execution & Idempotency
    story.append(Paragraph("6. Execution & Idempotency Analysis", h1_style))
    story.append(Paragraph(
        "• <b>Initial Execution:</b> Applied 7 state modifications (user, group, directories, template, files, service startup, handler trigger). Result: <code>ok=10 changed=7 unreachable=0 failed=0</code>."
        "<br/>• <b>Second Execution:</b> Executed to verify declarative idempotency. All 9 tasks verified existing state without re-triggering changes. Result: <code>ok=9 changed=0 unreachable=0 failed=0</code>.",
        body_style
    ))

    # 9. Screenshots
    story.append(PageBreak())
    story.append(Paragraph("7. Verified Execution Evidence & Screenshots", h1_style))

    screenshots = [
        ("01_environment.png", "Figure 1: Docker Environment & Container Verification"),
        ("02_ansible_inventory.png", "Figure 2: Inventory Configuration & Ad-Hoc Connectivity Ping"),
        ("03_ansible_playbook.png", "Figure 3: Ansible Master Playbook & Role Structure"),
        ("04_target_nodes.png", "Figure 4: Target Node Inspection & Python Runtime Verification"),
        ("05_ansible_syntax_check.png", "Figure 5: Playbook Syntax Check Validation"),
        ("06_ansible_execution.png", "Figure 6: Initial Playbook Execution (7 State Changes)"),
        ("07_ansible_success.png", "Figure 7: Second Playbook Run Demonstrating 100% Idempotency (changed=0)"),
        ("08_target_verification.png", "Figure 8: Direct Node Verification (Config, Process Status, Healthcheck)")
    ]

    for img_name, caption in screenshots:
        img_path = os.path.join(SCREENSHOTS_DIR, img_name)
        if os.path.exists(img_path):
            story.append(KeepTogether([
                Paragraph(f"<b>{caption}</b>", h2_style),
                Image(img_path, width=500, height=190),
                Spacer(1, 8)
            ]))

    # 10. Observations & Conclusion
    story.append(Paragraph("8. Observations & Key Takeaways", h1_style))
    story.append(Paragraph(
        "1. <b>Agentless Container Management:</b> Utilizing <code>community.docker.docker</code> eliminated the overhead of installing SSH daemons in minimal containers while retaining full Ansible task orchestration.<br/>"
        "2. <b>Dynamic Environment Provisioning:</b> Jinja2 templating enabled clean separation of staging (port 8081) and production (port 8082) environments.<br/>"
        "3. <b>Guaranteed Idempotency:</b> Successive runs produced zero modifications, verifying enterprise-grade declarative automation.",
        body_style
    ))

    story.append(Paragraph("9. Conclusion", h1_style))
    story.append(Paragraph(
        "Lab 3 Question 1 requirements were fully satisfied with genuine execution, zero failures, complete state verification, and verifiable proof of idempotency.",
        body_style
    ))

    doc.build(story)
    print(f"Built {filename}")


def build_pdf_terraform(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#065F46'),
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#047857'),
        spaceBefore=14,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1F2937'),
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#111827'),
        backColor=colors.HexColor('#F3F4F6'),
        borderPadding=6,
        spaceAfter=6
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Lab 3: Question 2 — Terraform Scalable Infrastructure as Code (IaC)", title_style))
    story.append(Paragraph("<b>Course:</b> DevOps Engineering &nbsp;|&nbsp; <b>Marks:</b> 5 Marks &nbsp;|&nbsp; <b>Evaluation:</b> IaC Lifecycle & Dynamic Scaling (2 → 4)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#059669'), spaceAfter=12))

    # 1. Objective
    story.append(Paragraph("1. Objective", h1_style))
    story.append(Paragraph(
        "The objective of this assignment is to provision scalable infrastructure using Terraform (Infrastructure as Code): write modular configuration files, initialize provider plugins, plan execution changes, apply real infrastructure resources, and demonstrate dynamic scaling from 2 to 4 application instances.",
        body_style
    ))

    # 2. Infrastructure Architecture
    story.append(Paragraph("2. Infrastructure Architecture & Provider Setup", h1_style))
    env_data = [
        ["Resource / Component", "Configuration", "Description"],
        ["IaC Engine", "Terraform v1.13.3 (windows_amd64)", "Declarative state management engine"],
        ["Provider", "kreuzwerker/docker v3.0.2", "Docker Engine API connector via Windows named pipe"],
        ["Bridge Network", "docker_network.app_network (lab3-tf-net)", "Isolated bridge network for provisioned instances"],
        ["Base Image", "docker_image.app_image (python:3.12-slim)", "Locally cached runtime image"],
        ["Scalable Service", "docker_container.app_service[count]", "Scalable microservices with dynamic port mapping"]
    ]
    t = Table(env_data, colWidths=[130, 180, 220])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#065F46')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # 3. Terraform Configuration
    story.append(Paragraph("3. Terraform Configuration Structure", h1_style))
    story.append(Paragraph(
        "• <code>main.tf</code>: Declares the Docker provider, custom bridge network (<code>lab3-tf-net</code>), image reference, and the container resource scaled via <code>count = var.replica_count</code>.<br/>"
        "• <code>variables.tf</code>: Defines input parameters (<code>docker_host</code>, <code>replica_count</code>, <code>base_host_port</code>) with validation constraints ensuring replica count is within [1, 10].<br/>"
        "• <code>outputs.tf</code>: Exports network ID, active replica count, and instance IP/port metadata.<br/>"
        "• <code>terraform.tfvars</code>: Provides explicit variable assignments.",
        body_style
    ))

    # 4. Lifecycle Execution & Scaling
    story.append(Paragraph("4. Lifecycle Execution & Dynamic Scaling (2 → 4)", h1_style))
    story.append(Paragraph(
        "1. <b>Initialization (<code>terraform init</code>):</b> Downloaded and cached <code>kreuzwerker/docker v3.0.2</code> and generated <code>.terraform.lock.hcl</code>.<br/>"
        "2. <b>Validation (<code>terraform validate</code>):</b> Verified syntax and argument types with 100% compliance.<br/>"
        "3. <b>Initial Provisioning (2 Replicas):</b> Planned and applied 4 resources: 1 network, 1 image, and 2 container instances (<code>lab3-tf-app-1</code> on port 8181, <code>lab3-tf-app-2</code> on port 8182).<br/>"
        "4. <b>Dynamic Scaling (4 Replicas):</b> Updated <code>replica_count = 4</code> in <code>terraform.tfvars</code>. <code>terraform plan</code> calculated the delta, and <code>terraform apply</code> expanded infrastructure to 4 running replicas (ports 8181, 8182, 8183, 8184).",
        body_style
    ))

    # 5. Screenshots
    story.append(PageBreak())
    story.append(Paragraph("5. Verified Execution Evidence & Screenshots", h1_style))

    screenshots = [
        ("09_terraform_files.png", "Figure 9: Terraform Configuration Files (main.tf, variables, outputs, tfvars)"),
        ("10_terraform_init.png", "Figure 10: Terraform Initialization & Docker Provider Installation"),
        ("11_terraform_validate.png", "Figure 11: Terraform Configuration Validation"),
        ("12_terraform_plan.png", "Figure 12: Initial Execution Plan (4 Resources to Add)"),
        ("13_terraform_apply.png", "Figure 13: Initial Apply (2 Replicas Provisioned)"),
        ("14_terraform_resources.png", "Figure 14: Verification of 2 Active Provisioned Containers & Network"),
        ("15_terraform_scaling_plan.png", "Figure 15: Scaling Execution Plan (replica_count 2 → 4)"),
        ("16_terraform_scaling_apply.png", "Figure 16: Scaling Apply Execution (4 Active Replicas)"),
        ("17_terraform_scaled_resources.png", "Figure 17: Verification of 4 Active Scaled Replicas & HTTP 200 Responses")
    ]

    for img_name, caption in screenshots:
        img_path = os.path.join(SCREENSHOTS_DIR, img_name)
        if os.path.exists(img_path):
            story.append(KeepTogether([
                Paragraph(f"<b>{caption}</b>", h2_style),
                Image(img_path, width=500, height=190),
                Spacer(1, 8)
            ]))

    # 6. Observations & Conclusion
    story.append(Paragraph("6. Observations & Key Takeaways", h1_style))
    story.append(Paragraph(
        "1. <b>Declarative Resource Management:</b> Changing a single variable (<code>replica_count</code>) allowed Terraform to calculate exact resource differences and seamlessly scale infrastructure.<br/>"
        "2. <b>Dynamic Port & IP Allocation:</b> Using <code>count.index</code> cleanly separated host port bindings (8181 to 8184) without conflict.<br/>"
        "3. <b>Automated Validation:</b> Health endpoints across all 4 container instances responded with HTTP 200 OK immediately after deployment.",
        body_style
    ))

    story.append(Paragraph("7. Conclusion", h1_style))
    story.append(Paragraph(
        "Lab 3 Question 2 requirements were completely fulfilled using genuine Terraform infrastructure provisioning, clean provider configuration, state tracking, and verified 2 → 4 dynamic scaling.",
        body_style
    ))

    doc.build(story)
    print(f"Built {filename}")


def build_pdf_combined(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontSize=14,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story = []

    story.append(Paragraph("Lab 3: Comprehensive Technical Documentation & Evidence Package", title_style))
    story.append(Paragraph("<b>DevOps Lab 3:</b> Ansible Configuration Automation & Terraform Infrastructure as Code (IaC)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=12))

    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "This consolidated document contains the complete technical documentation, source configuration files, terminal commands, execution verification, and visual evidence for both Lab 3 tasks: Question 1 (Ansible Automation) and Question 2 (Terraform IaC).",
        body_style
    ))

    # Summary table
    summary_data = [
        ["Evaluation Section", "Implemented Tooling", "Execution Result", "Idempotency / Scaling"],
        ["Q1: Configuration Automation", "Ansible Core 2.21.4 + community.docker", "10/10 tasks OK, 7 changed", "100% Idempotent (changed=0)"],
        ["Q2: Infrastructure as Code", "Terraform v1.13.3 + kreuzwerker/docker", "4 resources added, state tracked", "Scaled 2 → 4 Replicas (HTTP 200)"]
    ]
    t = Table(summary_data, colWidths=[120, 140, 130, 140])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Complete Evidence Screenshots", h1_style))

    all_screenshots = [
        ("01_environment.png", "Figure 1: Docker Host Environment & Target Node Status"),
        ("02_ansible_inventory.png", "Figure 2: Ansible Inventory & Ad-Hoc Target Node Ping"),
        ("03_ansible_playbook.png", "Figure 3: Ansible Master Playbook & Role Directory Structure"),
        ("04_target_nodes.png", "Figure 4: Target Node Inspection & Python 3.12 Runtime"),
        ("05_ansible_syntax_check.png", "Figure 5: Ansible Playbook Syntax Check"),
        ("06_ansible_execution.png", "Figure 6: Initial Playbook Execution (7 Changes Applied)"),
        ("07_ansible_success.png", "Figure 7: Second Playbook Execution (100% Idempotency, changed=0)"),
        ("08_target_verification.png", "Figure 8: Direct Node Verification (Config, Process Status, Healthcheck)"),
        ("09_terraform_files.png", "Figure 9: Terraform IaC Configuration Files"),
        ("10_terraform_init.png", "Figure 10: Terraform Initialization & Docker Provider Setup"),
        ("11_terraform_validate.png", "Figure 11: Terraform Configuration Validation"),
        ("12_terraform_plan.png", "Figure 12: Initial Execution Plan (2 Replicas)"),
        ("13_terraform_apply.png", "Figure 13: Initial Apply (2 Replicas Provisioned)"),
        ("14_terraform_resources.png", "Figure 14: Verification of 2 Active Provisioned Containers & Network"),
        ("15_terraform_scaling_plan.png", "Figure 15: Terraform Dynamic Scaling Plan (2 → 4 Replicas)"),
        ("16_terraform_scaling_apply.png", "Figure 16: Scaling Apply Execution (4 Active Replicas)"),
        ("17_terraform_scaled_resources.png", "Figure 17: Verification of 4 Active Scaled Replicas & HTTP 200 Responses")
    ]

    for img_name, caption in all_screenshots:
        img_path = os.path.join(SCREENSHOTS_DIR, img_name)
        if os.path.exists(img_path):
            story.append(KeepTogether([
                Paragraph(f"<b>{caption}</b>", h2_style),
                Image(img_path, width=490, height=180),
                Spacer(1, 6)
            ]))

    doc.build(story)
    print(f"Built {filename}")


def create_zip_package():
    zip_path = r"C:\Users\hp\Desktop\New folder\Devops\lab3\Lab3_Tools_Documents.zip"
    lab3_dir = r"C:\Users\hp\Desktop\New folder\Devops\lab3"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(lab3_dir):
            for file in files:
                if file.endswith('.zip') or file.endswith('.terraform') or '.terraform' in root:
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, lab3_dir)
                zipf.write(full_path, arcname=os.path.join("lab3", rel_path))
    print(f"Created {zip_path}")


if __name__ == "__main__":
    build_pdf_ansible(os.path.join(REPORTS_DIR, "Lab3_Ansible_Infrastructure_Report.pdf"))
    build_pdf_terraform(os.path.join(REPORTS_DIR, "Lab3_Terraform_Infrastructure_Report.pdf"))
    build_pdf_combined(os.path.join(REPORTS_DIR, "Lab3_Tools_Documents.pdf"))
    create_zip_package()
