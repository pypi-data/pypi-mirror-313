# from base_logger import logging
# from Config import Config
# import utils as Utils

from bomancli import utils as Utils
from bomancli.base_logger import logging
from bomancli.Config import Config


import yaml
import json
import requests
import os

logging.basicConfig(format='%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')


#### read the input from the yaml file -- MM ------------------------------------------------------------

def yamlValidation():

    logging.info('Validation: Finding boman.yaml file')

    #Config.boman_config_file 

    try: 
        with open(Config.boman_config_file, 'r') as file:
            Config.config_data = yaml.safe_load(file)    
        logging.info('Validation: SUCCESS!!! Message: Config yaml file found')    
    except:
        
        logging.error('Validation: FAILED!!! exit code: 4(CONFIG ERROR) Message: No config yaml file found')
        exit(4) ## validation error 

    logging.info('Validation: Parsing and Validating the config yaml file')
   


    try:
        Config.config_data['Auth']
        if Config.config_data['Auth'] != '':
            Config.app_token = Config.config_data['Auth']['project_token']
            Config.customer_token =Config.config_data['Auth']['customer_token']


    except KeyError:
        logging.error('Validation: FAILED!!! exit code: 2(AUTH ERROR) Message: Project and Customer token is mandatory to run the scan. Refer the documentation.')
        exit(2) #AUTH error    


    try: 

        if  Config.config_data['SAST'] != '':
            Config.sast_lang = Config.config_data['SAST']['language'].split(",") ## comma sperated if mulitple
            
            Config.sast_present = True
            Config.sast_message = 'SAST is properly configured'
            logging.info('Validation: SAST is properly configured with %s and ready to scan',Config.sast_lang)

            try:
                logging.info('Validation: choosing the sast working directory')
                Config.sast_build_dir  = Config.config_data['SAST']['work_dir']
            except KeyError: 
                logging.info('Validation: work dir not specified in config, choosing the default sast working directory')
                Config.sast_build_dir = os.getcwd()+'/'
                
            try:
                logging.info('Validation: Ignoring file and folder check')
                Config.sast_ignore =  Config.config_data['SAST']['ignore_files']
            except KeyError: 
                logging.info('Validation: ignore_files config was not found')
                

            #logging.info('snyk is choosen, and the env var declared was %s', str('s'))


            



        if 'java' in Config.sast_lang:

            try:
                Config.sast_target =  Config.config_data['SAST']['target']
            except KeyError: 
                logging.error('Validation: FAILED!!! Java requires a target file to be mentioned in the boman.yaml file. refer the documentation')
                Config.sast_present = False       
                Config.sast_message = 'SAST is not configured properly, Java requires a target file to be mentioned in the boman.yaml file. refer the documentation'    
        


        # if 'python-snyk' in Config.sast_lang:

        #         try:
        #             Config.sast_env = Config.config_data['SAST']['env']
        #             logging.info('snyk is choosen, and the env var declared was %s', str(Config.sast_env))
        #         except KeyError: 
        #             logging.error('Snyk requires a enviromenet var for snyk auth token to be mentioned in the boman.yaml file. refer the documentation')
        #             Config.sast_present = False 

        
    except KeyError:    
        Config.sast_present = False
        Config.sast_message = 'SAST was not properly defined in the config, Please check your boman.yaml file.'
        logging.warning('Validation: SAST was not properly defined in the config file')
        logging.warning('Validation: Ignoring SAST, Please provide all mandatory inputs incase you to run SAST scan.')
        

    
    ## DAST

    try: 
        Config.dast_target = Config.config_data['DAST']['URL']
        Config.dast_type = Config.config_data['DAST']['type']

        Config.dast_present = True

        try:        
            if Config.config_data['DAST']['auth'] == 'yes':
                Config.dast_auth_present = True
        except KeyError: 
            Config.dast_auth_present = False 


        if Utils.testDastUrl(Config.dast_target):
            logging.info('Validation: DAST is properly configured and ready to scan')
            
            if Config.dast_type == 'API':
                try:  
                    logging.info('Validation: DAST is configured for API scan, checking API type.')    
                    Config.dast_api_type = Config.config_data['DAST']['api_type']
                    
                except KeyError:
                    logging.info('Validation: DAST API type is not given, proceeding with default value: OPENAPI')
                    Config.dast_api_type = 'openapi'  


        else:    
            logging.info('Validation: DAST target is not reachable, ignoring DAST scan')
            Config.dast_present = False
            Config.dast_message = 'DAST target is not reachable. DAST scan was ignored'
                
    except KeyError:    
        Config.dast_present = False
        Config.dast_message = 'DAST was not properly defined in the config.'
        logging.warning('Validation: DAST was not properly defined in the config.')
        logging.warning('Validation: Ignoring DAST, Please provide all mandatory inputs incase you like to run DAST scan.')
        

        
               


    ## SCA

    try: 
        if  Config.config_data['SCA'] != '':
            Config.sca_lang = Config.config_data['SCA']['language'].split(",") ## comma sperated if mulitple
            
            Config.sca_present =  True
            Config.sca_build_dir = os.getcwd()+'/'
            
            try:
                logging.info('Configuring scan type for SCA')
                Config.sca_type = Config.config_data['SCA']['type']
                logging.info(f'Validation: Scan type configured for SCA: {Config.sca_type}')
            except KeyError: 
                logging.warning('Validation: Scan type for SCA not found. SCA will run with default scan type directory')
                Config.sca_type = "directory" # other options sbom and lockfile

            #depricated

            # try:
            #     logging.info('Configuring work directory for SCA')
            #     Config.sca_build_dir = Config.config_data['SCA']['work_dir']
            #     logging.info('Work directory found for SCA')
            # except KeyError: 
            #     logging.info('No work directory for SCA. Default work directory is set')
            #     ##after sbom and lockfile type check
            #     Config.sca_build_dir = os.getcwd()+'/'
                
            try:
                logging.info('Validation: Ignoring file and folder check')
                Config.sca_ignore =  Config.config_data['SCA']['ignore_files']
            except KeyError: 
                logging.warning('Validation: ignore_files config was not found')    
                
            try:
                logging.info('Validation: Configuring target for SCA')
                Config.sca_target = Config.config_data['SCA']['target']
                logging.info(f'Validation: Target configured for SCA: {Config.sca_target}')
            except KeyError: 
                if Config.sca_type == "directory":
                    logging.warning(f'Validation: Target for SCA not found. SCA will run with default scan type directory: {Config.sca_build_dir}')
                    # Config.sca_target = Config.sca_build_dir
                else:
                    logging.error("Validation: Failed !!! exit code: 4(CONFIG ERROR) Message: Target parameter missing. Target parameter is required for sbom or lockfile type")
                    exit(4)
                             
            Config.sca_message ='SCA is properly configured'
            logging.info('Validation: SCA is properly configured and ready to scan')    
    except KeyError:    
        Config.sca_present =  False
        Config.sca_message ='SCA was not properly defined in the config'
        logging.warning('Validation: SCA was not properly defined in the config')
        logging.warning('Validation: Ignoring SCA, Please provide all mandatory inputs incase you like to run SCA scan.')
        
    #ss
    try:
        if Config.config_data['Secret_Scan'] == False:
            Config.secret_scan_present = False
        else:   
            try:
                Config.sast_build_dir  = Config.config_data['SAST']['work_dir']
            except KeyError: 
                Config.sast_build_dir = os.getcwd()+'/'
                 
            try:
                Config.secret_scan_present =  True if Utils.isGitDirectory(Config.sast_build_dir) else False

                if Config.secret_scan_present:
                    logging.info('Validation: Secret scanning is properly configured and ready to scan')
                    Config.secret_scan_message ='Secret scanning is properly configured and ready to scan'
                else:
                    logging.warning('Validation: Secret scanning is properly configured, but working directory is not a git repository.') 
                    logging.warning('Validation: Ignoring Secret scanning.')    
                    Config.secret_scan_message ='Secret scanning is properly configured, but working directory is not a git repository.'       
            except KeyError:
                Config.secret_scan_present = False
                logging.warning('Validation: Secret scanning is not properly configured, Working directory is not git.') 
                Config.secret_scan_message ='Secret scanning is not properly configured'     
    except KeyError:
        Config.secret_scan_present = False  
        logging.warning('Validation: Secret scanning is not properly configured. Cant read the Secret_Scan configuration.')   
        Config.secret_scan_message ='Secret scanning is not properly configured'  

    try:
        if "container_scan" in Config.config_data:
            Config.con_scan_present = True
            Config.con_scan_build_dir= os.getcwd()+'/'
            try:
                logging.info('Validation: Configuring type for Container Scan')
                Config.con_scan_type = str(Config.config_data['container_scan']['type']).lower()
                if not (Config.con_scan_type == "config" or Config.con_scan_type == "image"):
                    logging.error(f"Invalid 'type': {Config.con_scan_type}. 'type' parameter must be 'config' or 'image' for container scanning")
                    exit(4)
                logging.info(f'Validation: Type configured for Container Scan: {Config.con_scan_type}')
            except KeyError: 
                logging.error("Validation: Type parameter is missing. 'type' parameter is required for container scanning")
                exit(4)
                
            try:
                logging.info('Validation: Configuring target for Container Scan')
                Config.con_scan_target = Config.config_data['container_scan']['target']
                if Config.con_scan_target is None:
                    if Config.con_scan_type == "config":
                        Config.con_scan_target= ""
                    else:
                        logging.error("Validation: FAILED!!! exit code: 4(CONFIG ERROR) Target is missing. Please configure target properly eg: target: myimage:version")
                        exit(4)
                logging.info(f'Validation: Target configured for Container Scan: {Config.con_scan_target}')
            except KeyError:
                if Config.con_scan_type=="config":
                    Config.con_scan_target="/"
                else:     
                    logging.error("Validation: FAILED!!! exit code: 4(CONFIG ERROR) Target parameter is missing. 'target' parameter is required for container scanning")
                    exit(4)
            
            logging.info('Validation: Container Scan is properly configured and ready to scan')
            Config.con_scan_message ='Container Scan is properly configured and ready to scan'
        else:
            Config.con_scan_present = False
            logging.warning('Validation: Container Scan is not properly configured. Cant read the "container_scan" configuration.')   
            Config.con_scan_message ='Container Scan is not properly configured'
    except:
        Config.con_scan_present = False
        logging.warning('Validation: Container Scan is not properly configured. Cant read the "container_scan" configuration.')   
        Config.con_scan_message ='Container Scan is not properly configured'

    try:
        if "SBOM" in Config.config_data:
            if Config.config_data['SBOM']:
                Config.sbom_present = True
                Config.sbom_build_dir = os.getcwd()+"/"
                logging.info('Validation: SBOM is properly configured and ready to scan')
            else:
                Config.sbom_present = False
                logging.warning('Validation: SBOM is not properly configured. Cant read the "sbom" configuration.')   
                Config.sbom_message ='sbom is not properly configured'
           
        else:
            Config.sbom_present = False
            logging.warning('Validation: SBOM is not properly configured. Cant read the "sbom" configuration.')   
            Config.sbom_message ='sbom is not properly configured'
    except:
        Config.sbom_present = False  
        logging.warning('Validation: SBOM is not properly configured. Cant read the "sbom" configuration.')   
        Config.sbom_message ='sbom is not properly configured'
    
    # Validation of boman.yaml for IaC scanning
    try:
        if "IAC" in Config.config_data:
            Config.iac_scan_present = True
            Config.iac_scan_build_dir= os.getcwd()+'/'
                
            try:
                logging.info('Validation: Configuring target for IaC Scan.')
                Config.iac_scan_target = Config.config_data['IAC']['target']
                logging.info(f'Validation: Target configured for IaC Scan: {Config.iac_scan_target}')
            except KeyError:
                Config.iac_scan_target="/"
                logging.info("KEY ERROR")
                logging.warning('Validation: target is missing for IaC Scan. target configured to default path')
            except TypeError:
                Config.iac_scan_target="/"
                logging.info("TYPE ERROR")
                logging.warning('Validation: target is missing for IaC Scan. target configured to default path')
            
            logging.info('Validation: IaC Scan is properly configured and ready to scan')
            Config.iac_scan_message ='IaC Scan is properly configured and ready to scan'
        else:
            Config.iac_scan_present = False
            logging.warning('Validation: IaC Scan is not properly configured. Cant read the "IAC" configuration.')   
            Config.iac_scan_message ='IaC Scan is not properly configured'
    except:
        Config.iac_scan_present = False
        logging.warning('Validation: IaC Scan is not properly configured. Cant read the "IAC" configuration.')   
        Config.iac_scan_message ='IaC Scan is not properly configured'    
   

## need to use lingudetect here, but the results are not trustable and misleading ------ MM -------------------
def findLang():
    print('[INFO]: Detecting Language')


def tool_configuration_validation():
    url = Config.boman_url+"/api/app/get_tool_config"
    logging.info('Tool Config: Authenticating with boman server')    
    data = {'app_token': Config.app_token, 'customer_token': Config.customer_token,'sca_langs':Config.sca_lang}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        logging.info("Tool Config: Communicating with SaaS for Authorization")
        res = requests.post(url, json=data, headers=headers)
    except requests.ConnectionError:
        logging.error("Tool Config: Failed!!! Message: Can't connect to the Server while getting tool configuration, Please check your Internet connection.")
        exit(1) #server/saas error
    else:
        if res.status_code == 200:
            try:
                json_response = json.loads(res.content)
                logging.info("Tool Config: Success!!! Message: Successfully Authorized")                
                # logging.info(json_response)
            except:
                logging.info("Tool Config: Failed!!!  exit code: 1 (Server ERROR) Message: Problem occured while authorizing the scan, Please contact boman.ai team")
                exit(1) #server error
            try:
                logging.info( json_response['data'])
               
                Config.dast_response = json_response['data']['dast']
                logging.info(Config.dast_response)
                Config.sast_response = json_response['data']['sast']
                Config.sca_response = json_response['data']['sca']
                Config.secret_scan_response = json_response['data']['secret_scan']
                Config.scan_token = json_response['data']['scan_token']    
                Config.scan_name = json_response['data']['scan_name']
                Config.con_scan_response = json_response['data']['cs']
                Config.sbom_response = json_response['data']['sbom']
                Config.iac_scan_response = json_response['data']['iac']  


                # if Config.json_response['data']['advanced_zap_auth']:
                #     Config.dast_adv_auth_enabled = True  
                # else:
                #     Config.dast_adv_auth_enabled = False

            except:
                logging.info("Tool Config: Failed!!!  exit code: 1 (Server ERROR) Message: Problem occured while authorizing the scan, Please contact boman.ai team")
                exit(1) ## server error  
                    
        elif res.status_code == 401:
            logging.error('Tool Config: Failed!!! exit code: 2(AUTH ERROR) Message: Unauthorized Access. Check the tokens')
            exit(2)
        else: 
            logging.error(f'Tool Config: Failed!!! exit code: 2(AUTH ERROR) Message: Boman returned status code: {res.status_code}({res.reason})')	       
            exit(2) ##auth error
    
    try:
        # logging.info( json_response['configuration'])
        Config.sast_present = json_response['configuration']['sast']['configured']
        Config.dast_present = json_response['configuration']['dast']['configured']
        Config.sca_present = json_response['configuration']['sca']['configured']
        Config.secret_scan_present = json_response['configuration']['secret']['configured']
        Config.sbom_present = json_response['configuration']['sbom']['configured']
        Config.iac_scan_present = json_response['configuration']['iac']['configured']
        Config.con_scan_present = json_response['configuration']['container']['configured']
    
    except KeyError as ke:
        logging.error(f'Tool Config: Failed!!! exit code: 4(CONFIG ERROR) Message: SaaS CONFIGURATION ERROR: {ke}')
        exit(4) #configuration error
    
    try:
        Config.sast_configuration = json_response['configuration']['sast']
        Config.dast_configuration = json_response['configuration']['dast']
        Config.sca_configuration = json_response['configuration']['sca']
        Config.secret_scan_configuration = json_response['configuration']['secret']
        Config.sbom_configuration = json_response['configuration']['sbom']
        Config.iac_scan_configuration = json_response['configuration']['iac']
        Config.con_scan_configuration = json_response['configuration']['container']
    
    except KeyError as ke:
        logging.error(f'Tool Config: Failed!!! exit code: 4(CONFIG ERROR) Message: SaaS CONFIGURATION ERROR: {ke}')
        exit(4) #configuration error
            
    Config.sast_build_dir = Config.sca_build_dir = Config.con_scan_build_dir = Config.sbom_build_dir = Config.iac_scan_build_dir = os.getcwd()+'/'
    
    try:
        if Config.sast_present:
            Config.sast_message = 'SAST is properly configured'
            Config.sast_ignore = True if Config.sast_configuration['ignore_files'].lower() == "true" else False
            Config.sast_target = Config.sast_configuration['target']
            Config.sast_lang = "semgrep"
            Config.sast_ignore_folders_and_files = Config.sast_configuration['sast_ignore_file_data']
        else:
            Config.sast_message = 'SAST was not properly configured on SaaS'
            logging.warning('Tool Config: SAST was not properly configured on SaaS')
            logging.warning('Tool Config: Ignoring SAST, Please provide all mandatory inputs incase you like to run SAST scan.')
    except KeyError as ke:
        logging.error(f'Tool Config: Failed!!! Message: SAST MISSING CONFIGURATION: {ke}')
        Config.sast_message = 'ERROR while configuring SAST'
        
        
    try:        
        if Config.dast_present:
            Config.dast_message = 'DAST is properly configured'
            if Config.dast_configuration['auth'] is True:
                Config.dast_auth_present = Config.dast_configuration['auth']
            elif Config.dast_configuration['auth'].lower() == "true":
                Config.dast_auth_present = True
            else:
                Config.dast_auth_present = False          
            # Config.dast_auth_present = Config.dast_configuration['auth']
            Config.dast_target = Config.dast_configuration['url']
            Config.dast_type = Config.dast_configuration['type'].lower()
            if Utils.testDastUrl(Config.dast_target):
                logging.info('Tool Config: DAST is properly configured and ready to scan')
                
                if Config.dast_type == 'API':
                    logging.info('Tool Config: DAST is configured for API scan, checking API type.')    
                    if (Config.dast_configuration['api_type'] is not None) and (Config.dast_configuration['api_type'] != "" ) :
                        Config.dast_api_type = Config.dast_configuration['api_type']
                        logging.info('Tool Config: API type for Dast is configured.')
                    else:
                        logging.info('Tool Config: DAST API type is not given, proceeding with default value: OPENAPI')
                        Config.dast_api_type = 'openapi'  


            else:    
                logging.warning('Tool Config: DAST target is not reachable, ignoring DAST scan')
                Config.dast_present = False
                Config.dast_message = 'DAST target is not reachable. DAST scan was ignored'
        else:
            Config.dast_message = 'DAST was not properly configured on SaaS'
            logging.warning('Tool Config: DAST was not properly configured on SaaS')
            logging.warning('Tool Config: Ignoring DAST, Please provide all mandatory inputs incase you like to run DAST scan.')
    except KeyError as ke:
        logging.error(f'Tool Config: Failed!!! Message: DAST MISSING CONFIGURATION: {ke}')
        Config.dast_message = 'ERROR while configuring DAST'
        
    try:
        if Config.secret_scan_present:
            Config.secret_scan_message = 'Secret Scan is properly configured'
        else:
            Config.secret_scan_message = 'Secret Scan was not properly configured on SaaS'
            logging.warning('Tool Config: Secret Scan was not properly configured on SaaS')
            logging.warning('Tool Config: Ignoring Secret Scan, Please provide all mandatory inputs incase you like to run Secret Scan.')
    except KeyError as ke:
        logging.error(f'Tool Config: Failed!!! Message: Secret Scan MISSING CONFIGURATION: {ke}')
        Config.secret_scan_message = 'ERROR while configuring Secret Scan'
        
    try:
        if Config.sca_present:
            Config.sca_message = 'SCA is properly configured'
        else:
            Config.sca_message = 'SCA was not properly configured on SaaS'
            logging.warning('Tool Config: SCA was not properly configured on SaaS')
            logging.warning('Tool Config: Ignoring SCA, Please provide all mandatory inputs incase you like to run SCA.')
    except KeyError as ke:
        logging.error(f'Tool Config: Failed!!! Message: SCA MISSING CONFIGURATION: {ke}')
        Config.sca_message = 'ERROR while configuring SCA'
        
    try:
        if Config.sbom_present:
            Config.sbom_message = 'SBOM is properly configured'
        else:
            Config.sbom_message = 'SBOM was not properly configured on SaaS'
            logging.warning('Tool Config: SBOM was not properly configured on SaaS')
            logging.warning('Tool Config: Ignoring SBOM, Please provide all mandatory inputs incase you like to run SBOM.')
    except KeyError as ke:
        logging.error(f'Tool Config: Failed!!! Message: SBOM MISSING CONFIGURATION: {ke}')
        Config.sbom_message = 'ERROR while configuring SBOM'
        
    try:
        if Config.iac_scan_present:
            Config.iac_scan_message = 'IaC scan is properly configured'
            Config.iac_scan_target = Config.iac_scan_configuration['target']
        else:
            Config.iac_scan_message = 'IaC scan  was not properly configured on SaaS'
            logging.warning('Tool Config: IaC scan  was not properly configured on SaaS')
            logging.warning('Tool Config: Ignoring IaC scan , Please provide all mandatory inputs incase you like to run IaC scan .')
    except KeyError as ke:
        logging.error(f'Tool Config: Failed!!! Message: IaC scan MISSING CONFIGURATION: {ke}')
        Config.iac_scan_message = 'ERROR while configuring IaC scan'
        
    try:
        if Config.con_scan_present:
            Config.con_scan_message = 'Container Scan is properly configured'
            Config.con_scan_type = Config.con_scan_configuration['type'].lower()
            Config.con_scan_target = Config.con_scan_configuration['target']
        else:
            Config.con_scan_message = 'Container Scan was not properly configured on SaaS'
            logging.warning('Tool Config: Container Scan was not properly configured on SaaS')
            logging.warning('Tool Config: Ignoring Container Scan, Please provide all mandatory inputs incase you like to run Container Scan scan.')
    except KeyError as ke:
        logging.error(f'Tool Config: Failed!!! Message: Container Scan MISSING CONFIGURATION: {ke}')
        Config.con_scan_message = 'ERROR while configuring Container scan'