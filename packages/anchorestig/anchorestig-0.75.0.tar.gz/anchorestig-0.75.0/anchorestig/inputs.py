import getopt, sys
import subprocess as sp
import json
import os

def selectFromDict(options, name):
    """ 
    Have the user select the container image that they are analyzing. Used in demo.main() to select
    and download the appropriate SSG policy. 
    """
    index = 0
    indexValidList = []
    print("\nPlease select an image profile (enter '1' for ubuntu:20.04, '2' for ubi8, '3' for postgre9, '4' for apache tomcat 9, '5' for crunchy postgresql, '6' for jboss, '7' for jre 7, '8' for mongodb, '9' for nginx, '10' for ubi9, or '11' for ubuntu:22.04):\n")
    for optionName in options:
        index = index + 1
        indexValidList.extend([options[optionName]])
        print(str(index) + '. ' + optionName)
    inputValid = False
    while not inputValid:
        inputRaw = input("\nImage Profile (enter 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, or 11): ")
        if inputRaw.isnumeric():
            inputNo = int(inputRaw) - 1
            if inputNo > -1 and inputNo < len(indexValidList):
                selected = indexValidList[inputNo]
                inputValid = True
                break
            else:
                print('\nNot a valid selection. Please select a valid ' + name)
        else:
            print('\nNot a valid selection. Please select a valid ' + name)
    return selected

def runtime_get_image_digest(pod, namespace, container):
    logdir_exists = os.path.exists('./logs')
    if not logdir_exists: os.makedirs('./logs')
    errout = open('./logs/err.txt','w+')
    image_name = sp.run(['kubectl', 'get', 'pod', pod, '-n', namespace, '-o', f'jsonpath=\"{{.status.containerStatuses[?(@.name==\'{container}\')].image}}\"'], stdout=sp.PIPE, stderr=errout, encoding='utf-8').stdout.strip().strip('"')
    image_digest = sp.run(['kubectl', 'get', 'pod', pod, '-n', namespace, '-o', f'jsonpath=\"{{.status.containerStatuses[?(@.name==\'{container}\')].imageID}}\"'], stdout=sp.PIPE, stderr=errout, encoding='utf-8').stdout.strip().strip('"').split("@")[-1]
    return image_digest, image_name

def get_runtime_cluster(usecontext):
    logdir_exists = os.path.exists('./logs')
    if not logdir_exists: os.makedirs('./logs')
    errout = open('./logs/err.txt','w+')
    try:
        proc = sp.run(['kubectl','config','view','-o',"jsonpath='{.contexts[?(@.name==\""+usecontext+"\")]}'"], stdout=sp.PIPE, stderr=errout, encoding='utf-8')
        contextdata = proc.stdout.strip().strip("'")
        contextdata = json.loads(contextdata)
        contextdata = contextdata['context']
        if "cluster" in contextdata: 
            cluster = contextdata['cluster']
            if cluster == '': 
                raise Exception("Cluster value is blank or not found in context config file")
            return cluster
        else: 
            raise Exception("Cluster not found within context. Please add a cluster to your context config and try again.")
        if "namespace" in contextdata: 
            print("\n**NOTE: A namespace has been found in the context you're using. Please note that you will still be required to provide a \
                namespace that will be used in the program execution if you have not already included one with CLI input.")

    except Exception as e:
        print('\n\u274C There was an error finding the cluster with the context provided. Please review your input, verify that the context exists, and try again.\n\n', e)
        exit()

def collect_inputs():
    print('\n -- REM 2.0: Container Runtime Automated STIG Analyzer --')

    # Set variables used to collect input parameters
    clear = '\x1b[2K\n'
    args = sys.argv[1:]
    shortopts = 'i:p:c:o:n:u:h'
    longopts = ['image=','pod=','container=','outfile=','namespace=','usecontext=','help']
    options = {}
    options['Ubuntu 20.04'] = 'ubuntu-20.04'
    options['Universal Base Image 8 (ubi8)'] = 'ubi8'
    options['Postgres 9'] = 'postgres9'
    options['Apache Tomcat 9'] = 'apache-tomcat9'
    options['Crunchy PostgreSQL'] = 'crunchy-postgresql'
    options['JBOSS'] = 'jboss'
    options['JRE 7'] = 'jre7'
    options['MongoDB'] = 'mongodb'
    options['nginx'] = 'nginx'
    options['Ubuntu 22.04'] = 'ubuntu2204'
    options['Universal Base Image 9 (ubi9)'] = 'ubi9'
    helpflag = False
    container = False
    namespace = False
    usecontext = False
    podprinted = False
    imageprinted = False
    aws_s3_bucket_upload = False
    account = False
    cluster = ''
    logdir_exists = os.path.exists('./logs')
    if not logdir_exists: os.makedirs('./logs')
    errout = open('./logs/err.txt','w+')

    try:
        """ 
        Save input args to variables, or show Help text if the --help argument was input 
        """
        arguments, values = getopt.getopt(args, shortopts, longopts)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--help"):
                print('Please see README located at: https://github.com/bknfzr/stig\n')
                helpflag = True
                exit()
            if currentArgument in ("-i", "--image"):
                image = currentValue
            if currentArgument in ("-p", "--pod"):
                pod = currentValue
            if currentArgument in ("-c", "--container"):
                container = currentValue 
            if currentArgument in ("-o", "--outfile"):
                outfile = currentValue
            if currentArgument in ("-n", "--namespace"):
                namespace = currentValue
            if currentArgument in ("-u","--usecontext"):
                usecontext = currentValue
            if currentArgument in ("-a", "--aws"):
                aws_s3_bucket_upload = currentValue
            if currentArgument in ("-c", "--account"):
                account = currentValue
    except getopt.error as err:
        print ('\n\u274C The program failed, see the following error\n\n:' + str(err))

    if not helpflag:
        """ 
        Collect input variables for all remaining arguments 
        """
        try:
            contextExists = False
            while not contextExists:
                # Set usecontext variable
                if not usecontext:
                    usecontext = input("\nPlease provide the context to use (to use the current context, type 'current' or press ENTER): ")
                    if usecontext == '':
                        usecontext = 'current'
                if usecontext == 'current':
                    try:
                        print('fetching name of current context...', end='\r')
                        proc = sp.run(['kubectl','config','current-context'], stdout=sp.PIPE, stderr=errout, encoding='utf-8')
                        usecontext = proc.stdout.strip()
                    except Exception as e:
                        print('\n\u274C Error obtaining the current user context:\n\n', e)
                        exit()
                else:
                    try:
                        proc = sp.run(['kubectl','config','view','-o',"jsonpath='{.contexts[*].name}'"], stdout=sp.PIPE, stderr=errout, encoding='utf-8')
                        contexts = proc.stdout.strip()
                        contexts = contexts.strip("'").split()
                        if usecontext in contexts: 
                            contextExists = True
                        else: 
                            usecontext = False
                            print('\n\u274C The context provided was not found.')
                    except Exception as e:
                        print('\n\u274C There was an error with the provided context. Please review your input, verify that the context exists, and try again.\n\n', e)
                        exit()
            
            print(clear, '\nContext:',usecontext)

            # Get context info
            try:
                proc = sp.run(['kubectl','config','view','-o',"jsonpath='{.contexts[?(@.name==\""+usecontext+"\")]}'"], stdout=sp.PIPE, stderr=errout, encoding='utf-8')
                contextdata = proc.stdout.strip().strip("'")
                contextdata = json.loads(contextdata)
                contextdata = contextdata['context']
                if "cluster" in contextdata: 
                    cluster = contextdata['cluster']
                    if cluster == '': 
                        raise Exception("Cluster value is blank or not found in context config file")
                    print("\nCluster: ", cluster)
                else: 
                    raise Exception("Cluster not found within context. Please add a cluster to your context config and try again.")
                if "namespace" in contextdata: 
                    print("\n**NOTE: A namespace has been found in the context you're using. Please note that you will still be required to provide a \
    namespace that will be used in the program execution if you have not already included one with CLI input.")

            except Exception as e:
                print('\n\u274C There was an error finding the cluster with the context provided. Please review your input, verify that the context exists, and try again.\n\n', e)
                exit()

            # Set namespace variable
            if not namespace:
                namespace = input("\nPlease provide the namespace name (to use the default namespace, type 'default' or press ENTER): ")
                if namespace == '':
                    namespace = 'default'
            try:
                proc = sp.run(['kubectl','get','namespaces','--context', usecontext, '-o',"jsonpath='{.items[*].metadata.labels.kubernetes\.io/metadata\.name}'"], stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf-8')
                namespaceerr = proc.stderr
                if namespaceerr:                
                    raise Exception("The provided namespace errored out.\n\n", namespaceerr)
                else:
                    namespaces = proc.stdout.strip().strip("'").split()
                    if namespace not in namespaces:
                        raise Exception("The namespace:'" + namespace + "' could not be found.\n")
                    print('\nNamespace:',namespace)
            except Exception as e:
                print('\n\u274C Error with the provided namespace: ' + namespace + '.\n\n', e)
                exit()

            # Set image variable
            if not 'image' in globals():
                image = selectFromDict(options, 'image')
                print('\nImage:',image)  
                imageprinted = True
            elif not imageprinted: print('\nImage:',image) 
            
            # Set pod variable
            if not 'pod' in globals():
                pod = input("\nPlease provide the pod name: ")
                print('Verifying that pod exists...', end='\r')
                print(clear + 'Pod:',pod)
                podprinted = True
            checkforpod = sp.run(['kubectl','get','pods',pod,'-n',namespace, '--context', usecontext], stdout=sp.DEVNULL, stderr=sp.PIPE, encoding='utf-8')
            poderr = checkforpod.stderr
            if poderr:
                raise Exception("The pod:'" + pod + "' could not be found. Please retry with a running pod.\n")
            elif not podprinted: print('\nPod:',pod)

            # Set container variable
            if not container:
                container = input("\nPlease provide the container name (to use the default container, type 'default' or press ENTER): ")
                if container == '':
                    container = 'default'
            if container == 'default':
                try:
                    print('fetching name of default container...', end='\r')
                    proc = sp.run(['kubectl','get','pods',pod,'-n',namespace, '--context', usecontext,'-o',"jsonpath='{.spec.containers[0].name}'"], stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf-8')
                    containererr = proc.stderr
                    if containererr:
                        raise Exception(containererr)
                    container = str(proc.stdout).strip("'")
                    print(clear + 'Container:',container)
                except Exception as e:
                    print('\n\u274C Error obtaining the default container name for the Pod: ' + pod + ': \n\n', e)
                    exit()
            else:
                try:
                    print('fetching name of default container...', end='\r')
                    proc = sp.run(['kubectl','get','pods',pod,'-n',namespace, '--context', usecontext,'-o',"jsonpath='{.spec.containers[*].name}'"], stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf-8')
                    containererr = proc.stderr
                    if containererr:                
                        raise Exception("The provided container name errored out.\n\n", containererr)
                    else:
                        containers = proc.stdout.strip().strip("'").split()
                        if container not in containers:
                            raise Exception("The container:'" + container + "' could not be found.\n")
                    print(clear + 'Container:',container)
                except Exception as e:
                    print('\n\u274C Error finding the container name: ' + container + ' provided for the Pod: ' + pod + ': \n\n', e)
                    exit()

            # Set output filename + extension variable
            if not 'outfile' in globals():
                outfile = input("\nPlease provide a json output filename, incl. name + ext (e.g. 'Results.json'): ")
                type = outfile.endswith('.json')
                while not type:
                    outfile = input("\nIncorrect file name/format. Please provide a json output filename, incl. name + ext (e.g. 'Results.json'): ")
                    type = outfile.endswith('.json')
            print('\n')

            if not 'aws_s3_bucket_upload' in globals():
                aws_s3_bucket_upload = input("\nPlease provide an S3 bucket to upload the output file to (to skip the upload press ENTER): ")
                if aws_s3_bucket_upload == '':
                    aws_s3_bucket_upload = 'skip_upload'
                    image_digest, image_name = runtime_get_image_digest(pod, namespace, container)
                if aws_s3_bucket_upload != 'skip_upload':
                    account = input("\nPlease provide an Anchore STIG UI account: ")
                    image_digest, image_name = runtime_get_image_digest(pod, namespace, container)
            print('\n')

            # Check for errors
            errout.close()
            if os.stat("./logs/err.txt").st_size != 0: 
                raise Exception("There was an error with the inputs provided. Please review the ./logs/err.txt file for more information.")
        except Exception as e:
            print('\n\n\u274C The following error has occurred:\n\n', e)
            exit()
        
        return image, pod, container, namespace, usecontext, cluster, outfile, aws_s3_bucket_upload, account, image_digest, image_name