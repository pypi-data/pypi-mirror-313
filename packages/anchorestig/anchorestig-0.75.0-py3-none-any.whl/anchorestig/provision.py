import subprocess as sp
import sys
import logging
import importlib.util
import os
import os.path

def install_cinc(privileged):
    if privileged:
        cmd = ["curl", "-L", "https://omnitruck.cinc.sh/install.sh", "|", "sudo", "bash", "-s", "--", "-P", "cinc-auditor", "-v", "5.22.50"]
    else:
        cmd = ["curl", "-L", "https://omnitruck.cinc.sh/install.sh", "|", "bash", "-s", "--", "-P", "cinc-auditor", "-v", "5.22.50"]
    try:
        sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    except Exception:
        print("Failed to install CINC auditor. Please try again or manually install by running 'curl -L https://omnitruck.cinc.sh/install.sh | sudo bash -s -- -P cinc-auditor -v 5.22.50'")
        exit()

def install_train_plugin():
    package_name = "anchorestig"
    spec = importlib.util.find_spec(package_name)
    train_k8s_container_path = f"{os.path.dirname(spec.origin)}/train-k8s-container"
    print(train_k8s_container_path)
    cmd = ["cinc-auditor", "plugin", "install", train_k8s_container_path]
    try:
        sp.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    except Exception:
        print("Failed to install the train k8s container plugin.")
        exit()