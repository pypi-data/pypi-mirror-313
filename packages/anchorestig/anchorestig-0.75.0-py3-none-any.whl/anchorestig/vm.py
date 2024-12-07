import os
import subprocess
import importlib.util
import datetime

def determine_profile(profile):
    package_name = "anchorestig"
    spec = importlib.util.find_spec(package_name)
    package_root_directory = os.path.dirname(spec.origin)

    if profile == "ubi8" or profile == "ubuntu2004" or profile == "ubi9" or profile == "ubuntu2204":
        policy_path = f"{package_root_directory}/policies/{profile}/anchore-{profile}-disa-stig-1.0.0.tar.gz"
    else:
        policy_path = profile
    return policy_path

def run_stig(output_dir, policy_path, input_file, ssh_user, ssh_password, ssh_host, ssh_key_path, sanitized_usertime):
    
    try:
        if input_file == "default":
            if ssh_password == "usekey":
                response = subprocess.run(["cinc-auditor", "exec", policy_path, "-t", f"ssh://{ssh_user}@{ssh_host}", "-i", ssh_key_path, "--reporter=cli", f"json:./{output_dir}/{sanitized_usertime}-output.json"], stdout=subprocess.PIPE)
            else:
                response = subprocess.run(["cinc-auditor", "exec", policy_path, "-t", f"ssh://{ssh_user}:{ssh_password}@{ssh_host}", "--reporter=cli", f"json:./{output_dir}/{sanitized_usertime}-output.json"], stdout=subprocess.PIPE)
        else:
            if not os.path.isfile(input_file):
                print(f"Input file: {input_file} does not exist. Please Retry.")
                pass
            else:
                if ssh_password == "usekey":
                    response = subprocess.run(["cinc-auditor", "exec", policy_path, "-t", f"ssh://{ssh_user}@{ssh_host}", "-i", ssh_key_path, f"--input-file={input_file}", "--reporter=cli", f"json:./{output_dir}/{sanitized_usertime}-output.json"], stdout=subprocess.PIPE)
                else:
                    response = subprocess.run(["cinc-auditor", "exec", policy_path, "-t", f"ssh://{ssh_user}:{ssh_password}@{ssh_host}", f"--input-file={input_file}", "--reporter=cli", f"json:./{output_dir}/{sanitized_usertime}-output.json"], stdout=subprocess.PIPE)
    except Exception:
        print("Failed to run STIG")
        stop_container(container_id)
        exit()

# Execute profiles on the remote machine
def run_stig_over_ssh(profile, input_file, host, user, password, key):
    try:
        policy_path = determine_profile(profile)
        dir_name = host.replace("/", "-").replace(":", "-")
        os.makedirs(f"stig-results/{dir_name}", exist_ok=True)

        now = datetime.datetime.now()
        sanitized_usertime = f"{user}-{now}".replace(" ", "-").replace("/", "-").replace(":", "-")

        print("\n-------Run Parameters-------\n")
        print(f"Target Host: {host}")
        print(f"Profile: {profile}")
        print(f"User: {user}")
        print(f'Output File Path: ./stig-results/{dir_name}/{sanitized_usertime}-output.json\n')

        run_stig(f"stig-results/{dir_name}", policy_path, input_file, user, password, host, key, sanitized_usertime)

    except Exception as e:
        print(f"Error running profile {profile}: {e}")
