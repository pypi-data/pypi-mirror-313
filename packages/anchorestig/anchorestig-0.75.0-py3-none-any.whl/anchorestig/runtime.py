import subprocess as sp
import logging
import importlib.util
import shutil
import os
from .inputs import *
import os.path
import boto3
import datetime
import itertools
import threading
import time
import sys
from botocore.exceptions import NoCredentialsError, ClientError

def upload_to_s3(bucket_name, file, account, image_digest, image_name):
    """
    Upload files from a specified directory to an AWS S3 bucket.

    :param bucket_name: Name of the S3 bucket.
    :param directory: Directory containing files to upload.
    """
    # Check if the directory exists
    if not os.path.exists(file):
        print(f"Error: output directory does not exist.")
        return

    # Initialize S3 client with custom credentials
    if "@" in image_name:
        image_name = image_name.split('@')[0] + "NOTAG"
    
    image_name = image_name.removeprefix('http://').removeprefix('https://')
    
    tag = image_name.split(':')[-1]
    registry = image_name.split('/', 1)[0]
    repository = image_name.split('/', 1)[-1].split(":")[0].replace("/", "-")

    s3 = boto3.client('s3')

    file_name = file.split("/")[-1]
    date_filename = add_date_prefix(file_name)

    try:
        # Walk through the directory and upload files
        file_path = f"anchore/{account}/{registry}/{repository}/{tag}/{image_digest}/{date_filename}"
        s3.upload_file(file, bucket_name, file_path)
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"Error: {e}")

def sync_policies():
    package_name = "anchorestig"
    spec = importlib.util.find_spec(package_name)
    package_root_directory = os.path.dirname(spec.origin)
    try:
        sp.run(["docker", "run", "--rm", "-d", "--name=policies", "anchore/combined-stig:latest", "sleep", "1000"])
        sp.run(["docker", "cp", "policies:policies/.", f"{package_root_directory}/policies"])
        sp.run(["docker", "kill", "policies"])
    except Exception:
        print("Unauthorized to pull Anchore policies. Please login with the provided Docker credentials and try again.")
        exit()

def add_date_prefix(filename):
    date_prefix = str(datetime.datetime.now().timestamp()).replace(" ", "_").split(".")[0]
    split_filename = filename.rsplit(".", 1)
    return split_filename[0] + date_prefix + "." + split_filename[-1]

def completedStep():
    """ 
    Show progress of program in stdout 
    """
    global step, stepText
    if not step == totalSteps:
        step+=1
    print('\u2705 (' + str(step) + '/' + str(totalSteps) + ') -', stepText)

def failedStep(e):
        """ 
        Show error and exit if exception occurs 
        """
        print('\n\u274C Program failed. See details below:\n')
        print('Failed Step (' + str(step+1) + '/' + str(totalSteps) + '):', stepText, '\n')
        print(e,'\n')
        exit()

def scan():
    context = usecontext.replace(':',"--colon--")
    context = context.replace('/','--slash--')
    print(namespace)
    sp.run([
            "cinc-auditor","exec",controls,
            "-t","k8s-container://"+context+"/"+namespace+'/'+pod+'/'+container,
            "--input-file",profile,
            "--reporter=cli",
            "json:./output/"+outfile,
            "--log-level","debug"
            ],
            stdout=l, stderr=e, encoding='utf-8'
            )

def verifyOutput(outfile):
    """
    Verify that the output report has been successfully created and complete program execution
    """
    global step, stepText
    stepText = 'Output file verified.'
    print('  \u231B',stepText + '..', end="\r")
    try:
        if not os.path.isfile("./output/" + outfile):
            failedStep('Error generating output file. Please check the ./logs directory for more details.\n')
        with open("./output/" + outfile,"r") as f:
            length = len(f.readlines())
        if length < 1:
            failedStep('Error generating output file. Please check the ./logs directory for more details.\n')
        completedStep()
        print('\n The REM 2.0 STIG Analyzer process is complete. Please review your output here: ./output/' + outfile +'\n')
    except Exception as e: failedStep(e)

def check_saf_installed():
    # Check if 'saf' binary is available in PATH
    saf_path = shutil.which('saf')
    
    if saf_path:
        print(f"'saf' is installed at: {saf_path}")
    else:
        print("'saf' is not installed. If running this tool in a disconnected environment, please cancel this run with CTRL+C and manually install before proceeding.")
        
        # Prompt user to install via Homebrew or npm
        choice = input("Do you want to install 'saf' via Homebrew (1) or npm (2)? Enter 1 or 2: ")
        
        if choice == '1':
            install_command = "HOMEBREW_NO_AUTO_UPDATE=1 brew install mitre/saf/saf-cli"
        elif choice == '2':
            install_command = "npm install -g @mitre/saf"
        else:
            print("Invalid choice. Please enter 1 for Homebrew or 2 for npm.")
            return
        
        try:
            # Run the chosen installation command
            sp.run(install_command, shell=True, check=True)
            print(f"'saf' has been installed successfully using {install_command}.")
        except sp.CalledProcessError as e:
            print(f"Installation failed: {e}")

def saf_convert_output(outfile):
    conversion_tools = [ 'hdf2xccdf', 'hdf2ckl', 'hdf2csv']

    split_outfile = outfile.split('/')[-1].split('.json')[0]
    outfile_dir_exists = os.path.exists(f'./output/{split_outfile}')
    if not outfile_dir_exists: os.makedirs(f'./output/{split_outfile}')

    done = False
    def animate():
        print('Converting to additional output formats')
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\r' + c)
            sys.stdout.flush
            time.sleep(0.1)
        sys.stdout.write('\rDone converting.     ')
    t = threading.Thread(target=animate)
    t.start()

    for tool in conversion_tools:
        if tool == "hdf2xccdf":
            file_ending = ".xml"
        elif tool == "hdf2ckl":
            file_ending = ".ckl"
        else:
            file_ending = ".csv"
        conversion_cmd = f"saf convert {tool} -i ./output/{outfile} -o ./output/{split_outfile}/{split_outfile}{file_ending}" 
        try:
            # Run the chosen installation command
            sp.run(conversion_cmd, shell=True, check=True)
            # print(f"Successfully converted {outfile} using {conversion_cmd}.")
        except sp.CalledProcessError as e:
            print(f"Failed to convert {outfile} to {split_outfile}{file_ending}: {e}")
    done = True


def runtime_analysis(input_image, input_pod, input_container, input_namespace, input_usecontext, input_cluster, input_outfile, input_aws_s3_bucket_upload, input_account, input_image_digest, input_image_name):
    global step, stepText, e, totalSteps
    global image, pod, container, namespace, usecontext, cluster, outfile, controls, profile, aws_s3_bucket_upload, account, l, e

    # Set logger config and variables
    step = 0
    stepText = 'Setup complete. Running STIG Scan...'
    totalSteps = 3

    try:
        """
        Save input params as variables
        """
        logging.basicConfig(level=logging.INFO)
        log = logging.getLogger("REM 2.0")
        l = open('./logs/log.txt','w+')
        e = open('./logs/err.txt','w+')
        image = str(input_image).strip()
        pod = input_pod.strip()
        container = str(input_container).strip()
        namespace = input_namespace.strip()
        usecontext = input_usecontext.strip()
        cluster = input_cluster.strip()
        outfile = input_outfile.strip()
        if input_aws_s3_bucket_upload != 'skip_upload':
            aws_s3_bucket_upload = input_aws_s3_bucket_upload.strip()
            account = input_account.strip()
        image_digest = input_image_digest
        image_name = input_image_name
        outfile = input_outfile
        out_ext = outfile[outfile.index('.')+1:len(outfile)]
        outdir_exists = os.path.exists(f'./output/{outfile.split("/")[0]}')
        if not outdir_exists: os.makedirs(f'./output/{outfile.rsplit("/")[0]}')
        out_dir='./'

        package_name = "anchorestig"
        spec = importlib.util.find_spec(package_name)
        package_root_directory = os.path.dirname(spec.origin)

        if image == 'ubuntu-20.04': 
            image = 'ubuntu2004'
            policy_dir = f'{package_root_directory}/policies/ubuntu2004/'
        elif image == 'ubi8': policy_dir = f'{package_root_directory}/policies/ubi8/'
        elif image == 'postgres9': policy_dir = f'{package_root_directory}/policies/postgres9/'
        elif image == 'apache-tomcat9': policy_dir = f'{package_root_directory}/policies/apache-tomcat9/'
        elif image == 'crunchy-postgresql': policy_dir = f'{package_root_directory}/policies/crunchy-postgresql/'
        elif image == 'jboss': policy_dir = f'{package_root_directory}/policies/jboss/'
        elif image == 'jre7': policy_dir = f'{package_root_directory}/policies/jre7/'
        elif image == 'mongodb': policy_dir = f'{package_root_directory}/policies/mongodb/'
        elif image == 'nginx': policy_dir = f'{package_root_directory}/policies/nginx/'
        elif image == 'ubi9': policy_dir = f'{package_root_directory}/policies/ubi9/'
        elif image == 'ubuntu2204': policy_dir = f'{package_root_directory}/policies/ubuntu2204/'
        else:
            failedStep('Configuration and variables failed. Please ensure that you\'re using the correct input parameter values.')

        profile = policy_dir + 'profile.yaml'
        controls = policy_dir + 'anchore-'+image+'-disa-stig-1.0.0.tar.gz'
        proc = sp.Popen(["kubectl","--context",usecontext,"--namespace",namespace,"get","pods","-o","jsonpath='{..containers[*].name}'"], stdout=sp.PIPE)
        output = proc.stdout.read().decode("utf-8").strip().replace("'","")
        containerList = output.split(' ')

        completedStep()
    except Exception as e: failedStep(e)

    try:
        scan()
        # Check for errors
        e.close()
        if os.stat("./logs/err.txt").st_size != 0: 
            raise Exception("There was an error with the scan. Please review the ./logs/err.txt file for more information.")
        else:
            e = open('./logs/err.txt','w+')
            stepText = 'STIG scan complete. Verifying output file...'
            if input_aws_s3_bucket_upload != 'skip_upload':
                outfile_raw_dir = f"{outfile.rsplit('.', 1)[0]}"
                output_file_dir = f"./output/{outfile.split('/')[0]}"
                for file in os.listdir(output_file_dir):
                    upload_to_s3(aws_s3_bucket_upload, file, account, image_digest, image_name)
            completedStep()
    except Exception as e: failedStep(e)

    verifyOutput(outfile)