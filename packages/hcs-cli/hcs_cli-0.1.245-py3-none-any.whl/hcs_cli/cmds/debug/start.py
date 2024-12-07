"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import click
from hcs_core.ctxp import recent
from hcs_cli.support.debug_util import get_mvn_build_cmd
import subprocess
import os
import shlex

_forwarding_process = None


@click.command()
@click.argument("service", type=str, required=False)
@click.option(
    "--skip/--build", "-s/-b", type=bool, required=False, default=False, help="Skip rebuild and re-deploy service"
)
def start(service: str, skip: bool, **kwargs):
    """Start build deploy and debug service"""

    service = recent.require(service, "k8s_service")

    pod_id = _get_pod_id(service)

    if not skip:
        _build_service()
        _push_jar_to_pod(service=service, pod_id=pod_id)

    pod_forwarding(pod_id)
    run_with_debug(pod_id)


def _get_pod_id(service):
    pod_name_command = ["kubectl", "get", "po", "-l", f"app={service}", "-o", "jsonpath='{.items[0].metadata.name}'"]
    pod_id = subprocess.run(pod_name_command, capture_output=True, check=True, text=True).stdout
    print("Pod Id fetched: ", pod_id)
    return pod_id


def pod_forwarding(pod_id):
    print("Start forwarding pod")
    pod_forwarding_command = f"kubectl port-forward {pod_id} 10762:10762"
    global _forwarding_process
    _forwarding_process = subprocess.Popen(
        shlex.split(pod_forwarding_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    print("Start forwarding pod:", _forwarding_process.pid)


def run_with_debug(pod_id):

    run_app_command = f"kubectl exec -it {pod_id} -c app -- /bin/bash -c 'java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=10762 -jar app.jar'"

    # Execute the command
    process = subprocess.Popen(shlex.split(run_app_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Continuously print logs
    try:
        for line in iter(process.stdout.readline, b""):
            print(line.decode("utf-8"))
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) to stop the process gracefully
        process.terminate()
        if _forwarding_process:
            _forwarding_process.terminate()


def _build_service():
    mvn_build_command = get_mvn_build_cmd()
    print(f"Running command: {mvn_build_command}")
    mvn_build_result = subprocess.Popen(
        mvn_build_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        text=True,
        shell=True,
    )
    # Read and print output line by line
    for line in iter(mvn_build_result.stdout.readline, ""):
        print(line, end="")

    # Wait for the process to finish
    mvn_build_result.wait()

    # Check if the command was successful
    if mvn_build_result.returncode == 0:
        print("Maven build completed successfully.")
    else:
        print("Maven build failed.")


def _push_jar_to_pod(service: str, pod_id: str):
    jar_files = _get_jar_files_with_keyword("target/", service)
    print("Jar file fetched: ", jar_files)
    jar_file = jar_files[0]
    push_image_command = f"cat target/{jar_file} | kubectl exec -i {pod_id} -c app -- sh -c 'cat > /app.jar'"
    print(f"Start pushing {jar_file} to k8s pod {pod_id} ")
    subprocess.run(push_image_command, capture_output=True, check=True, text=True, shell=True)
    print("Push success, starting app.jar")


def _get_jar_files_with_keyword(directory, keyword):
    jar_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".jar") and keyword in filename:
            jar_files.append(filename)
    return jar_files
