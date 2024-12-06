
# Copyright (C) Integrate.ai, Inc. All rights reserved.

import subprocess
import sys
from integrate_ai.utils.rest_client import RestClient
import typer
import os
import rich
from integrate_ai.utils.typer_utils import (
    TogglePromptOption,
)


app = typer.Typer(no_args_is_help=True)


@app.command()
def install(
    token: str = TogglePromptOption(
        ...,
        help="Your generated IAI token.",
        prompt="Please provide your IAI token",
        envvar="IAI_TOKEN",
    ),
    taskrunner_name: str = TogglePromptOption(
        ...,
        help="The taskrunner name to register.",
        prompt="Please provide the taskrunner name",
        envvar="IAI_TASKRUNNER_NAME",
    ),
):
    """
    This command register this node and save the regiter information to ecsanywhwere_output.txt
    """
    if os.geteuid() != 0:
        rich.print("This command must be run as root.")
        sys.exit(1)

    # clean up rm /tmp/ecs-anywhere-install.sh if there is any
    if os.path.exists("/tmp/ecs-anywhere-install.sh"):
        subprocess.run("rm /tmp/ecs-anywhere-install.sh", shell=True, check=True, text=True, capture_output=True)

    # register taskrunner id
    client = RestClient(token=token)
    response = client.register_on_prem_taskrunner(taskrunner_name)

    # install ecs anywhere
    cmd = 'sudo curl --proto "https" -o "/tmp/ecs-anywhere-install.sh" "https://amazon-ecs-agent.s3.amazonaws.com/ecs-anywhere-install-latest.sh"'
    cmd += " && sudo bash /tmp/ecs-anywhere-install.sh"
    cmd += f' --region "{response["region"]}"'
    cmd += f' --cluster "{response["cluster_name"]}"'
    cmd += f' --activation-id "{response["activation_id"]}"'
    cmd += f' --activation-code "{response["activation_code"]}"'
    cmd += "> ecsanywhwere_output.txt"

    try:
        rich.print("Registering...")
        subprocess.run(cmd, shell=True, check=True)
        rich.print("Agent registered successfully.")
        rich.print("Output is saved in ecsanywhwere_output.txt. The file contains instance id, please do not delete.")
    except subprocess.CalledProcessError as e:
        rich.print(f"Command failed with error: {e.stderr}, Logs can be found in ecsanywhwere_output.txt.")


@app.command()
def uninstall(
    token: str = TogglePromptOption(
        ...,
        help="Your generated IAI token.",
        prompt="Please provide your IAI token",
        envvar="IAI_TOKEN",
    ),
    taskrunner_name: str = TogglePromptOption(
        ...,
        help="The taskrunner id to register.",
        prompt="Please provide the taskrunner id",
        envvar="IAI_TASKRUNNER_NAME",
    ),
):
    """
    This command deregister this node and clean up the directory.
    """
    if os.geteuid() != 0:
        rich.print("This command must be run as root.")
        sys.exit(1)
    # register taskrunner id
    client = RestClient(token=token)
    response = client.deregister_on_prem_taskrunner(taskrunner_name=taskrunner_name, instance_id=get_instance_id())
    rich.print("Deregister instance ", response["containerInstance"]["ec2InstanceId"])

    # uninstall ecs anywhere
    stop_ecs = "sudo systemctl stop ecs amazon-ssm-agent"

    try:
        stop_ecs_out = subprocess.run(stop_ecs, shell=True, check=True, text=True, capture_output=True)
        rich.print(stop_ecs_out.stdout)

        # Check OS and remove packages
        os_type = None
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("ID="):
                        os_type = line.strip().split("=")[1].replace('"', "").lower()
                        break
        except FileNotFoundError:
            raise Exception("Unable to detect OS. /etc/os-release not found.")

        if "centos" in os_type or "rhel" in os_type:
            uninstall_packages_cmd = "sudo yum remove -y amazon-ecs-init amazon-ssm-agent"
        elif "debian" in os_type or "ubuntu" in os_type:
            uninstall_packages_cmd = "sudo apt remove -y amazon-ecs-init amazon-ssm-agent"
        else:
            raise Exception("Unsupported OS for package removal")

        uninstall_out = subprocess.run(uninstall_packages_cmd, shell=True, check=True, text=True, capture_output=True)
        rich.print(uninstall_out.stdout)

        # Remove leftover directories
        remove_directories_cmd = (
            "sudo rm -rf /var/lib/ecs /etc/ecs /var/lib/amazon/ssm /var/log/ecs /var/log/amazon/ssm"
        )
        subprocess.run(remove_directories_cmd, shell=True, check=True, text=True)
        rich.print("Leftover directories removed")

        # Remove instance id file
        remove_output_cmd = "sudo rm ecsanywhwere_output.txt"
        subprocess.run(remove_output_cmd, shell=True, check=True, text=True)
        rich.print("ecsanywhwere_output.txt removed")

    except subprocess.CalledProcessError as e:
        rich.print(f"Command failed with error: {e.stderr}")


def get_instance_id():
    result = subprocess.check_output(
        "grep 'Container instance arn:' ecsanywhwere_output.txt | sed 's#.*/##'", shell=True
    )
    instance_id = result.decode("utf-8").strip().strip('"')
    if not instance_id:
        rich.print(
            "[red]Error: Could not parse instance ID from ecsanywhwere_output.txt. Please verify the file's contents."
        )
        raise Exception("Instance ID not found.")
    rich.print("Deregister instance with instance_id ", instance_id)
    return instance_id


@app.callback()
def main():
    """
    Sub command for managing on-prem taskrunners related operations.
    """
