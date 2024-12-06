## importing required libraries

#import docker
import yaml
import json
import time
import os
import requests
import argparse
import subprocess
from pathlib import Path
import sys
import pyfiglet

##importing required files

#import linguDetect/lingu_detect as ling
# from base_logger import logging
# from Config import Config

# import validation as Validation
# import utils as Utils
# import auth as Auth

from docker import errors
from bomancli.base_logger import logging
from bomancli.Config import Config

from bomancli import validation as Validation
from bomancli import utils as Utils
from bomancli import auth as Auth


parser = argparse.ArgumentParser(
	prog='bomancli',
	description='''
	#This is a CLI tool to communicate with Boman.ai SaaS server
	''',
	epilog='copyright (c) 2024 SUMERU'
	)


docker = Config.docker_client

### function to init the scan and will check the docker is in place
def init():
    logging.info('Intializing new scan .......')
    logging.info('Checking for availability of Docker in the Environment')
    try:
        #docker = docker.from_env()
        if docker.ping():
           logging.info('Docker is running in the Environment')
        else:
            logging.error('Unable to connect to docker, Please install docker in your environment')
    except Exception as e:
        logging.error('Docker not found in your machine, Pls install')
        #print(str(e))
        exit(3) ## docker/system error




### Run the scanners -- MM
### function to run the image -- MM ---------------------------------------------------------------------------

def runImage(data=None,type=None):

    if data is None:
        logging.error('Docker run: Unable to access the response data while running the scan')

    if type is None:
        logging.error('Docker run: Unable to access the response data while running the scan')



    #print(data['image'])
    docker_image = data['image']
    #lang= None
    tool_name =data['tool']
    command_line= data['command']
    output_file= data['output_file']
    will_generate_output = data['will_generate_output']
    tool_id= data['tool_id']
    scan_details_id= data['scan_details_id']
    conversion_required = data['conversion_required']
   

    #print(docker_image,tool_name,command_line,output_file,will_generate_output,tool_id,scan_details_id)

    if docker_image is None:
        logging.info('Docker run: Problem with running the scanner, image not specified.')
        exit(3) ## docker/system error

    try:

        uid = os.getuid()
        gid = os.getgid()


        if Config.jenkins == 'yes':
            logging.info('Jenkins configuration: Configuring user permission for jenkins environment')
            userid = 'root'
            Config.userid = userid
            logging.info('Jenkins configuration: Docker will run with USER:  %s',userid)
        else:
            logging.info('CI/CD configuration: Configuring user permission')
            userid= f"{uid}:{gid}"
            Config.userid = userid
            logging.info('CI/CD configuration: Docker will run with USER:  %s',userid)

    except:
        userid= 'root'

    try:
        # logging.info('environment var configured for the scan is not picked up by the cli')
        env = data['env']
        env_var =  env.split(',')
        logging.info('Docker Run: environment var configured for the scan is %s',str(env_var))
    except:
        env_var = ['test=test']
        logging.warning("Docker Run: environment var configuration failed or can't find the variables from sass")



    if type == 'SAST':
        if Config.sast_ignore:
            if Utils.copy_file('.bomanignore','.semgrepignore'):
                logging.info("SAST Configuration: Files and Folders to be ignored is added to .semgrepignore file")
            else:
                logging.error("SAST Configuration: Failed!!!. EXIT CODE:4(MISCONFIGURATION). Message: .bomanignore file was not found. Please check if you have '.bomanignore' file in the repository(Main Directory). As you have configured ignore files and folder")
                exit(4)
        target_file = Config.sast_target
        Utils.checkImageAlreadyExsist(docker_image)
        
        if (Config.sast_target is not None) and (Config.sast_target != "" ):
            Config.sast_build_dir = os.path.join(Config.sast_build_dir,Utils.remove_leading_slash(Config.sast_target)) 

        logging.info('SAST Docker: Running %s in the repository',tool_name)

        if data['dynamic_comment'] == 1:
            command_line = "% s" % command_line.format(target_file = target_file)
            #print(Config.sast_build_dir,command_line,docker_image)
            #command_line =  repr(command_line)


        detach = True if data['detach'] == 1 else False
        container_output = None
        try:

            if Config.jenkins == 'yes':

                logging.info('SAST Docker: Preparing %s scan for jenkins env with %s user ', tool_name , userid)    

                Config.build_dir = Config.sast_build_dir
                container_output = docker.containers.run(docker_image, command_line, volumes={Config.sast_build_dir: {
                                'bind': data['bind']}}, user=userid,detach=detach,environment=env_var)
                logging.info('SAST Docker: SUCCESS !!!. Message: %s Scan Completed',tool_name)

            else:    

                logging.info('SAST Docker: Preparing %s scan for non jenkins env with %s user ', tool_name ,userid)
                Config.build_dir = Config.sast_build_dir
                container_output = docker.containers.run(docker_image, command_line, volumes={Config.sast_build_dir: {
                            'bind': data['bind']}}, user=userid,detach=detach,environment=env_var)
                logging.info('SAST Docker: SUCCESS !!!. Message: %s Scan Completed',tool_name)

        except errors.ContainerError as exc:
            msg='\n The following error has been recorded while scanning SAST'
            Utils.logError(msg,str(exc))
            logging.error(f'SAST Docker: Failed !!!, Message: Some Error recorded while scanning {str(exc)}')
            Config.sast_scan_status = 'Failed'
            Config.sast_errors = f'Exit Status {exc.exit_status}:{str(exc)}]'



        try:
            if Config.sast_ignore:
                os.remove('.semgrepignore')
            if will_generate_output == 1:
                #logging.info('WILL GENERATE OUTPUT')
                if uploadReport(output_file,tool_name,tool_id,scan_details_id,'SAST'):
                    Config.sast_scan_status = 'Completed'
                    Config.sast_upload_status ='Completed'
                    Config.sast_message = 'Scan is completed'
                else:
                    Config.sast_upload_status ='Failed'
                    Config.sast_message ='Error occured while uploading the report, Please check the cli logs'
           
        except EnvironmentError as e:
            Config.sast_message = 'Error while uploading the report',tool_name,' [',str(e),']'
            logging.error(f'SAST UPLOAD: Failed !!!, Message: Some Error recorded while scanning {str(e)}')
            msg='Error while uploading the report'
            Utils.logError(msg,e)

    if type == 'DAST':

        Utils.checkImageAlreadyExsist(docker_image)
        logging.info('DAST Docker: Running %s on %s ',tool_name, Config.dast_target)
        logging.info('DAST Docker: Checking if Authenticated scan is configured...')

        is_dast_auth_available = 0
    
        if Config.dast_auth_present == True:
            logging.info('DAST Docker: Authenticated scan is configured')
            logging.info('DAST Docker: Fetching Authenticated scan config from SaaS')
            is_dast_auth_available = Utils.fetchDASTConfigFromSaas()


            if Config.zap_plan_config is None:
                logging.warning('DAST Docker: Failed !!!. Message: Failed to fetch Authenticated scan config from SaaS')
                logging.warning('DAST Docker: Proceeding with DAST Baseline Scan') 
                
            else:
                logging.info('Configured Auth method is : %s',str(Config.zap_plan_config['auth_method']))

                if Config.zap_plan_config['auth_method'] == 'form':
                    logging.info('DAST Docker:Creating Zap plan for form based authentication')
                    # if Config.custom_zap_plan_present:
                    #     logging. info('Custom Zap plan is configured %s',Config.zap_plan_config_file_name)   
                    # else:
                    Utils.createZapPlan(Config.zap_plan_config,output_file)          
                    #return 0
                elif Config.zap_plan_config['auth_method'] == 'json':
                    logging.info('DAST Docker: Creating Zap plan for json based authentication')
                    # if Config.custom_zap_plan_present:
                    #     logging.info('Custom Zap plan is configured %s',Config.zap_plan_config_file_name)   
                    # else:
                    Utils.createZapPlan(Config.zap_plan_config,output_file)     
                    #Utils.createZapPlan(Config.zap_plan_config,output_file)
                    logging.info('checking session management script configuration')

                    if Config.custom_zap_script_present:
                        logging.info('DAST Docker: Custom Zap script is configured %s',Config.zap_script_config_file_name)     
                    else:
                        logging.info('DAST Docker: Creating session management script for zap')
                        Utils.createZapScript(Config.zap_plan_config)
                          
                    #return 0
                else:
                    logging.info('DAST Docker: Creating Custom Zap script')
                    Utils.createZapPlan(Config.zap_plan_config,output_file)
                    logging.info('DAST Docker: Custom Zap script creation done')  

        else: 
            logging.info('DAST Docker: DAST Auth is not configured')       

        ## adding adv auth function here - MM
        if Config.dast_adv_auth_enabled == True: 
            ## Calling the advance auth fucntion to fetch required files
            ## logic to get files from saas and run the scan here by assigning all the required files to config
            logging.info('DAST Docker: Zap Advanced Authentication is configured')
            logging.info('DAST Docker: Fetching Zap config files from saas')
            Utils.fetch_zap_advance_config()

        #command_line = '-h '+Config.dast_target+' -maxtime 10 -o tmp/'+output_file
        #print(command_line_nikto)
        detach = True if data['detach'] == 1 else False

        if Config.sast_build_dir == None:
            Config.sast_build_dir = os.getcwd()+'/'

        if data['dynamic_comment'] == 1:
            
            target_url = Config.dast_target

            if Config.dast_type == "API":
                api_type = Config.dast_api_type
                command_line = "% s" % command_line.format(target_url = target_url, api_type=api_type)
            elif Config.dast_auth_present == True:
                if Config.custom_zap_plan_present:
                    Config.zap_plan_config_file_name = Config.zap_plan_config_file_name
                else:
                    Config.zap_plan_config_file_name = Config.zap_plan_config_file_name+'.yaml'
                command_line = "% s" % command_line.format(zap_plan_file = Config.zap_plan_config_file_name) 
            elif Config.dast_adv_auth_enabled == True:
                command_line = "% s" % command_line.format(zap_plan_file = Config.zap_plan_config_file_name)       
            else:
                command_line = "% s" % command_line.format(target_url = target_url)

            # logging.info('Command for zap is : %s',command_line)


            ## context file appending -- MM

   #         if Config.zap_context_configured == 'true':

    #            context_file_name = Config.zap_context_file_nmae
     #           context_command = Config.zap_context_cmd
      #          command_line = "% s" % command_line.format(context_file = context_file_name)



        ## part where running dast based on the given env i.e jenkins or non jenkins



        if Config.jenkins == 'yes':

            logging.info('Preparing %s scan for jenkins environment as user %s ',tool_name, userid)       

            try:
                Config.build_dir = Config.sast_build_dir
                container= docker.containers.run(docker_image, command_line, volumes={Config.sast_build_dir: {
                    'bind': data['bind'], 'mode': 'rw'}},user=userid,detach=detach)

                #print(output_file,toolname,tool_id,scan_details_id)
                logging.info('[SUCCESS]: %s Scan Completed',tool_name)
                Config.dast_scan_status ='Completed'
            except errors.ContainerError as exc:
                if exc.exit_status==2:
                    Config.dast_scan_status ='Completed'
                    logging.info(f'DAST Docker: SUCCESS!!! Message: Completed with warning: {str(exc)} for the tool %s',tool_name)
                    Config.dast_message = f"Completed with warning: {str(exc)}"
                elif exc.exit_status==0:
                    Config.dast_scan_status ='Completed'
                    logging.info(f'DAST Docker: SUCCESS!!! Message: Completed')
                else:
                    Config.dast_scan_status ='Failed'
                    logging.error('DAST Docker: Failed!!! Message: Error recorded while Scanning %s',tool_name)
                    Config.dast_errors = f'Exit Status {exc.exit_status}:{str(exc)}]'
                    msg='\n The following error has been recorded while scanning DAST'
                    Utils.logError(msg,str(exc))

        else:    

            logging.info('DAST Docker: Preparing %s scan for non-jenkins environment with user %s',tool_name, userid)  

            try:
                Config.build_dir = Config.sast_build_dir
                logging.info('DAST Docker: Command for running the scan %s',command_line)
                container= docker.containers.run(docker_image, command_line, volumes={Config.sast_build_dir: {
                   'bind': data['bind'], 'mode': 'rw'}},user=userid,detach=detach)

                #print(output_file,toolname,tool_id,scan_details_id)
                logging.info('DAST Docker: SUCCESS!!! Message: %s Scan Completed',tool_name)
                Config.dast_scan_status ='Completed'
            except errors.ContainerError as exc:
                if exc.exit_status==2:
                    Config.dast_scan_status ='Completed'
                    logging.info(f'DAST Docker: SUCCESS!!! Message: Completed with warning: {str(exc)} for the tool %s',tool_name)
                    Config.dast_message = f"Completed with warning: {str(exc)}"
                elif exc.exit_status==0:
                    Config.dast_scan_status ='Completed'
                    logging.info(f'DAST Docker: SUCCESS!!! Message: Completed')
                else:
                    Config.dast_scan_status ='Failed'
                    logging.error('DAST Docker: Failed!!! Message: Error recorded while Scanning %s',tool_name)
                    Config.dast_errors = f'Exit Status {exc.exit_status}:{str(exc)}]'
                    msg='\n The following error has been recorded while scanning DAST'
                    Utils.logError(msg,str(exc))


        try:
            if will_generate_output == 1:
                logging.info('DAST Docker: Uploading %s to the server',output_file)
                if uploadReport(output_file,tool_name,tool_id,scan_details_id,'DAST'):
                    Config.dast_scan_status = 'Completed'
                    Config.dast_upload_status ='Completed'
                    Config.dast_message = 'Scan is completed'
                else:
                    Config.dast_upload_status ='Failed'
                    Config.dast_message ='Error occured while uploading the report, Please check the cli logs'
            else:
                logging.error('DAST Docker: Failed!!! Message: Cant upload files to the server %s',tool_name)
                Config.dast_message ='Cant upload files to the server',tool_name

        except:
            logging.error('DAST Docker: Failed!!! Message: Error recorded while uploading the report %s',tool_name)
            Config.dast_message ='Error recorded while uploading the report of',tool_name

    if type == 'SCA':
        Utils.checkImageAlreadyExsist(docker_image)
        logging.info('Running %s',tool_name)
        try:
            if Config.sca_lang=="osv":
                if Config.sca_type == "directory":
                    target = Utils.remove_leading_slash(Config.sca_target)
                    Config.build_dir = Config.sca_build_dir
                    command_line = "% s" % command_line.format(target = './'+target)
                    container_output = docker.containers.run(docker_image, command_line, volumes={Config.sca_build_dir: {
                            'bind': data['bind']}}, user=uid)
                    logging.info('SCA Docker: SUCCESS!!! Message: %s Scan Completed',tool_name)
                else:
                    target = Utils.remove_leading_slash(Config.sca_target)
                    Config.build_dir = Config.sca_build_dir
                    command_line = "% s" % command_line.format(target ='/src/'+target)
                    container_output = docker.containers.run(docker_image, command_line, volumes={Config.sca_build_dir: {
                            'bind': data['bind']}}, user=uid)
                    logging.info('SCA Docker: SUCCESS!!! Message: %s Scan Completed',tool_name)
            else:
                if Config.sca_ignore:
                    Config.sca_exclude_files = Utils.read_bomanignore('.bomanignore')
                    logging.info("SCA Docker: excluded files or Folders ==> ", Config.sca_exclude_files )
                    if Config.sca_exclude_files:
                        command_line = f'{command_line} {Config.sca_exclude_files}'
                        logging.info('SCA Docker:  Command ==> %s',command_line)
                Config.build_dir = Config.sca_build_dir
                container_output = docker.containers.run(docker_image, command_line, volumes={Config.sca_build_dir: {
                        'bind': data['bind']}}, user=uid)
                logging.info('SCA Docker: SUCCESS!!! Message: %s Scan Completed',tool_name)           
            Config.sca_message ='SCA scan completed'
            Config.sca_scan_status ='Completed'
        except errors.ContainerError as exc:
            if tool_name =='OSV Scanner':
                if exc.exit_status==1:
                    Config.sca_message ='SCA scan completed'
                    Config.sca_scan_status ='Completed'
                    logging.info('SCA Docker: SUCCESS!!! Message: %s Scan Completed',tool_name)
                    logging.info(f'OSV: {exc.stderr}')
            else:
                logging.error('SCA Docker: Failed!!! Message: Some Error recorded while scanning %s',str(exc))
                msg='\n The following error has been recorded while scanning sca'
                Config.sca_scan_status ='Completed'
                Config.sca_errors =f'{str(exc)}]'
                Utils.logError(msg,str(exc))

        try:
            if will_generate_output == 1:
                logging.info('SCA Docker: Uploading %s to the server',output_file)
                if uploadReport(output_file,tool_name,tool_id,scan_details_id,'SCA'):
                    Config.sca_scan_status ='Completed'
                    Config.sca_upload_status = 'Completed'
                    Config.sca_message ='Scan Completed'
                else:
                    Config.sca_scan_status ='Failed'
                    Config.sca_upload_status = 'Failed'
                    Config.sca_message ='Error occured while uploading the report, Please check the cli logs'
            else:
                logging.error('SCA Docker: Failed!!! Message: Cant upload files to the server',tool_name)
                Config.sca_message ='Cant upload files to the server for SCA,Please check your directory for the files.'

        except EnvironmentError as e:
            logging.error('SCA Docker: Failed!!! Message: Error recorded while uploading the report %s',str(e))
            Config.sca_message ='Error recorded while uploading the report of SCA, Please check your directory for the files.'           ## need to change logic here -- MM
            msg = 'Error recorded while uploading the report'
            Utils.logError(msg,str(e))
            
    if type == 'container_scan':
        Utils.checkImageAlreadyExsist(docker_image)
        logging.info('CS Docker: Running %s',tool_name)
        
        try:
            if Config.con_scan_type == 'config':    
                command_line = "% s" % command_line.format(target = os.path.join('/src',Utils.remove_leading_slash(Config.con_scan_target)))
            else:
                command_line = "% s" % command_line.format(target = Config.con_scan_target)
            
            logging.info(f"CS Docker: command ==> {command_line}")    
            Config.build_dir = Config.con_scan_build_dir
            container_output = docker.containers.run(docker_image, command_line, volumes={Config.con_scan_build_dir: {
                        'bind': data['bind']}}, user=uid)
            logging.info('CS Docker: SUCCESS!!! Message: %s Scan Completed',tool_name)
            Config.con_scan_message ='Container Scan completed'
            Config.con_scan_status ='Completed'
        except errors.ContainerError as exc:
            logging.error('CS Docker: Failed!!! Message:Some Error recorded while scanning %s',str(exc))
            msg='\n The following error has been recorded while scanning Container'
            Config.con_scan_status ='Failed'
            Config.con_scan_errors =f'{str(exc)}]'
            Utils.logError(msg,str(exc))
        
        try:
            if will_generate_output == 1:
                logging.info('CS Docker: Uploading %s to the server',output_file)
                if uploadReport(output_file,tool_name,tool_id,scan_details_id,'container_scan'):
                    Config.con_scan_status ='Completed'
                    Config.con_scan_upload_status = 'Completed'
                    Config.con_scan_message ='Scan Completed'
                else:
                    Config.con_scan_status ='Failed'
                    Config.con_scan_upload_status = 'Failed'
                    Config.con_scan_message ='Error occured while uploading the report, Please check the cli logs'
            else:
                logging.error('CS Docker: Failed!!! Message: Cant upload files to the server',tool_name)
                Config.con_scan_message ='Cant upload files to the server for Container Scan,Please check your directory for the files.'

        except EnvironmentError as e:
            logging.error('CS Docker: Failed!!! Message: Error recorded while uploading the report %s',str(e))
            Config.con_scan_message ='Error recorded while uploading the report of Container Scan, Please check your directory for the files.'           ## need to change logic here -- MM
            msg = 'Error recorded while uploading the report'
            Utils.logError(msg,str(e))    
        
    if type == 'sbom':
        Utils.checkImageAlreadyExsist(docker_image)
        logging.info('Running %s',tool_name)
        
        try:
            Config.build_dir = Config.sbom_build_dir
            command_line = "% s" % command_line.format(target = 'src/')
            container_output = docker.containers.run(docker_image, command_line, volumes={Config.sbom_build_dir: {
                        'bind': data['bind']}}, user=uid)
            logging.info('SBOM Docker: SUCCESS!!! Message: %s Scan Completed',tool_name)
            Config.sbom_message ='SBOM scan completed'
            Config.sbom_scan_status ='Completed'
        except errors.ContainerError as exc:
           logging.error('SBOM Docker: Failed!!! Message: Some Error recorded while scanning %s',str(exc))
           msg='\n The following error has been recorded while scanning sca'
           Config.sbom_scan_status ='Completed'
           Config.sbom_errors =f'Exit Status {exc.exit_status}:{str(exc)}]'
           Utils.logError(msg,str(exc))
           
        try:
            if will_generate_output == 1:
                logging.info('SBOM Docker: Uploading %s to the server',output_file)
                if uploadReport(output_file,tool_name,tool_id,scan_details_id,'sbom'):
                    Config.sbom_scan_status ='Completed'
                    Config.sbom_upload_status = 'Completed'
                    Config.sbom_message ='Scan Completed'
                else:
                    Config.sbom_scan_status ='Failed'
                    Config.sbom_upload_status = 'Failed'
                    Config.sbom_message ='Error occured while uploading the report, Please check the cli logs'
            else:
                logging.error('SBOM Docker: Failed!!! Message: Cant upload files to the server',tool_name)
                Config.sbom_message ='Cant upload files to the server for SBOM,Please check your directory for the files.'

        except EnvironmentError as e:
            logging.error('SBOM Docker: Failed!!! Message: Error recorded while uploading the report %s',tool_name)
            logging.error('%s',str(e))
            Config.sbom_message ='Error recorded while uploading the report of SBOM, Please check your directory for the files.'           ## need to change logic here -- MM
            msg = 'Error recorded while uploading the report'
            Utils.logError(msg,str(e))    

    if type == 'iac':
        Utils.checkImageAlreadyExsist(docker_image)
        logging.info('Running %s',tool_name)
        
        try:
            command_line = "% s" % command_line.format(target = os.path.join('/src',Utils.remove_leading_slash(Config.iac_scan_target)))   
            Config.build_dir = Config.iac_scan_build_dir
            container_output = docker.containers.run(docker_image, command_line, volumes={Config.iac_scan_build_dir: {
                        'bind': data['bind']}}, user=uid)
            logging.info('IaC Docker: SUCCESS!!! Message: %s Scan Completed',tool_name)
            Config.iac_scan_message ='IaC Scan completed'
            Config.iac_scan_status ='Completed'
        except errors.ContainerError as exc:
            if exc.exit_status in Config.iac_valid_exit_status:
                Config.iac_scan_message ='IaC scan completed'
                Config.iac_scan_status ='Completed'
                logging.info('IaC Docker: SUCCESS!!! Message: %s Scan Completed',tool_name)
                logging.info(f'IaC: {exc.stderr}')
            else: 
                logging.error('IaC Docker: Failed!!! Message: Some Error recorded while scanning %s',str(exc))
                msg='\n The following error has been recorded while scanning IaC'
                Config.iac_scan_status ='Failed'
                Config.iac_scan_errors =f'Exit Status {exc.exit_status}:{str(exc)}]'
                Utils.logError(msg,str(exc))
        
        try:
            if will_generate_output == 1:
                logging.info('IaC Docker: Uploading %s to the server',output_file)
                if uploadReport(output_file,tool_name,tool_id,scan_details_id,'iac'):
                    Config.iac_scan_status ='Completed'
                    Config.iac_scan_upload_status = 'Completed'
                    Config.iac_scan_message ='Scan Completed'
                else:
                    Config.iac_scan_status ='Failed'
                    Config.iac_scan_upload_status = 'Failed'
                    Config.iac_scan_message ='Error occured while uploading the report, Please check the cli logs'
            else:
                logging.error('IaC Docker: Failed!!! Message: Cant upload files to the server',tool_name)
                Config.iac_scan_message ='Cant upload files to the server for IaC Scan,Please check your directory for the files.'

        except EnvironmentError as e:
            logging.error('IaC Docker: Failed!!! Message: Error recorded while uploading the report %s',str(e))
            Config.iac_scan_message ='Error recorded while uploading the report of IaC Scan, Please check your directory for the files.'           ## need to change logic here -- MM
            msg = 'Error recorded while uploading the report'
            Utils.logError(msg,str(e))    
        

#### function to upload the test report to the server with other data -- MM ------------------------------------
def uploadReport(filename,toolname,tool_id,scan_details_id,type):

    logging.info('Uploading %s report with filename: %s', toolname,filename)
    if True:
        #build_dir = '/home/boxuser/box/trainingdata/repos/youtube-dl/'
        #print(Config.sast_build_dir+filename)
        #files = open(build_dir+filename)

        try:

            if type == 'SAST':
                message = Config.sast_message
                errors = Config.sast_errors
            elif type == 'DAST':
                message = Config.dast_message
                errors = Config.dast_errors
            elif type == 'SCA':
                message = Config.sca_message
                errors = Config.sca_errors
            elif type =='SS':
                message = Config.secret_scan_message
                errors = Config.secret_scan_errors
            elif type =="container_scan":
                message = Config.con_scan_message
                errors = Config.con_scan_errors
            elif type =="sbom":
                message = Config.sbom_message
                errors = Config.sbom_errors
            elif type =="iac":
                message = Config.iac_scan_message
                errors = Config.iac_scan_errors
        except:
            message = 'NA'
            errors = 'NA'




        try:
            logging.info('fetching the %s file from the directory %s',filename,Config.build_dir)
            ##path = '/home/boxuser/box/Vuln-code/boman_njsscan.json'


            # print(str(Config.build_dir))
            # print(str(filename))

            data_folder = Path(str(Config.build_dir))

            path = data_folder / str(filename)
           
            with open(path) as f: 
                f.seek(0)
                data = json.load(f)


        except EnvironmentError as e:
            logging.error('Error while fetching the output file from the directory')
            logging.error('%s',str(e))
            msg = 'Error while fetching the output file from the directory'
            Utils.logError(msg,str(e))
            values = {'tool_name': toolname, 'time': time.time(),'scan_token':Config.scan_token, 'app_token':Config.app_token,'customer_token':Config.customer_token,'tool_id':tool_id,'scan_details_id':scan_details_id,"tool_results":None,"message":message,"errors":errors,"app_loc":Config.app_loc}
            url = Config.boman_url+"/api/app/upload" 
        # with open(path) as f: 
        #     file_obj = f
            r = requests.post(url,json=values)
            return 0

        tool_output = json.dumps(data, ensure_ascii=False, indent=4)
    
        # files = {'upload_file': open(path,'rb')}
        
        logging.info('output size of file is %s', sys.getsizeof(tool_output))
        values = {'tool_name': toolname, 'time': time.time(),'scan_token':Config.scan_token, 'app_token':Config.app_token,'customer_token':Config.customer_token,'tool_id':tool_id,'scan_details_id':scan_details_id,"tool_results":tool_output,"message":message,"errors":errors,"app_loc":Config.app_loc}
        url = Config.boman_url+"/api/app/upload" 
        # with open(path) as f: 
        #     file_obj = f
        r = requests.post(url,json=values)
        #print(r.status_code)
        if r.status_code == 200:
            logging.info('[COMPLETED]: %s Report uploaded Successfully! Report Name: %s',toolname,filename)
            logging.info('Removing the result file')
            os.remove(path)
            return 1
        elif r.status_code == 401 :
            logging.error('Unauthorized Access while uploading the results. Please check the app/customer tokens')
            exit(2)  ## Auth error
        else:
            logging.error('Problem While uploading the results.')
            logging.error('response code is %s',r.status_code)
            return 0
    else:
       logging.error(toolname,' Report cant be uploaded filename: %s',filename)
       return 0 ## need to write a logic here



   
    return 1




## function for seceert scan using trufflehog
def initSecertScan(path,data):

    build_dir = path
    command_line_truffle = data[0]['command']
    image_name= data[0]['image']
    tool_name = data[0]['tool']
    bind_dir = data[0]['bind']
    tool_id = data[0]['tool_id']
    scan_details_id = data[0]['scan_details_id']
    Utils.checkImageAlreadyExsist(image_name)


    try:
        logging.info('Running Secert Scanning on the repository')
        container = Config.docker_client.containers.run(image_name, command_line_truffle, detach=True,volumes={build_dir: {
                    'bind': bind_dir}})
        op = []
        for iteration_main,line in enumerate(container.logs(stream=True)):
            try:
                op.append(json.loads(line.strip()))
                #print(op[iteration_main]['stringsFound'])
                for iteration,key in enumerate(op[iteration_main]['stringsFound']):
                   #print(key)
                    op[iteration_main]['stringsFound'][iteration] = Utils.masker(key)

            except:
                logging.error('Some Findings from the trufflehog is unrecognisble.Skiping them.')
                Config.secret_scan_status ='Completed'
                Config.secret_scan_message ='Some Findings from the trufflehog is unrecognisble.'
                break


        logging.info('[SUCCESS]: Secert Scanning Completed ')
    except errors.ContainerError as exc:
        Config.secret_scan_errors = str(exc)
        logging.error('Error Occured while running Trufflehog on the repository')
        logging.error('%s',str(exc))
        msg='\n The following error has been recorded while scanning Trufflehog'
        Utils.logError(msg,str(exc))

    try:
        file_name = data[0]['output_file']
        Config.build_dir = Config.sast_build_dir
        path = Config.sast_build_dir+file_name
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(op, f, ensure_ascii=False, indent=4)

        if uploadReport(file_name,tool_name,tool_id,scan_details_id,'SS'):
            logging.info('[COMPLETED]: Secret Scan report Uploaded')
            Config.secret_scan_status ='Completed'
            Config.secret_scan_upload_status = 'Completed'
            Config.secret_scan_message = 'Scan Completed'
        else:
            logging.error('Error Occured while uploading report to boman.ai server. Please contact admin.')
    except Exception as error:
         logging.error(' Error Occured while generating report for secert scan')

    return True



## filtering the vuln and exit code

def exitFunction():
    scan_token = Config.scan_token
    app_token = Config.app_token
    customer_token =  Config.customer_token

    logging.info('Summary: Fetching Vulnerabilities reported by the tools')
    url = Config.boman_url+"/api/vuln/get"
    values = {'app_token':app_token, 'scan_token':scan_token, 'customer_token':customer_token}
    try:
        vuln = {"LOW":0,"MEDIUM":0,"HIGH":0,"CRITICAL":0}
        x = requests.post(url,json=values)  


        response = x.json()

        if response['status'] == True:
            logging.info('Summary: Analyzing the vulnerabilities found')
            for data in response['data'] :
                vuln[data['_id']] = data['count']

            Config.low_count = vuln['LOW']
            Config.medium_count = vuln['MEDIUM']
            Config.high_count = vuln['HIGH']
            Config.critical_count = vuln['CRITICAL'] 
           
            logging.info('Summary: Analyzing Vulnerabitlites Done')

        else:
            logging.info('Summary: Error Analyzing Vulnerabitlites.')



    except requests.ConnectionError as e:
        
        logging.error(f"Connection Error: Can't connect to the Server, Please check your Internet connection. Error: {e}")
        exit(1) #server/saas error
    





#main fucntion where all the actions have been initiated
def main():
    init()
    Utils.testServer()
    
    if (Config.app_token is not None) and (Config.customer_token is not None):
        logging.info("Authorization: Tokens found in CLI Arguments")
        Auth.new_authorize()
        logging.info("Authorization: Successfull !!!")
        logging.info("Scan Configuration: Fetching configuration from SaaS")
        Validation.tool_configuration_validation()
        logging.info("Scan Configuration: Successfull !!!") 
    else:
        logging.info(f"Scan Configuration: Fetching configuration from {Config.boman_config_file}")
        Validation.yamlValidation()
        logging.info("Scan Configuration: Successfull !!!")
        if Config.secret_scan_present == True or Config.sast_present is True or Config.dast_present is True or Config.sca_present is True or Config.con_scan_present is True or Config.sbom_present or Config.iac_scan_present:
            Utils.testServer()
        else:
            content = Auth.authorize()
            logging.info('Nothing configured to be scan.')
            return 0
        logging.info(f"Authorization: Tokens found in {Config.boman_config_file}")
        content = Auth.authorize()
        logging.info("Authorization: Successfull !!!")
    global scan_token

    if Utils.isGitDirectory(Config.sast_build_dir):
        logging.info('Git Details: Git repository is found in the directroy')
        Config.git_present = True
        logging.info('Git Details: Fetching git details')
        git_data = Utils.getGitDetails()
        logging.info(f"Git Details: Successfull !!!")
        Config.git_branch =git_data['branch']
        Config.git_repo =git_data['repo']
        
        # try:   # Language detection not in use
        #     logging.info('Language info: Detecting languages in repository')
        #     loc = Utils.getLoc()
        #     logging.info(f"Language Info: Successfull !!!")
        # except Exception as e:
        #     logging.error('some error occured while detecing languages: %s',e)
        #     loc = 0    



            
    else:
        logging.warning('Git Details: Git repository not found in the directroy %s',Config.sast_build_dir)


    scan_token = Config.scan_token


    if Config.sast_present is True:


        logging.info('SAST: Preparing SAST Scan')
        logging.info('SAST: Working directory is %s',Config.sast_build_dir)
        if Config.sast_lang is None:
            #findLang()
            logging.error('SAST: Language was not defined. Exiting')
            exit(4) ## misconfig error



        for data in Config.sast_response:

            if data['scan_status'] == 2 :   
                logging.warning('SAST: No Configuration found from SaaS')    
                logging.info('SAST: Ignoring Scan')
            else:
                runImage(data=data,type='SAST')
                logging.info("SAST: Successfull !!!")

    else:
        logging.warning('SAST: Ignoring Scan. Message: Not Configured')


    if Config.dast_present is True:
        logging.info('DAST: Preparing scan')

        if Utils.testDastUrl(Config.dast_target):

           for data in Config.dast_response:

                if data['scan_status'] == 2 :   
                    logging.warning('DAST: No Configuration found from SaaS')    
                    logging.info('DAST: Ignoring Scan')
                else:
                    runImage(data=data,type='DAST')
                    logging.info("DAST: Successfull !!!")
           # runImage(imagename= content['data']['dast']['tool_2']['image'], toolname= content['data']['dast']['tool_2']['tool'],type='DAST',output_file=content['data']['dast']['tool_2']['output_file'],tool_id=content['data']['dast']['tool_2']['tool_id'], scan_details_id=content['data']['dast']['scan_details_id'])


        else:
            logging.error(f'DAST: Failed !!!. Message: The target({Config.dast_target}) is unreachable')
            Config.dast_scan_status = 'Failed'
            Config.dast_upload_status ='NA'
            Config.dast_message = f'DAST: Failed. The target({Config.dast_target}) is unreachable'


    else:
        logging.info('DAST: Ignoring scan. Message: Not Configured')


    if Config.sca_present is True:
        logging.info('SCA: Preparing scan')

        
        for data in Config.sca_response:

            if data['scan_status'] == 2 :   
                logging.info('SCA: No Configuration found from SaaS')    
                logging.info('SCA: Ignoring Scan')
            else: 
                runImage(data=data,type='SCA')
                logging.info("SCA: Successfull !!!")
            
    else:
        logging.info('SCA: Ignoring scan. Message: Not Configured')
        
    if Config.secret_scan_present == True:

        if Utils.isGitDirectory(Config.sast_build_dir):
            logging.info('Secret Scan: Preparing Scan')
            for data in Config.secret_scan_response:
                initSecertScan(Config.sast_build_dir,data=Config.secret_scan_response)
                logging.info("Secret Scan: Successfull !!!")
                
        else:
            logging.error('Secret Scan: Failed !!!. Message: The Directory is not Git directory %s',Config.sast_build_dir)
            Config.secret_scan_status = 'Failed'
            Config.secret_scan_upload_status ='NA'
            Config.secret_scan_message = f'Secret Scan: Failed. The Directory is not Git directory {Config.sast_build_dir}'
            logging.warning('Secret Scan: Ignoring scan')
    else:
        logging.warning('Secret Scan: Ignoring scan. Message: Not Configured')
        
    if Config.con_scan_present is True:
        logging.info("Container Scan: Preparing scan")
        
        for data in Config.con_scan_response:

            if data['scan_status'] == 2 :   
                logging.info('Container Scan: No Configuration found from SaaS')    
                logging.warning('Container Scan: Ignoring Scan')
            else:
                runImage(data=data,type='container_scan')
    else:
        logging.warning('Container Scan: Ignoring scan. Message: Not Configured')
        
    if Config.sbom_present is True:
        logging.info("SBOM: Preparing requirements")
        
        for data in Config.sbom_response:

            if data['scan_status'] == 2 :   
                logging.info('SBOM: No Configuration found from SaaS')    
                logging.warning('SBOM: Ignoring')
            else:
                runImage(data=data,type='sbom')
    else:
        logging.warning('SBOM: Ignoring. Message: Not Configured')
        
    if Config.iac_scan_present is True:
        logging.info("IaC: Preparing Scan")
        
        for data in Config.iac_scan_response:

            if data['scan_status'] == 2 :   
                logging.info('IaC: No Configuration found from SaaS')    
                logging.warning('IaC: Ignoring Scan')
            else:
                runImage(data=data,type='iac')
    else:
        logging.warning('IaC: Ignoring scan. Message: Not Configured')
    
    exitFunction()
    return 1

def default():

    parser.add_argument('-a','--action',default='init',help="Action arugment, you need to pass the value for action (eg: test-saas, test-docker, run , test-yaml, version, check-user)")
    parser.add_argument('-u','--url',default='https://dashboard.boman.ai',help="Provide the URL of the boman saas (eg: On-Prem URL)")
    parser.add_argument('-v','--version',default='show',help="Will show the version of boman-cli tool",action='store_true')
    parser.add_argument('-fb','--failBuild',default='pass',help="This is for failing the boman scan based on the severity of the findings, pass -fb high for failing the build when any high issue is found, similarly you can pass medium,low")
    parser.add_argument('-cicd','--cicd',default='other',help="Pass jenkins if the cicd you are using is jenkins (value: jenkins). if your are using non-jenkins cicd you can ignore this option.")
    parser.add_argument('-at','--appToken',default=None,help="Pass your app token for authenticating the app")
    parser.add_argument('-ct','--cusToken',default=None,help="Pass your customer token for authenticating the license")
    #parser.add_argument('-check-docker',help='Check you docker is present in your system is compatable to run the boman.ai')
    parser.add_argument('-config','--config',default='boman.yaml',help="Pass the file name if you have any custom file name for the boman config. eg:boman-prod.yaml")
    # parser.add_argument('-custom_dast_auth_config','--custom_dast_auth_config',default=False,help="Pass True in the case of custom zap auth scan, this requires , -zap_auth_method , -zap_plan and -zap_session_script (incase of json auth method)")
    # parser.add_argument('-zap_auth_method','--zap_auth_method',default='form',help="Pass the auth method of DAST(zap) scan, supported method [form, json]. default value is form based")
    parser.add_argument('-zap_plan','--zap_custom_plan',default='boman_zap_auth_plan.yaml',help="Pass the file name if you have any custom zap context plan. eg:custom-zap-plan.yaml")
    parser.add_argument('-zap_session_script','--zap_custom_session_script',default='session_management.js',help="Pass the file name if you have any custom zap session script file name. eg:custom-script.js")
    # parser.add_argument('-uid','--user_id',default='1000:1000',help="[internal] Pass the custom userid:groupid incase the lingu detec function is failed")
    args = parser.parse_args()

    # if len(sys.args) == 1:
    #     # display help message when no args are passed.
    #     print('Welcome to Boman CLI, pass bomancli --help to view the commands args ')
    #     exit(1)

    if args.url == 'https://dashboard.boman.ai':
        Config.boman_url = "https://dashboard.boman.ai"
    else:
        Config.boman_url = args.url   


    ## cicd argument

    if args.cicd == 'jenkins':
        ##logging.info('jenkins is choosen')
        Config.jenkins = 'yes'
    else:
        ###logging.info('jenkins is not choosen')
        Config.jenkins = 'no'  

    ## lingu user id set
    # if args.user_id == '1000:1000':
    #     ##logging.info('jenkins is choosen')
    #     Config.lingu_user = '1000:1000'
    # else:
    #     ###logging.info('jenkins is not choosen')
    #     Config.lingu_user = args.user_id  


    if args.config == 'boman.yaml':
        ##logging.info('jenkins is choosen')
        Config.boman_config_file = 'boman.yaml'
    else:
        ###logging.info('jenkins is not choosen')
        Config.boman_config_file = args.config


##custom zap auth method

    # if args.zap_auth_method == 'form':
    #     Config.zap_custom_auth_method = 'form'
    # elif args.zap_auth_method == 'json':
    #     Config.zap_custom_auth_method = 'json'
    # else:
    #     Config.zap_custom_auth_method = 'form'




## custom script for zap auth scan automation
    if args.zap_custom_plan == 'boman_zap_auth_plan.yaml':
        Config.zap_plan_config_file_name = 'boman_zap_auth_plan.yaml'
        #exit(1)
    else:
        logging.info('custom zap contct plan option is choosen')
        Config.custom_zap_plan_present = True
        Config.zap_plan_config_file_name = args.zap_custom_plan
        #exit(1)

    ## custom script for zap auth scan automation
    if args.zap_custom_session_script == 'session_management.js':
        Config.zap_script_config_file_name = 'session_management.js'
    else:
        ###logging.info('jenkins is not choosen')
        Config.custom_zap_script_present = True
        Config.zap_script_config_file_name = args.zap_custom_session_script
        
    #Auth token
    if args.appToken is not None:
        Config.app_token = args.appToken
    elif os.path.isfile(Config.boman_config_file):
        logging.info(f"Authorization Config: Found {Config.boman_config_file} config file and switching to CLI config")
    else:
        logging.error(f"Authorization Config: Failed !!!, Exit Code: 4 (Misconfiguration/Validation). Message: The {Config.boman_config_file} file is not found and tokens were not found in cli arguments as well")
        exit(4) #validation error
        
    if args.cusToken is not None:
        Config.customer_token = args.cusToken
    elif os.path.isfile(Config.boman_config_file):
        logging.info(f"Found {Config.boman_config_file} config file and and switching to CLI config")
    else:
        logging.error(f"Authorization Config: Failed !!!, Exit Code: 4 (Misconfiguration/Validation). The {Config.boman_config_file} file is not found and tokens were not found in cli arguments as well")
        exit(4) #validation error
## auth method args validation

    # if args.custom_dast_auth_config == True:
    #     if Config.zap_custom_auth_method == 'json':
    #         if Config.custom_zap_plan_present & Config.custom_zap_script_present:
    #             Config.dast_auth_present == True
    #             Config.custom_zap_plan_present = True
    #         else:
    #             logging.error('Zap auth method "json" needs both plan and session script files')
    #             exit(4)    


        if Config.zap_custom_auth_method == 'form':
            if Config.custom_zap_plan_present :
                Config.dast_auth_present == True
                Config.custom_zap_plan_present = True
            else:
                logging.error('Zap auth method "form" needs plan file')
                exit(4)
    






## Action argument
    tool_name = pyfiglet.figlet_format(f"Boman CLI {Config.version}",justify="center")
    logging.info(f"\n\n{tool_name}")
    if args.action == 'init':
        print(f'Welcome to Boman CLI {Config.version}. Pass bomancli --help to view the commands args')
        exit(0)
    elif args.action =='run':
        logging.info("\n\n #################################### -  BOMAN Scanner Initiated - #################################### \n\n")
        if main():
            logging.info('################################ BOMAN Scanning Done ################################')
            logging.info('#####################################################################################')
            Utils.showSummary()
            Utils.uploadLogs()

           ## checking the failbuild argument
            if args.failBuild == 'fail':
                total_vuln = Config.high_count + Config.medium_count + Config.low_count + Config.critical_count
                if total_vuln > 0:
                    exit(-1)
                else:
                    exit(0)    

            elif args.failBuild == 'high':
                if Config.high_count > 0 or Config.critical_count > 0:
                    exit(-1)
                else:
                    exit(0)     

            elif args.failBuild == 'medium':
                if Config.medium_count > 0 or Config.high_count > 0:
                    exit(-1)
                else:
                    exit(0)    

            elif args.failBuild == 'low':
                if Config.low_count > 0 or Config.medium_count > 0 or Config.high_count > 0:
                    exit(-1)
                else:
                    exit(0)  

            elif args.failBuild == 'critical':
                if Config.critical_count > 0:
                    exit(-1)
                else:
                    exit(0)                     


            else:
                exit(0)  

            
        else:
            logging.info('All tasks done')
            exit(0)
           
    elif args.action =='test-saas':
        Utils.testServer()
        exit(0)
    elif args.action =='test-docker':
        Utils.testDockerAvailable()
        exit(0)
    elif args.action =='test-yaml':
       Validation.yamlValidation()
       exit(0)

    elif args.action == 'version':
       print('boman-cli-uat',Config.version)
       exit(0)
    elif args.action == 'check-user':
       
       print('User:', os.getlogin())
       print('UID:', os.getuid())
       print('GID:', os.getgid())
       print('------------------')
       current_work_dir = os.getcwd()+'/'
       print('Access for :', current_work_dir)
       print('READ:', os.access(current_work_dir, os.R_OK))
       print('WRITE:',os.access(current_work_dir, os.W_OK))
       print('EXECUTION:',os.access(current_work_dir, os.X_OK))
       print('WRITE FILE IN DIR:',os.access(current_work_dir, os.X_OK | os.W_OK))
       print('------------------')
       exit(0)   

    else:
        print('Welcome to Boman CLI',Config.version,',pass bomancli --help to view the commands args ')
        exit(0)

## version argument 
    if args.version == 'show':
        print(f'Welcome to Boman CLI ({Config.version})')



## starting the cli



default()
