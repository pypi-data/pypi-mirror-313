import subprocess
import os


def resart_service(service_full_name: str, **kwargs):
    restart_command = ["kubectl", "rollout", "restart", f"{service_full_name}"]

    try:
        result = subprocess.run(restart_command, capture_output=True, check=True, text=True)
        print("Command execution successful:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e.stderr)


def get_service_full_name(service: str, **kwargs):
    if service == "clouddriver" or service == "connection-service":
        return f"statefulset/{service}-statefulset"
    else:
        return f"deployment/{service}-deployment"


def get_mvn_build_cmd():
    for filename in os.listdir():
        if filename == "settings.xml":
            return "mvn package -DskipTests -s settings.xml"
    return "mvn package -DskipTests"
