# Anchore STIG

Anchore STIG is a complete STIG solution that can be used to run STIG profile against static images, running containers in a kubernetes cluster, and virtual machines via ssh.

## Description

Use Anchore STIG to perform STIG checks against running containers in Kubernetes environments or static Docker images from a registry or stored locally. The tool executes automated scans against specific STIG Security Guide (SSG) policies. The program will output either a JSON report with a summary of STIG check results for runtime checks or XCCDF XML and OpenSCAP XML and HTML for static checks. 

The profiles for static, runtime, and vm are as follows:

* Ubuntu 20.04 (ubuntu-20.04)
* Ubuntu 22.04 (ubuntu-22.04)
* Universal Base Image 8 (ubi8) - This runs the full RHEL 8 STIG
* Universal Base Image 9 (ubi9) - This runs the full RHEL 9 STIG
* Postgres 9 (postgres9)
* Apache Tommcat 9 (apache-tomcat9)
* Crunchy PostgreSQL (crunchy-postgresql)
* JBOSS (jboss)
* Java Runtime Environment 7 (jre7)
* MongoDB Enterprise (mongodb)
* nginx (nginx)

## Getting Started

### Dependencies

#### Overall
* `python3 >= 3.8 with pip installed`
* `make`
* `saf` - There is an option to install this tool after running the tool, but installing it manually is the most reliable.

#### Static
* `docker`

#### Runtime
* `kubectl exec` privileges
* Pods running one of the above listed software / OS types

#### VM
* An SSH profile for the VM or the path to the key used to connect to the machine
* The VM's endpoint


### Install

* clone the repo
* run `make` to install 

### Running the Program

#### Runtime

* Run `anchorestig runtime` from the terminal. 
    * NOTE: This edition of the demo has been optimized for single-container pods by default

* The program will run in interactive mode by executing `anchorestig runtime --interactive` from the terminal, however, you may also use the following CLI input parameters:

```
CLI Input Parameters:

  -i, --image TEXT       Specify profile to use. Available options are ubuntu-20.04, ubi8, postgres9, apache-tomcat9, crunchy-postgresql, jboss, jre7, mongodb, nginx
  -p, --pod TEXT         Any running pod running an image that runs one of the specififed profile's software
  -c, --container TEXT   Container in the pod to run against
  -o, --outfile TEXT     Output file name. Only JSON output filetype is supported (include the '.json' extension with the output file name in CLI)
  -n, --namespace TEXT   Namespace the pod is located in
  -u, --usecontext TEXT  Specify the kubernetes context to use
  -b, --aws-bucket TEXT  Specify the S3 bucket to upload results to. Omit to skip upload
  -a, --account TEXT     Specify the Anchore STIG UI account to associate the S3 upload with. Omit to skip upload
  -t, --interactive      Run in interactive mode
  -s, --sync             Sync policies from Anchore
  --help                 Show this message and exit.

```
Ex: `anchore-stig runtime -u current -n test -i postgres9 -p postgres9 -c default -o postgres.json`

* NOTE: The output file will be saved to the `./outputs` directory

##### Viewing Results

Navigate to the `./outputs` directory to view the output file. 

#### Static

* Run the tool using `anchorestig static IMAGE`. 
    * Ex: `anchorestig static docker.io/ubi8:latest`

```
CLI Input Parameters:

    -u, --username TEXT    Username for private registry
    -p, --password TEXT    Password for private registry
    -r, --url TEXT         URL for private registry
    -b, --aws-bucket TEXT  S3 upload. Specify bucket name
    -a, --account TEXT     Anchore STIG UI account. Required for S3 upload
    -s, --insecure         Allow insecure registries or registries with custom certs
    -l, --profile TEXT     Specify profile to run. Can be the name of an existing profile or the path to a custom profile
    -i, --input-file TEXT  Specify the path to a custom input file to run with a profile.
    --help                 Show this message and exit.
```

##### Viewing Results

Navigate to the `./stig-results` directory. The output directory containing output files will be named according to the image scanned.

#### VM
* Run the tool using `anchorestig vm -h <vm-endpoint> -u <user> -k <path-to-key> --profile <profile>`

```
CLI Input Paramters:

  -u, --user TEXT        Username for SSH Host  [required]
  -p, --password TEXT    Password for SSH Host
  -k, --key TEXT         PEM Key path for SSH Host
  -h, --host TEXT        Username for SSH Host  [required]
  -l, --profile TEXT     Specify profile to run. Can be the name of an existing profile or the path to a custom profile [required]
  -i, --input-file TEXT  Specify the path to a custom input file to run with a profile.
  --help                 Show this message and exit.
```

## Help

Use the `--help` flag to see more information on how to run the program:

`anchorestig --help`

## CINC Functionality Explanation

`cinc-auditor` allows users to specify a target to run profiles against. This can be a number of things including SSH targets or a local system. The `train-k8s-container` plugin allows our STIG tool to target a kubernetes namespace, pod, and container to run cinc profiles against. When a container is set as the target, each individual control will be prepended with `kubectl exec .....` and the appropriate commands to run within the container and retireve the results to make the determination of a pass or fail against the control baseline.

## Modifying Controls

The `policies` directory contains sub-directories for the Ubuntu, UBI, and Postgres STIG profiles. Each directory has a `tar.gz` file that can be decompressed. From there, each control that runs is defined as a ruby gem file in the `controls` directory. The ID of each control (displayed in Heimdall) is pulled from the `control` section at the beginning of the ruby gem file. To change what is displayed, change the control id at the beginning of the file.

## Adding Not-Applicable Controls

The `UBI 8` and `Ubuntu 20.04` policies were built with the `not-applicable` rules removed. To add them back, untar the tar files in each repository, move the ruby gem files from the `not-applicable/` directory to the controls directory. Then run `cinc-auditor archive .` in the untarred directory. This will generate a new tar archive file. Replace the original archive, that you un-tarred at the beginning with the newly generated one and the newly included rules will run.

<!-- ## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Anchore License - see the LICENSE.md file for details -->