import requests
# from base_logger import logging
# from Config import Config
from bomancli.base_logger import logging
from bomancli.Config import Config
from bomancli import utils as Utils
import os
import json 

logging.basicConfig(format='%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')

# new authorization which just authorize the cli run using app token and customer token. 
# This api gets SCA configuration as well to decide which tool to be used (OSV or owasp dependency check)
def new_authorize():
    
    url_new =Config.boman_url+"/api/app/new_authorize"
    data_new = {'app_token': Config.app_token, 'customer_token': Config.customer_token}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        # logging.info(data_new)
        logging.info("New Authorization: Communicating with SaaS for Authorization")
        res = requests.post(url_new, json=data_new, headers=headers)
        # logging.info(res.content)
        #print('req:', json.dumps(data))
        #print('res:',json.loads(res.content))
    except requests.ConnectionError:
       logging.error("New Authorization: Failed!!! Message: Can't connect to the Server while authorizing, Please check your Internet connection.")
       exit(1) #server/saas error
    else:
        if res.status_code == 200:
            try:
                json_response = json.loads(res.content)
                logging.info("New Authorization: Success!!! Message: Successfully Authorized")
                if json_response['advanced_zap_auth']:
                    Config.dast_adv_auth_enabled = True  
                else:
                    Config.dast_adv_auth_enabled = False
                logging.info(json_response)
                
            except:
                logging.info('New Authorization: Failed!!! exit code: 2 (AUTH ERROR) Message: Authorization Failed unable to load json response')
                exit(2) ##auth error
            try:
                sca_configuration = json_response['sca']
                
            except:
                logging.error('New Authorization: Failed!!! exit code: 1 (Server ERROR) Message: Problem occured while authorizing the scan, Please contact boman.ai team') 
                #uploadLogs() this wont work because the scan is not initated.
                exit(1) ## server error
        elif res.status_code == 401:
            logging.error('New Authorization: Failed!!! exit code: 2 (Server ERROR) Message: Problem occured while authorizing the scan , Please check authorization tokens correct. If you are still facing the same problem.')
            exit(2) ##auth error
        else: 
            logging.error(f'New Authorization: Failed!!! exit code: 2 (Server ERROR) Message: Boman returned status code: {res.status_code}({res.reason})')	       
            exit(2) ##auth error
    Config.sca_present = (sca_configuration['configured'])
    Config.sca_build_dir = os.getcwd()+'/'           
    if Config.sca_present:
        Config.sca_type = sca_configuration['type'].lower()
        Config.sca_target = sca_configuration['target']
        Config.sca_ignore = True if sca_configuration['ignore_files'].lower() == "true" else False
        Config.sca_ignore_folders_and_files = sca_configuration['sca_ignore_file_data']
        if Config.sca_type == "directory":
            file_present = False     
            for filename in Config.osv_supported_files:
                if Config.sca_target is None:
                    if recursive_file_present_check(Config.sca_build_dir,filename):
                        file_present =True
                        Config.sca_target= ""
                        logging.info(f"New Authorization: Boman has found the dependency file: {filename} in the path: {os.path.join(Config.sca_build_dir,Config.sca_target)}")
                        break                
                else:    
                    if recursive_file_present_check(os.path.join(Config.sca_build_dir,Config.sca_target),filename):
                        file_present =True
                        Config.sca_target= os.path.join(Config.sca_target,filename)
                        logging.info(f"New Authorization: Boman has found the dependency file: {filename} in the path: {os.path.join(Config.sca_build_dir,Config.sca_target)}")
                        break
            if file_present:
                Config.sca_lang ="osv"
            else:
                logging.warning(f"New Authorization: Boman has not found the dependency file which OSV supports.")
                if Config.sca_target is not None:
                    Config.sca_build_dir = os.path.join(Config.sca_build_dir,Config.sca_target)
                logging.info(f"New Authorization: build dir: {Config.sca_build_dir} ")
                Config.sca_lang = "owasp dependency check"
        elif file_present_check(os.path.join(Config.sca_build_dir,Utils.remove_leading_slash(Config.sca_target))):
            Config.sca_lang ="osv"
        else:
            logging.error(f"New Authorization: No such file found: {os.path.join(Config.sca_build_dir,Utils.remove_leading_slash(Config.sca_target))}")
            exit(4)
        
        logging.info(f"Boman opted for: {Config.sca_lang} scan.")
        
                
               

## function to authorize and get the images form SAAS --------------------------------------------------------
def authorize():
    
    url = Config.boman_url+"/api/app/authorize"
    
    if Config.sca_present:
        if Config.sca_type == "directory":
            file_present = False     
            for filename in Config.osv_supported_files:
                if Config.sca_target is None:
                    if recursive_file_present_check(Config.sca_build_dir,filename):
                        file_present =True
                        Config.sca_target= ""
                        logging.info(f"Authorization: Boman has found the dependency file: {filename} in the path: {os.path.join(Config.sca_build_dir,Config.sca_target)}")
                        break                
                else:    
                    if recursive_file_present_check(os.path.join(Config.sca_build_dir,Config.sca_target),filename):
                        file_present =True
                        Config.sca_target= os.path.join(Config.sca_target,filename)
                        logging.info(f"Authorization: Boman has found the dependency file: {filename} in the path: {os.path.join(Config.sca_build_dir,Config.sca_target)}")
                        break
            if file_present:
                Config.sca_lang ="osv"
            else:
                logging.warning(f"Authorization: Boman has not found the dependency file")
                if Config.sca_target is not None:
                    Config.sca_build_dir = os.path.join(Config.sca_build_dir,Config.sca_target)
                logging.info(f"Authorization: build dir: {Config.sca_build_dir} ")
                Config.sca_lang = "owasp dependency check"
        elif file_present_check(os.path.join(Config.sca_build_dir,Utils.remove_leading_slash(Config.sca_target))):
            Config.sca_lang ="osv"
        else:
            logging.error(f"Authorization: Failed!!! Message: No such file found: {os.path.join(Config.sca_build_dir,Utils.remove_leading_slash(Config.sca_target))}")
            exit(4)
        
        logging.info(f"Authorization: Boman opted for: {Config.sca_lang} scan")
    logging.info('Authorization: Authenticating with boman server')    
    data = {'app_token': Config.app_token, 'customer_token': Config.customer_token, 'sast':Config.sast_present,"dast":Config.dast_present,"dast_type":Config.dast_type,"dast_auth_enabled":Config.dast_auth_present,"sast_langs":Config.sast_lang,"sca":Config.sca_present,"sca_langs":Config.sca_lang,"sca_scan_type":Config.sca_type,"secret_scan":Config.secret_scan_present,'container_scan': Config.con_scan_present,'container_scan_type': Config.con_scan_type,"sbom":Config.sbom_present,'iac':Config.iac_scan_present}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # logging.info(data)
    try:
        logging.info("Authorization: Communicating with SaaS for Authorization")
        res = requests.post(url, json=data, headers=headers)
        #print('req:', json.dumps(data))
        logging.info('res: %s',json.loads(res.content))
    except requests.ConnectionError:
       logging.error("Authorization: Failed!!! Message: Can't connect to the Server while authorizing, Please check your Internet connection.")
       exit(1) #server/saas error
    else:
        if res.status_code == 200:
            try:
                json_response = json.loads(res.content)
                logging.info("Authorization: Success!!! Message: Successfully Authorized")
                if json_response['data']['advanced_zap_auth']:
                    Config.dast_adv_auth_enabled = True  
                else:
                    Config.dast_adv_auth_enabled = False
                # logging.info(json_response)
            except:
                logging.info("Authorization: Failed!!!  exit code: 1 (Server ERROR) Message: Problem occured while authorizing the scan, Please contact boman.ai team")
                exit(1) #Server error
            try:
                Config.dast_response = json_response['data']['dast']
                Config.sast_response = json_response['data']['sast']
                Config.sca_response = json_response['data']['sca']
                Config.secret_scan_response = json_response['data']['secret_scan']
                Config.scan_token = json_response['data']['scan_token']    
                Config.scan_name = json_response['data']['scan_name']
                Config.con_scan_response = json_response['data']['cs']
                Config.sbom_response = json_response['data']['sbom']
                Config.iac_scan_response = json_response['data']['iac']   

                return 1    
            except:
                logging.info("Authorization: Failed!!!  exit code: 1 (Server ERROR) Message: Problem occured while authorizing the scan, Please contact boman.ai team")
                exit(1) ## server error  
                    

        elif res.status_code == 401:
            logging.error('Authorization: Failed!!! Message: Unauthorized Access. Check the tokens')
            exit(2) ##auth error
        else: 
            logging.error(f'Authorization: Failed!!! Message: Boman returned status code: {res.status_code}({res.reason})')	       
            exit(2) ##auth error

# whether file present in the directory or not
def recursive_file_present_check(root_dir, file_name):
    for root, dirs, files in os.walk(root_dir):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

# whether file present in the directory or not
def file_present_check(filename):
    if os.path.isfile(filename):
        return True
    return False
