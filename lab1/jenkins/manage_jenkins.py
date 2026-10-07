import urllib.request
import urllib.parse
import http.cookiejar
import json
import time
import os
import sys

JENKINS_URL = "http://localhost:8080"
JOB_NAME = "DevOps-CI-CD-Pipeline"

# Install global cookie jar opener
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
urllib.request.install_opener(opener)

def get_crumb():
    try:
        req = urllib.request.Request(f"{JENKINS_URL}/crumbIssuer/api/json")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('crumbRequestField', 'Jenkins-Crumb'), data.get('crumb', '')
    except Exception as e:
        print(f"Crumb fetching status/error: {e}")
        return None, None

def create_or_update_job(config_path):
    crumb_field, crumb_value = get_crumb()
    with open(config_path, 'rb') as f:
        xml_data = f.read()

    headers = {'Content-Type': 'application/xml'}
    if crumb_field and crumb_value:
        headers[crumb_field] = crumb_value

    job_exists = False
    try:
        req = urllib.request.Request(f"{JENKINS_URL}/job/{JOB_NAME}/config.xml")
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                job_exists = True
    except Exception:
        job_exists = False

    if job_exists:
        print(f"Job '{JOB_NAME}' exists. Updating configuration...")
        req = urllib.request.Request(f"{JENKINS_URL}/job/{JOB_NAME}/config.xml", data=xml_data, headers=headers, method='POST')
    else:
        print(f"Creating job '{JOB_NAME}'...")
        req = urllib.request.Request(f"{JENKINS_URL}/createItem?name={JOB_NAME}", data=xml_data, headers=headers, method='POST')

    with urllib.request.urlopen(req) as resp:
        print(f"Job configured successfully! HTTP Status: {resp.status}")

def trigger_build():
    crumb_field, crumb_value = get_crumb()
    headers = {}
    if crumb_field and crumb_value:
        headers[crumb_field] = crumb_value

    print(f"Triggering build for {JOB_NAME}...")
    req = urllib.request.Request(f"{JENKINS_URL}/job/{JOB_NAME}/build", data=b'', headers=headers, method='POST')
    with urllib.request.urlopen(req) as resp:
        print(f"Build triggered! HTTP Status: {resp.status}")

def wait_for_build():
    print("Waiting for build to start...")
    build_num = None
    for _ in range(30):
        try:
            req = urllib.request.Request(f"{JENKINS_URL}/job/{JOB_NAME}/api/json")
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                last_build = data.get('lastBuild')
                if last_build:
                    build_num = last_build['number']
                    print(f"Identified active build #{build_num}")
                    break
        except Exception as e:
            pass
        time.sleep(2)

    if not build_num:
        print("Build did not start within expected timeframe.")
        return False

    print(f"Streaming Console Output for Build #{build_num}...\n" + "="*60)
    done = False
    offset = 0
    while not done:
        try:
            # Fetch console log
            log_req = urllib.request.Request(f"{JENKINS_URL}/job/{JOB_NAME}/{build_num}/consoleText")
            with urllib.request.urlopen(log_req) as log_resp:
                log_text = log_resp.read().decode('utf-8', errors='replace')
                if len(log_text) > offset:
                    sys.stdout.write(log_text[offset:])
                    sys.stdout.flush()
                    offset = len(log_text)

            req = urllib.request.Request(f"{JENKINS_URL}/job/{JOB_NAME}/{build_num}/api/json")
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                building = data.get('building', True)
                result = data.get('result')

                if not building and result is not None:
                    print("="*60)
                    print(f"BUILD #{build_num} COMPLETED: {result}")
                    print("="*60)
                    return result == "SUCCESS"
        except Exception as e:
            pass
        time.sleep(2)
    return False

if __name__ == '__main__':
    config_file = os.path.join(os.path.dirname(__file__), 'job_config.xml')
    create_or_update_job(config_file)
    trigger_build()
    success = wait_for_build()
    if not success:
        sys.exit(1)
