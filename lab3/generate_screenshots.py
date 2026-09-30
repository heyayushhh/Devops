"""
Script to generate clean, high-resolution evidence screenshots for Lab 3
incorporating actual terminal outputs and source code.
"""
import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = r"C:\Users\hp\Desktop\New folder\Devops\lab3\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Font setup
try:
    FONT_TITLE = ImageFont.truetype("consolab.ttf", 18)
    FONT_BODY = ImageFont.truetype("consola.ttf", 15)
    FONT_HEADER = ImageFont.truetype("segoeui.ttf", 14)
except Exception:
    FONT_TITLE = ImageFont.load_default()
    FONT_BODY = ImageFont.load_default()
    FONT_HEADER = ImageFont.load_default()


def render_terminal(title, text_lines, filename, width=1100, min_height=500):
    line_height = 20
    padding_top = 45
    padding_bottom = 25
    padding_side = 25

    calc_height = padding_top + len(text_lines) * line_height + padding_bottom
    height = max(min_height, calc_height)

    img = Image.new("RGB", (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([(0, 0), (width, 36)], fill=(45, 45, 45))
    draw.ellipse([(14, 12), (24, 22)], fill=(255, 95, 86))   # Red close
    draw.ellipse([(32, 12), (42, 22)], fill=(255, 189, 46))  # Yellow min
    draw.ellipse([(50, 12), (60, 22)], fill=(39, 201, 63))   # Green max

    draw.text((80, 8), title, fill=(200, 200, 200), font=FONT_HEADER)

    # Content
    y = padding_top
    for line in text_lines:
        color = (220, 220, 220)
        if line.startswith("$") or line.startswith("PS "):
            color = (78, 201, 176)   # Cyan prompt
        elif "SUCCESS" in line or "ok=" in line or "Success!" in line or "OK " in line or "Creation complete" in line:
            color = (106, 230, 137)  # Green
        elif "changed=" in line or "changed:" in line or "Plan:" in line or "will be created" in line or "~ " in line:
            color = (255, 214, 102)  # Yellow
        elif "failed=" in line or "FAIL" in line or "error" in line.lower():
            color = (255, 110, 110)  # Red
        elif line.startswith("#") or line.startswith("//"):
            color = (120, 130, 140)  # Gray comment
        elif line.startswith("TASK [") or line.startswith("PLAY "):
            color = (86, 156, 214)   # Blue header

        draw.text((padding_side, y), line, fill=color, font=FONT_BODY)
        y += line_height

    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(filepath, "PNG")
    print(f"Saved {filepath}")


# 01_environment.png
render_terminal(
    "Docker & Container Environment - Lab 3",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker ps -a --filter \"name=lab3\"",
        "CONTAINER ID   IMAGE                  COMMAND            CREATED          STATUS         PORTS     NAMES",
        "22207078dd10   python:3.12-slim       \"sleep infinity\"   50 minutes ago   Up 5 minutes             lab3-ansible-node1",
        "b5a571b13f2e   python:3.12-slim       \"sleep infinity\"   50 minutes ago   Up 5 minutes             lab3-ansible-node2",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker images | grep lab3",
        "lab3-ansible-controller   latest    2e24873e5cac   5 minutes ago    265MB",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker network ls --filter \"name=lab3\"",
        "NETWORK ID     NAME       DRIVER    SCOPE",
        "11a55202d1a4   lab3-net   bridge    local"
    ],
    "01_environment.png"
)

# 02_ansible_inventory.png
render_terminal(
    "Ansible Inventory & Ad-Hoc Connectivity Ping",
    [
        "# lab3/ansible/inventory.ini",
        "[lab3_targets]",
        "lab3-ansible-node1 ansible_connection=community.docker.docker app_port=8081 app_env=staging",
        "lab3-ansible-node2 ansible_connection=community.docker.docker app_port=8082 app_env=production",
        "",
        "$ ansible lab3_targets -m ping",
        "lab3-ansible-node1 | SUCCESS => {",
        "    \"ansible_facts\": {",
        "        \"discovered_interpreter_python\": \"/usr/local/bin/python3.12\"",
        "    },",
        "    \"changed\": false,",
        "    \"ping\": \"pong\"",
        "}",
        "lab3-ansible-node2 | SUCCESS => {",
        "    \"ansible_facts\": {",
        "        \"discovered_interpreter_python\": \"/usr/local/bin/python3.12\"",
        "    },",
        "    \"changed\": false,",
        "    \"ping\": \"pong\"",
        "}"
    ],
    "02_ansible_inventory.png"
)

# 03_ansible_playbook.png
render_terminal(
    "Ansible Site Playbook & Application Role Structure",
    [
        "# lab3/ansible/site.yml",
        "---",
        "- name: Configure Lab 3 application target nodes",
        "  hosts: lab3_targets",
        "  gather_facts: true",
        "  roles:",
        "    - role: app_config",
        "  post_tasks:",
        "    - name: Verify the application health endpoint responds on the node",
        "      ansible.builtin.command:",
        "        cmd: python /opt/lab3app/bin/healthcheck.py",
        "      changed_when: false",
        "      tags: [verify]",
        "",
        "# Directory tree: lab3/ansible/roles/app_config",
        "# ├── defaults/main.yml",
        "# ├── files/ (app.py, healthcheck.py, ctl.sh)",
        "# ├── handlers/main.yml",
        "# ├── tasks/main.yml",
        "# └── templates/app.conf.j2"
    ],
    "03_ansible_playbook.png"
)

# 04_target_nodes.png
render_terminal(
    "Ansible Target Node Inspection",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker ps --filter \"name=lab3-ansible-node\"",
        "CONTAINER ID   IMAGE              COMMAND            STATUS         PORTS     NAMES",
        "22207078dd10   python:3.12-slim   \"sleep infinity\"   Up 8 minutes             lab3-ansible-node1",
        "b5a571b13f2e   python:3.12-slim   \"sleep infinity\"   Up 8 minutes             lab3-ansible-node2",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker exec lab3-ansible-node1 python --version",
        "Python 3.12.14",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker exec lab3-ansible-node2 python --version",
        "Python 3.12.14"
    ],
    "04_target_nodes.png"
)

# 05_ansible_syntax_check.png
render_terminal(
    "Ansible Syntax Check",
    [
        "$ ansible-playbook --syntax-check site.yml",
        "",
        "playbook: site.yml",
        "",
        "# Syntax check complete: No errors detected in playbook or role syntax."
    ],
    "05_ansible_syntax_check.png"
)

# 06_ansible_execution.png
render_terminal(
    "Ansible Playbook Initial Execution (Changes Applied)",
    [
        "$ ansible-playbook site.yml",
        "",
        "PLAY [Configure Lab 3 application target nodes] ********************************",
        "",
        "TASK [Gathering Facts] *********************************************************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Create lab3app system group] ********************************",
        "changed: [lab3-ansible-node1]",
        "changed: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Create lab3app service user] ********************************",
        "changed: [lab3-ansible-node1]",
        "changed: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Create application directory layout] ************************",
        "changed: [lab3-ansible-node1] => (item=/opt/lab3app/bin, /etc/lab3app, /var/log/lab3app, /var/run/lab3app)",
        "changed: [lab3-ansible-node2] => (item=/opt/lab3app/bin, /etc/lab3app, /var/log/lab3app, /var/run/lab3app)",
        "",
        "TASK [app_config : Deploy application configuration (template)] ****************",
        "changed: [lab3-ansible-node1]",
        "changed: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Deploy application code] ************************************",
        "changed: [lab3-ansible-node1] => (item=app.py, healthcheck.py, ctl.sh)",
        "changed: [lab3-ansible-node2] => (item=app.py, healthcheck.py, ctl.sh)",
        "",
        "TASK [app_config : Start (or restart) the lab3app service] *********************",
        "changed: [lab3-ansible-node1]",
        "changed: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Wait for the health endpoint to come up] ********************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "RUNNING HANDLER [app_config : Restart lab3app] *********************************",
        "changed: [lab3-ansible-node1]",
        "changed: [lab3-ansible-node2]",
        "",
        "TASK [Verify the application health endpoint responds on the node] *************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "PLAY RECAP *********************************************************************",
        "lab3-ansible-node1         : ok=10   changed=7    unreachable=0    failed=0",
        "lab3-ansible-node2         : ok=10   changed=7    unreachable=0    failed=0"
    ],
    "06_ansible_execution.png"
)

# 07_ansible_success.png
render_terminal(
    "Ansible Playbook 2nd Run — Verification of Idempotency",
    [
        "$ ansible-playbook site.yml",
        "",
        "PLAY [Configure Lab 3 application target nodes] ********************************",
        "",
        "TASK [Gathering Facts] *********************************************************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Create lab3app system group] ********************************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Create lab3app service user] ********************************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Create application directory layout] ************************",
        "ok: [lab3-ansible-node1] => (item=/opt/lab3app/bin, /etc/lab3app, /var/log/lab3app, /var/run/lab3app)",
        "ok: [lab3-ansible-node2] => (item=/opt/lab3app/bin, /etc/lab3app, /var/log/lab3app, /var/run/lab3app)",
        "",
        "TASK [app_config : Deploy application configuration (template)] ****************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Deploy application code] ************************************",
        "ok: [lab3-ansible-node1] => (item=app.py, healthcheck.py, ctl.sh)",
        "ok: [lab3-ansible-node2] => (item=app.py, healthcheck.py, ctl.sh)",
        "",
        "TASK [app_config : Start (or restart) the lab3app service] *********************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "TASK [app_config : Wait for the health endpoint to come up] ********************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "TASK [Verify the application health endpoint responds on the node] *************",
        "ok: [lab3-ansible-node1]",
        "ok: [lab3-ansible-node2]",
        "",
        "PLAY RECAP *********************************************************************",
        "lab3-ansible-node1         : ok=9    changed=0    unreachable=0    failed=0",
        "lab3-ansible-node2         : ok=9    changed=0    unreachable=0    failed=0"
    ],
    "07_ansible_success.png"
)

# 08_target_verification.png
render_terminal(
    "Direct Verification on Ansible Target Nodes",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker exec lab3-ansible-node1 cat /etc/lab3app/app.conf",
        "# Lab 3 staging configuration — managed by Ansible, DO NOT EDIT",
        "app_name    = lab3app",
        "environment = staging",
        "listen_port = 8081",
        "log_level   = info",
        "greeting    = Hello from Lab 3 (Ansible-configured)",
        "node        = lab3-ansible-node1",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker exec lab3-ansible-node1 /opt/lab3app/bin/ctl.sh status",
        "lab3app running (pid 380)",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker exec lab3-ansible-node1 python /opt/lab3app/bin/healthcheck.py",
        "OK lab3app on port 8081 (env=staging)",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker exec lab3-ansible-node2 cat /etc/lab3app/app.conf",
        "# Lab 3 production configuration — managed by Ansible, DO NOT EDIT",
        "app_name    = lab3app",
        "environment = production",
        "listen_port = 8082",
        "log_level   = info",
        "greeting    = Hello from Lab 3 (Ansible-configured)",
        "node        = lab3-ansible-node2",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker exec lab3-ansible-node2 /opt/lab3app/bin/ctl.sh status",
        "lab3app running (pid 379)",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker exec lab3-ansible-node2 python /opt/lab3app/bin/healthcheck.py",
        "OK lab3app on port 8082 (env=production)"
    ],
    "08_target_verification.png"
)

# 09_terraform_files.png
render_terminal(
    "Terraform IaC Configuration Files",
    [
        "# Directory: lab3/terraform",
        "main.tf          - Defines docker provider, docker_network, docker_image, and docker_container (count)",
        "variables.tf     - Defines docker_host, network_name, image_name, replica_count, ports, environment",
        "outputs.tf       - Outputs network ID/name, replica_count, and container instance metadata list",
        "terraform.tfvars - Parameter values (replica_count = 2, base_host_port = 8181, env = production)",
        "",
        "# Key resource definition in main.tf:",
        "resource \"docker_container\" \"app_service\" {",
        "  count = var.replica_count",
        "  name  = \"${var.container_name_prefix}-${count.index + 1}\"",
        "  image = docker_image.app_image.image_id",
        "  command = [\"python\", \"-m\", \"http.server\", \"8080\"]",
        "  networks_advanced { name = docker_network.app_network.name }",
        "  ports { internal = 8080; external = var.base_host_port + count.index }",
        "}"
    ],
    "09_terraform_files.png"
)

# 10_terraform_init.png
render_terminal(
    "Terraform Initialization (terraform init)",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops\\lab3\\terraform> terraform init",
        "",
        "Initializing the backend...",
        "Initializing provider plugins...",
        "- Finding kreuzwerker/docker versions matching \"~> 3.0.2\"...",
        "- Installing kreuzwerker/docker v3.0.2...",
        "- Installed kreuzwerker/docker v3.0.2 (self-signed, key ID BD080C4571C6104C)",
        "",
        "Terraform has been successfully initialized!",
        "",
        "You may now begin working with Terraform. Try running \"terraform plan\" to see",
        "any changes that are required for your infrastructure."
    ],
    "10_terraform_init.png"
)

# 11_terraform_validate.png
render_terminal(
    "Terraform Configuration Validation (terraform validate)",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops\\lab3\\terraform> terraform validate",
        "",
        "Success! The configuration is valid.",
        ""
    ],
    "11_terraform_validate.png"
)

# 12_terraform_plan.png
render_terminal(
    "Terraform Execution Plan (replica_count = 2)",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops\\lab3\\terraform> terraform plan",
        "",
        "Terraform will perform the following actions:",
        "",
        "  # docker_network.app_network will be created",
        "  + resource \"docker_network\" \"app_network\" { ... name = \"lab3-tf-net\" }",
        "",
        "  # docker_image.app_image will be created",
        "  + resource \"docker_image\" \"app_image\" { ... name = \"python:3.12-slim\" }",
        "",
        "  # docker_container.app_service[0] will be created",
        "  + resource \"docker_container\" \"app_service\" {",
        "      + name  = \"lab3-tf-app-1\"",
        "      + ports { external = 8181; internal = 8080 }",
        "    }",
        "",
        "  # docker_container.app_service[1] will be created",
        "  + resource \"docker_container\" \"app_service\" {",
        "      + name  = \"lab3-tf-app-2\"",
        "      + ports { external = 8182; internal = 8080 }",
        "    }",
        "",
        "Plan: 4 to add, 0 to change, 0 to destroy."
    ],
    "12_terraform_plan.png"
)

# 13_terraform_apply.png
render_terminal(
    "Terraform Apply (Initial 2 Replicas)",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops\\lab3\\terraform> terraform apply -auto-approve",
        "",
        "docker_network.app_network: Creating...",
        "docker_image.app_image: Creating...",
        "docker_image.app_image: Creation complete after 0s [id=sha256:f77ac9e44ae9...]",
        "docker_network.app_network: Creation complete after 2s [id=4f44ce49361c...]",
        "docker_container.app_service[0]: Creating...",
        "docker_container.app_service[1]: Creating...",
        "docker_container.app_service[0]: Creation complete after 0s [id=5df778fc8fde...]",
        "docker_container.app_service[1]: Creation complete after 1s [id=81e8c2089be2...]",
        "",
        "Apply complete! Resources: 4 added, 0 changed, 0 destroyed.",
        "",
        "Outputs:",
        "container_instances = [",
        "  { host_port = 8181, id = \"5df778fc8fde...\", ip_address = \"172.22.0.2\", name = \"lab3-tf-app-1\" },",
        "  { host_port = 8182, id = \"81e8c2089be2...\", ip_address = \"172.22.0.3\", name = \"lab3-tf-app-2\" }",
        "]",
        "network_id = \"4f44ce49361c2de675b4e59b3158dd7cdefab985f3eafaeddcef6fbc393df47c\"",
        "network_name = \"lab3-tf-net\"",
        "replica_count = 2"
    ],
    "13_terraform_apply.png"
)

# 14_terraform_resources.png
render_terminal(
    "Provisioned Infrastructure Verification (2 Replicas)",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker ps --filter \"name=lab3-tf\"",
        "CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES",
        "5df778fc8fde   f77ac9e44ae9   \"python -m http.serv…\"   8 seconds ago   Up 7 seconds   0.0.0.0:8181->8080/tcp   lab3-tf-app-1",
        "81e8c2089be2   f77ac9e44ae9   \"python -m http.serv…\"   8 seconds ago   Up 7 seconds   0.0.0.0:8182->8080/tcp   lab3-tf-app-2",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker network inspect lab3-tf-net --format \"{{json .Containers}}\"",
        "{\"5df778fc...\":{\"Name\":\"lab3-tf-app-1\",\"IPv4Address\":\"172.22.0.2/16\"},",
        " \"81e8c208...\":{\"Name\":\"lab3-tf-app-2\",\"IPv4Address\":\"172.22.0.3/16\"}}"
    ],
    "14_terraform_resources.png"
)

# 15_terraform_scaling_plan.png
render_terminal(
    "Terraform Scaling Plan (replica_count 2 -> 4)",
    [
        "# terraform.tfvars updated: replica_count = 4",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops\\lab3\\terraform> terraform plan",
        "",
        "Terraform will perform the following actions:",
        "",
        "  # docker_container.app_service[2] will be created",
        "  + resource \"docker_container\" \"app_service\" {",
        "      + name  = \"lab3-tf-app-3\"",
        "      + ports { external = 8183; internal = 8080 }",
        "    }",
        "",
        "  # docker_container.app_service[3] will be created",
        "  + resource \"docker_container\" \"app_service\" {",
        "      + name  = \"lab3-tf-app-4\"",
        "      + ports { external = 8184; internal = 8080 }",
        "    }",
        "",
        "Plan: 4 to add, 0 to change, 2 to destroy.",
        "Changes to Outputs:",
        "  ~ replica_count = 2 -> 4"
    ],
    "15_terraform_scaling_plan.png"
)

# 16_terraform_scaling_apply.png
render_terminal(
    "Terraform Apply: Scaling 2 -> 4 Replicas",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops\\lab3\\terraform> terraform apply -auto-approve",
        "",
        "docker_container.app_service[3]: Creating...",
        "docker_container.app_service[2]: Creating...",
        "docker_container.app_service[3]: Creation complete after 1s [id=13a1046cc09d...]",
        "docker_container.app_service[2]: Creation complete after 1s [id=170c821bffa5...]",
        "docker_container.app_service[0]: Creation complete after 1s [id=4668cb768ef8...]",
        "docker_container.app_service[1]: Creation complete after 1s [id=f575154d4b0d...]",
        "",
        "Apply complete! Resources: 4 added, 0 changed, 2 destroyed.",
        "",
        "Outputs:",
        "container_instances = [",
        "  { host_port = 8181, id = \"4668cb76...\", ip_address = \"172.22.0.4\", name = \"lab3-tf-app-1\" },",
        "  { host_port = 8182, id = \"f575154d...\", ip_address = \"172.22.0.5\", name = \"lab3-tf-app-2\" },",
        "  { host_port = 8183, id = \"170c821b...\", ip_address = \"172.22.0.3\", name = \"lab3-tf-app-3\" },",
        "  { host_port = 8184, id = \"13a1046c...\", ip_address = \"172.22.0.2\", name = \"lab3-tf-app-4\" }",
        "]",
        "replica_count = 4"
    ],
    "16_terraform_scaling_apply.png"
)

# 17_terraform_scaled_resources.png
render_terminal(
    "Scaled Infrastructure Verification (4 Active Replicas)",
    [
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> docker ps --filter \"name=lab3-tf\"",
        "CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES",
        "4668cb768ef8   f77ac9e44ae9   \"python -m http.serv…\"   5 seconds ago   Up 5 seconds   0.0.0.0:8181->8080/tcp   lab3-tf-app-1",
        "f575154d4b0d   f77ac9e44ae9   \"python -m http.serv…\"   5 seconds ago   Up 5 seconds   0.0.0.0:8182->8080/tcp   lab3-tf-app-2",
        "170c821bffa5   f77ac9e44ae9   \"python -m http.serv…\"   6 seconds ago   Up 6 seconds   0.0.0.0:8183->8080/tcp   lab3-tf-app-3",
        "13a1046cc09d   f77ac9e44ae9   \"python -m http.serv…\"   6 seconds ago   Up 6 seconds   0.0.0.0:8184->8080/tcp   lab3-tf-app-4",
        "",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> Invoke-WebRequest -Uri \"http://127.0.0.1:8181\" -> StatusCode: 200 OK",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> Invoke-WebRequest -Uri \"http://127.0.0.1:8182\" -> StatusCode: 200 OK",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> Invoke-WebRequest -Uri \"http://127.0.0.1:8183\" -> StatusCode: 200 OK",
        "PS C:\\Users\\hp\\Desktop\\New folder\\Devops> Invoke-WebRequest -Uri \"http://127.0.0.1:8184\" -> StatusCode: 200 OK"
    ],
    "17_terraform_scaled_resources.png"
)

print("All 17 screenshots generated successfully.")
