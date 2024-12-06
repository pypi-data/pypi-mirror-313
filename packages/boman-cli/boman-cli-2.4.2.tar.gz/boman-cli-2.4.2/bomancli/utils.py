
# from base_logger import logging
# from Config import Config
# import loc_finder as loc
#from datetime import datetime


from bomancli.base_logger import logging
from bomancli.Config import Config
from bomancli import loc_finder as loc
import pkg_resources

import requests


import os 
import subprocess
import json
import xmltodict
import yaml
 
logging.basicConfig(format='%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s') 
 
docker = Config.docker_client


##fucntion to check the docker image is already present or not
def checkImageAlreadyExsist(imagename):
    #print(imagename)
    try:
        
        image_list = docker.images.list()
        logging.info('Checking the scanner image (%s) locally',imagename)  
    except Exception as e:
        logging.error('Docker throwing a error , please check the docker installation')
        #print(str(e))
        exit(3) ## docker/system error

    for image in image_list:
       #print(image.tags)
        if imagename in image.tags:
            logging.info('Image is already in the local machine')
            return True
    
    logging.info('Image is not present in the local machine')
    logging.info('Pulling the required image [%s]',imagename)
    return 1

    try:
        pulled = docker.images.pull(imagename)
        return 1
    except Exception as exc:
        logging.error(exc)
        logging.error('Error pulling the image [%s]',imagename)
        exit(3) ## docker/system error

            


### fucntion to check the git is present or not
def isGitDirectory(path):
    try:
        isdir = os.path.isdir(path+'/.git/') 
        #print(isdir) 
        return isdir
        #return subprocess.call(['git', '-C', path, 'status'], stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) == 0
    except:
        return 0

    




### fucntion to test SaaS server, whether is up or not:
def testServer():
    logging.info('Testing Boman.ai Server')
    url = Config.boman_url+"/api/app/ping"
    try:
        x = requests.get(url)  #var ="renga"
    except requests.ConnectionError as e:
        print(e)
        logging.error("Can't connect to the Server, Please check your Internet connection.")
        exit(1) #server/saas error
    else:
        if str(x.content):
            logging.info("Server is reachable ")
            return 1
        else:
            logging.error("Boman.ai Server is not reachable")	
            exit(1) ## docker/system error



### function to check docker is available in the machine or not -- MM
def testDockerAvailable():
    logging.info('Checking for docker in the machine')
    try:
        
        if docker.ping():
           logging.info('Docker is running in the machine. Good to go!')
        else:
            logging.error('Unable to connect to docker, Please install docker in your environment')    
    except Exception as e:
        logging.error('Docker not found in your machine, Please install docker to continue the scanning')
        #print(str(e))
        exit(3) ## docker/system error



### function to test the dast url is accesible or not --- MM


def testDastUrl(url):
    logging.info('Testing %s target', url)
    #url = Config.boman_url+"/api/app/ping"
    #print(url)
    try:
        x = requests.get(url)
    except requests.ConnectionError:
        logging.error("Can't connect to the %s, Please check your Internet connection.", url)
        return 0
    else:
        logging.info("DAST target is reachable")
        return 1
        # if x.status_code == 200:
           
        #     return 1
        # else:
        #     logging.error("Boman.ai Server is not reachable")	
        #     exit(3)




### fucntion to get the loc in given directory and lang

def getLoc():
    return 0


    #logging.info('Counting the lines of code of the given languages. Found: %s',Config.sast_build_dir)

    uid = os.getuid()
    Config.lingu_user = uid;




    logging.info('Counting the lines of code of the given language with user id: %s on : %s',Config.lingu_user,Config.sast_build_dir)

    if isGitDirectory(Config.sast_build_dir):
    
        try:

            docker_image = 'bomanai/linguist:latest'
            command_line = 'github-linguist --json'
            
            Config.build_dir = Config.sast_build_dir
            container_output = docker.containers.run(docker_image, command_line, volumes={Config.sast_build_dir: {
                        'bind': Config.sast_build_dir}}, user=Config.lingu_user, working_dir=Config.sast_build_dir)


            #print(container_output)
            decoded_string = container_output.decode('utf-8')
            Config.lingu_details = json.loads(decoded_string)
            return Config.lingu_details

        except Exception as e:
            print('error occured while detecting the languages: [%s]',e)
            return 0

    else:

        return 0


## this function will mask the middle charecters depending on the lenght of given value and return -- used in trufflehog -- MM
def masker(n):
    var1 = str(n)
    str_length = len(n)

    if str_length > 15:
        total_unmask_char_len = 8
        prefix_char_len = 4
        sufix_char_len = 4
    elif str_length < 10:
        total_unmask_char_len = 4
        prefix_char_len = 2
        sufix_char_len = 2
    elif str_length < 5:
        total_unmask_char_len = 2
        prefix_char_len = 1
        sufix_char_len = 1
    elif str_length < 3:
        masked = '#' * str_length
        return masked

    unmasked_len = str_length - total_unmask_char_len
    masked_value = '#' * unmasked_len

    prefix = var1[:prefix_char_len]

    sufix = var1[-sufix_char_len:]

    masked = prefix+masked_value+sufix
    return masked



def convertXmlToJson(file_name,path,output_file):
    
    # open the input xml file and read
    # data in form of python dictionary
    # using xmltodict module
    target = path+file_name
    output_target = path+output_file

    try:
        with open(target) as xml_file:
            
            data_dict = xmltodict.parse(xml_file.read())
            xml_file.close()
            
            # generate the object using json.dumps()
            # corresponding to json data
            
            json_data = json.dumps(data_dict)
            
            # Write the json data to output
            # json file
            with open(output_target, "w") as json_file:
                json_file.write(json_data)
                json_file.close()
            return 1

    except Exception as e:
        return 0




def logError(msg,error):
    f = open("bomancli.errors.log", "a")
    msg = msg+'\n'
    # writing in the file
    now = 'ss'
    f.write('\n===========================================================\n')
    f.write(str(now))
    f.write(str(msg))
    f.write(str(error)) 
     # closing the file
    f.close()



## summary function

def showSummary():
    logging.info('---------------------------------------------------------------------------------------------------------------')
    logging.info('--------------------------  SUMMARY FOR SCAN: %s  -----------------------------------------------',Config.scan_name,)
    logging.info('--------------------------- Scan Token: %s --------------------------------------------------------',Config.scan_token)
    if Config.git_present:
        logging.info('--------------------------- Git Details:[Repo: %s, Branch: %s ]--------------------------------------------------------',Config.git_repo,Config.git_branch)
        logging.info('--------------------------- Language  :   Files_Size :  Percentage --------------------------------------------------------')
        # Step 3: Loop through each item in the JSON object    
        for file_type, details in Config.lingu_details.items():
            logging.info('--------------------------- %s  :   %s :  %s%%--------------------------------------------------------', file_type, details['size'], details['percentage'])
    logging.info('---------------------------------------------------------------------------------------------------------------')
    logging.info('----------------------------------------')
    logging.info('-------- Vulnerabilities Found ---------')
    logging.info('HIGH : %s | MEDIUM : %s | LOW : %s ', Config.high_count, Config.medium_count, Config.low_count)
    logging.info('----------------------------------------')
    logging.info('----------------------------------------')
    logging.info('-------- SAST STATUS ---------')
    if Config.sast_present == True:
        logging.info('SCAN STATUS: %s',Config.sast_scan_status)
        logging.info('UPLOAD STATUS: %s',Config.sast_upload_status)
        logging.info('SCAN MESSAGE : %s', Config.sast_message)

        logging.info('ERRORS: %s',Config.sast_errors)
    else:
        logging.info('SCAN MESSAGE : %s', Config.sast_message)   
    logging.info('----------------------------------------')

    logging.info('-------- DAST STATUS ---------')
    if Config.dast_present == True:
        logging.info('SCAN STATUS: %s',Config.dast_scan_status)
        logging.info('UPLOAD STATUS: %s',Config.dast_upload_status)
        logging.info('SCAN MESSAGE : %s', Config.dast_message)

        logging.info('ERRORS: %s',Config.dast_errors)
    else:
        logging.info('SCAN MESSAGE : %s', Config.dast_message)    
    logging.info('--------------------------------------')


    
    logging.info('-------- SCA STATUS ---------')
    if Config.sca_present == True:
        logging.info('SCAN STATUS: %s',Config.sca_scan_status)
        logging.info('UPLOAD STATUS: %s',Config.sca_upload_status)
        logging.info('SCAN MESSAGE : %s', Config.sca_message)
        
        logging.info('ERRORS: %s',Config.sca_errors)
    else:
        logging.info('SCAN MESSAGE : %s', Config.sca_message)     
    logging.info('--------------------------------------')



    logging.info('-------- SECRET SCAN STATUS --------- ')
    if Config.secret_scan_present:
        logging.info('SCAN STATUS: %s',Config.secret_scan_status)
        logging.info('UPLOAD STATUS: %s',Config.secret_scan_upload_status)
        logging.info('SCAN MESSAGE : %s', Config.secret_scan_message)
        
        logging.info('ERRORS: %s',Config.secret_scan_errors)
    else:
        logging.info('SCAN MESSAGE : %s', Config.secret_scan_message)   
    logging.info('-------------------------------------')

    logging.info('-------- CONTAINER SCAN STATUS --------- ')
    if Config.con_scan_present:
        logging.info('SCAN STATUS: %s',Config.con_scan_status)
        logging.info('UPLOAD STATUS: %s',Config.con_scan_upload_status)
        logging.info('SCAN MESSAGE : %s', Config.con_scan_message)
        
        logging.info('ERRORS: %s',Config.con_scan_errors)
    else:
        logging.info('SCAN MESSAGE : %s', Config.con_scan_message)   
    logging.info('-------------------------------------')
    
    logging.info('-------- SBOM SCAN STATUS --------- ')
    if Config.sbom_present:
        logging.info('SCAN STATUS: %s',Config.sbom_scan_status)
        logging.info('UPLOAD STATUS: %s',Config.sbom_upload_status)
        logging.info('SCAN MESSAGE : %s', Config.sbom_message)
        
        logging.info('ERRORS: %s',Config.sbom_errors)
    else:
        logging.info('SCAN MESSAGE : %s', Config.sbom_message)   
    logging.info('-------------------------------------')

    logging.info('-------- IaC SCAN STATUS --------- ')
    if Config.iac_scan_present:
        logging.info('SCAN STATUS: %s',Config.iac_scan_status)
        logging.info('UPLOAD STATUS: %s',Config.iac_scan_upload_status)
        logging.info('SCAN MESSAGE : %s', Config.iac_scan_message)
        
        logging.info('ERRORS: %s',Config.iac_scan_errors)
    else:
        logging.info('SCAN MESSAGE : %s', Config.iac_scan_message)   
    logging.info('-------------------------------------')
    # logging.info(Config.sast_message)
    # logging.info(Config.dast_message)
    # logging.info(Config.sca_message)
    # logging.info(Config.secret_scan_message)




## zap config part


##zap plan creation fucntion


def write_yaml_to_file(py_obj,filename):
    with open(f'{filename}.yaml', 'w',) as f :
        yaml.dump(py_obj,f,sort_keys=False) 
    logging.info('Written to file successfully')



def createZapPlan(config,output_file):


    template_file_path = pkg_resources.resource_filename(__name__,'templates/template_plan.yaml')

    #logging.info(template_file_path)

    with open(template_file_path, 'r') as file:
        template_content = yaml.safe_load(file)


   ### print(config)
    
    #context part

    context_parameters = template_content['env']['contexts']

    context_parameters[0]['name'] = 'boman_generated_context'
    context_parameters[0]['urls'] = [config['target_url']]



    # authentication part


    #authentication method
    auth_method = template_content['env']['contexts'][0]['authentication']


    auth_method['method'] = config['auth_method']

    ##print(auth_method)

    #authentication parameters

    auth_parameters = template_content['env']['contexts'][0]['authentication']['parameters']

    auth_parameters['loginPageUrl'] = config['login_page_url']
    auth_parameters['loginRequestUrl'] = config['login_request_url']
    auth_parameters['loginRequestBody'] = config['login_request_body']


    #authentication verification

    auth_verification = template_content['env']['contexts'][0]['authentication']['verification']





    auth_verification['method'] = str(config['verification_strategy']['method'])

    if config['verification_strategy']['method'] == 'poll':
        auth_verification['pollFrequency'] = config['verification_strategy']['poll_frequency']
        auth_verification['pollUrl'] =  config['verification_strategy']['poll_url']
        auth_verification['pollPostData'] = ''



    auth_verification['loggedOutRegex'] = str(config['logout_indicator'])
    auth_verification['loggedInRegex'] = str(config['login_indicator'])






    #user credentials 

    users_parameter = template_content['env']['contexts'][0]['users']
    users_parameter[0]['name'] = 'Boman'
    users_parameter[0]['credentials']['username']= config['username']
    users_parameter[0]['credentials']['password'] = config['password']




    ##session script adding

    if config['auth_method'] == 'json':
        session =  template_content['env']['contexts'][0]
        session['sessionManagement']['method'] = 'script'
        session_path = '/zap/wrk/'+Config.zap_script_config_file_name
        session['sessionManagement']['parameters']['script'] = session_path
        session['sessionManagement']['parameters']['scriptEngine'] = 'Graal.js'
    else:
        session =  template_content['env']['contexts'][0]
        session.pop('sessionManagement')

    #     sessionManagement:
    #   method: "script"
    #   parameters:
    #     script: "C:\\Users\\Aswin G M\\Documents\\ZAP\\simplejsonscript.js"
    #     scriptEngine: "Graal.js"
        






    ##include/exculed urls 

    # include_urls = ['tets,test']
    # exclude_urls =['tets,test']




    # template_content['env']['contexts'][0]['includePaths'] = include_urls 
    # template_content['env']['contexts'][0]['excludePaths'] = exclude_urls

    passive_max_duration = 1
    passive_max_depth = 2
    passive_max_children = 0 

    #jobs_context_parametes
    template_content['jobs'][1]['parameters']['context'] = 'boman_generated_context'
    template_content['jobs'][1]['parameters']['url'] = config['target_url']
    template_content['jobs'][1]['parameters']['user'] = 'Boman'
    template_content['jobs'][1]['parameters']['maxDuration'] = passive_max_duration
    template_content['jobs'][1]['parameters']['maxDepth'] = passive_max_depth
    template_content['jobs'][1]['parameters']['maxChildren'] = passive_max_children


    template_content['jobs'][3]['parameters']['context'] = 'boman_generated_context'
    template_content['jobs'][3]['parameters']['user'] ='Boman'

    template_content['jobs'][4]['parameters']['reportDir'] = '/zap/wrk'
    template_content['jobs'][4]['parameters']['reportFile'] = output_file


    write_yaml_to_file(template_content, Config.zap_plan_config_file_name)


    
def fetchDASTConfigFromSaas():
    logging.info('Initiating connection with SaaS')
    scan_token = Config.scan_token
    app_token = Config.app_token
    customer_token =  Config.customer_token

    url = Config.boman_url+"/api/zapconfig/get"
    values = {'app_token':app_token, 'scan_token':scan_token, 'customer_token':customer_token}
    try:
        x = requests.post(url,json=values)  


        response = x.json()

        if response['status'] == True:
            logging.info('Analyzing DAST Auth config')
            Config.zap_plan_config = response['zap_config']['zap_auth_config']
            return 1

        else:
            logging.info('No DAST Auth Config found on SaaS')
            Config.zap_plan_config = None
            return 0


    except requests.ConnectionError as e:
        
        logging.error("Can't connect to the Server, Please check your Internet connection.")
        print(e)
        exit(1) #server/saas error



def createZapScript(config):
    zap_config = config
    logging.info('generating session_management script')
    #print(config)
    #return 0
    #exit(1)


    file_path = Config.zap_script_config_file_name

    vars = """
    var COOKIE_TYPE   = org.parosproxy.paros.network.HtmlParameter.Type.cookie;
    var HtmlParameter = Java.type('org.parosproxy.paros.network.HtmlParameter')
    var ScriptVars = Java.type('org.zaproxy.zap.extension.script.ScriptVars');
    """



    
    

    js_string=""

    if zap_config['token_present_in_res_body']:


        response_body_indentifier = 'json.'+ zap_config['token_param_in_res_body']

        extract_token_from_response_body ="""
        function extractWebSession(sessionWrapper) {
            // parse the authentication response
            var json = JSON.parse(sessionWrapper.getHttpMessage().getResponseBody().toString());
            var token = """+response_body_indentifier+""";
            // save the authentication token
            sessionWrapper.getSession().setValue("token", token);
        }
        """

        js_string="""
        """+extract_token_from_response_body+"""

        """

      

    # else:
    #     print('this part exceuted')
    #     print(zap_config['token_present_in_res_body'])
    #     exit(1)
    



    

   


    #print(zap_config["cookie_token_present"],zap_config["bearer_present"])
    #return 0

    if zap_config["bearer_present"] & zap_config["cookie_token_present"]:

        bearer_name="Authorization"

        if zap_config["custom_bearer_present"]:
            bearer_name= zap_config["custom_bearer_name"]
    
        cookie_param_name= "cookie."+zap_config["cookie_token_param_name"]

        logging.info('Bearer name %s',bearer_name)
        extract_cookie_or_token = """
        function extractWebSession(sessionWrapper) {
            // parse the authentication response
            var res_headers = sessionWrapper.getHttpMessage().getResponseHeader();
            var token =  res_headers."""+bearer_name+""";
            print("token is :"+token);
            // save the authentication token
            sessionWrapper.getSession().setValue("token", token);
        }
        """

        process_cookie_to_be_authenticated_by_zap ="""
        function processMessageToMatchSession(sessionWrapper) {
            var token = sessionWrapper.getSession().getValue("token");
            if (token === null) {
                print('JS mgmt script: no token');
                return;
            }
            var cookie = new HtmlParameter(COOKIE_TYPE, '"""+zap_config["cookie_token_param_name"]+"""', token);
            // add the saved authentication token as an Authentication header and a cookie
            var msg = sessionWrapper.getHttpMessage();
            msg.getRequestHeader().setHeader('"""+bearer_name+"""' , token);
            var cookies = msg.getRequestHeader().getCookieParams();
            cookies.add(cookie);
            msg.getRequestHeader().setCookieParams(cookies);
        }
        """

        clear_session ="""
        function clearWebSessionIdentifiers(sessionWrapper) {
            var headers = sessionWrapper.getHttpMessage().getRequestHeader();
            headers.setHeader('"""+bearer_name+"""', null);
        }"""

        js_string="""
        """+vars+"""
        """+extract_cookie_or_token+"""


        """+clear_session+"""


        """+process_cookie_to_be_authenticated_by_zap+"""

        function getRequiredParamsNames() {
        return [];
        }

        function getOptionalParamsNames() {
        return [];
        }

        """
    elif zap_config["bearer_present"]:
        bearer_name="Authorization"
    
        if zap_config["custom_bearer_present"]:
            bearer_name= zap_config["custom_bearer_name"]

        extract_cookie_or_token = """
        function extractWebSession(sessionWrapper) {
            // parse the authentication response
            var res_headers = sessionWrapper.getHttpMessage().getResponseHeader();
            var token =  res_headers."""+bearer_name+""";
            print("token is :"+token);
            // save the authentication token
            sessionWrapper.getSession().setValue("token", token);
        }
        """

        process_cookie_to_be_authenticated_by_zap ="""
        function processMessageToMatchSession(sessionWrapper) {
            var token = sessionWrapper.getSession().getValue("token");
            if (token === null) {
                print('JS mgmt script: no token');
                return;
            }
            var msg = sessionWrapper.getHttpMessage();
            msg.getRequestHeader().setHeader('"""+bearer_name+"""' , token);
        }
        """

        clear_session ="""
        function clearWebSessionIdentifiers(sessionWrapper) {
            var headers = sessionWrapper.getHttpMessage().getRequestHeader();
            headers.setHeader('"""+bearer_name+"""', null);
        }"""

        js_string="""
        """+vars+"""
        """+extract_cookie_or_token+"""


        """+clear_session+"""


        """+process_cookie_to_be_authenticated_by_zap+"""

        function getRequiredParamsNames() {
        return [];
        }

        function getOptionalParamsNames() {
        return [];
        }

        """
    elif zap_config["cookie_token_present"]:
       
        bearer_name="Authorization"
        if zap_config["custom_bearer_present"]:
            bearer_name= zap_config["custom_bearer_name"]
            
        cookie_param_name= "cookie."+zap_config["cookie_token_param_name"]

        #print(bearer_name)


        if zap_config['token_present_in_res_body']:


            response_body_indentifier = 'json.'+ zap_config['token_param_in_res_body']

            extract_cookie_or_token ="""
            function extractWebSession(sessionWrapper) {
                // parse the authentication response
                var json = JSON.parse(sessionWrapper.getHttpMessage().getResponseBody().toString());
                var token = """+response_body_indentifier+""";
                // save the authentication token
                sessionWrapper.getSession().setValue("token", token);
            }
            """

            process_cookie_to_be_authenticated_by_zap ="""
            function processMessageToMatchSession(sessionWrapper) {
                var token = sessionWrapper.getSession().getValue("token");
                if (token === null) {
                    print('JS mgmt script: no token');
                    return;
                }
                var cookie = new HtmlParameter(COOKIE_TYPE, '"""+zap_config["cookie_token_param_name"]+"""', token);
                var cookies = msg.getRequestHeader().getCookieParams();
                cookies.add(cookie);
                msg.getRequestHeader().setCookieParams(cookies);
            }
            """

           

        else:

            extract_cookie_or_token = """
            function extractWebSession(sessionWrapper) {
                // parse the authentication response
                var res_headers = sessionWrapper.getHttpMessage().getResponseHeader();
                var token =  res_headers."""+cookie_param_name+""";
                print("token is :"+token);
                // save the authentication token
                sessionWrapper.getSession().setValue("token", token);
            }
            """

            process_cookie_to_be_authenticated_by_zap ="""
            function processMessageToMatchSession(sessionWrapper) {
                var token = sessionWrapper.getSession().getValue("token");
                if (token === null) {
                    print('JS mgmt script: no token');
                    return;
                }
                var cookie = new HtmlParameter(COOKIE_TYPE, '"""+zap_config["cookie_token_param_name"]+"""', token);
                var cookies = msg.getRequestHeader().getCookieParams();
                cookies.add(cookie);
                msg.getRequestHeader().setCookieParams(cookies);
            }
            """




        js_string="""

        """+vars+"""
       
        """+extract_cookie_or_token+"""

        """+process_cookie_to_be_authenticated_by_zap+"""

        function getRequiredParamsNames() {
        return [];
        }

        function getOptionalParamsNames() {
        return [];
        }

        """

    with open(file_path, 'w') as js_file:
        js_file.write(js_string)
        logging.info('Wrote session management script')
    return 0


## git metadata fetch
def getGitDetails():
    try:
        # Get the Git repository name
        repo_name_cmd = "basename $(git rev-parse --show-toplevel)"
        repo_name_process = subprocess.Popen(repo_name_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        repo_name, _ = repo_name_process.communicate()
        repo_name = repo_name.decode("utf-8").strip()

        # Get the current branch name
        branch_name_cmd = "git rev-parse --abbrev-ref HEAD"
        branch_name_process = subprocess.Popen(branch_name_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        branch_name, _ = branch_name_process.communicate()
        branch_name = branch_name.decode("utf-8").strip()

        # Get the current commit message
        output = subprocess.check_output(["git", "log", "-1"])
        # Split the output into lines.
        lines = output.decode("utf-8").splitlines()
        # The commit message is the second line of the output.
        commit_message = lines[1]
        # Return the commit message, or None if there is no commit history.
        commit_message = commit_message or None
        




        data = {'repo':repo_name,'branch':branch_name,'commit_message':commit_message}

        return data
    except Exception as e:
        return {'repo':'None','branch':'None','commit_message':'None'}


#### create a zap plan and script with advanced scan
def download_file(url, save_path):
    """
    Downloads a file from the given URL and saves it to the specified path.

    :param url: The URL of the file to download.
    :param save_path: The path where the file will be saved.
    :return: None
    """
    try:
        url = url
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for HTTP errors

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    
        logging.info(f"File downloaded successfully and saved to {save_path}")
        return 1
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download file: {e}")



### fetch zap advance auth config
def fetch_zap_advance_config():
    logging.info('Initiating connection with SaaS')
    #scan_token = Config.scan_token
    app_token = Config.app_token
    customer_token =  Config.customer_token

    url = Config.boman_url+"/api/app/advanced_zap_authentication"
    values = {'app_token':app_token, 'customer_token':customer_token}
    try:
        x = requests.post(url,json=values)  


        response = x.json()

        

        if response['status'] == True:
            logging.info('Zap Advacne config: Analyzing DAST Auth config')
        
            ## fetching the urls

            config_files = response['zap_config']['files']
            logging.info('Config from SaaS: %s',config_files)
            files_count = len(config_files)
            logging.info('Zap Advance Config: Total %s file(s) uploaded in saas' )
            logging.info('Zap Advance Config: Downloading files one by one' )

            plan_file_present_in_adv_zap_config = False
            for file in config_files:
                logging.info('Zap Advacne Config: Fetching from %s filename %s',file['file_path'], file['file_name'])
                download_file(file['file_path'], file['file_name'])
                
                
                if file['is_plan_file']:
                    Config.zap_plan_config_file_name = file['file_name']
                   #Config.dast_auth_present = True
                    Config.custom_zap_plan_present = True
                    # with open(Config.zap_plan_config_file_name , 'r') as file:
                    #     Config.zap_plan_config = yaml.safe_load(file)  
                    #     print(Config.zap_plan_config)
                    #     exit(1)  
                    #     logging.info('Validation: SUCCESS!!! Message: Config yaml file found and parsed') 
                        
                    plan_file_present_in_adv_zap_config = True
                    logging.info('Zap Advacne Config: Plan file found %s',Config.zap_plan_config_file_name)


                
            logging.info('Zap Advance Config: files are downloaded')
            if plan_file_present_in_adv_zap_config == False:
                logging.info('Zap Advance Config: Plan.yaml file not found in the server, will be unable to continue the zap advance scan')
                logging.info('Main: Terminating the scan')
                exit(4)


            return 1

        else:
            logging.info('No DAST Auth Config found on SaaS')


    except requests.ConnectionError as e:
        
        logging.error("Can't connect to the Server, Please check your Internet connection.")
        logging.error(e)
        exit(1) #server/saas error    


def uploadLogs():
    
    # Get the captured log messages
    all_logs = Config.log_stream.logs

    #parameter setup

    body = {
    'auth_token': Config.app_token,
    'customer_token': Config.customer_token,
    'scan_token':Config.scan_token,
    'git_present':Config.git_present,
    'git_repo_name':Config.git_repo,
    'git_branch_name':Config.git_branch,
    'full_logs':all_logs,
    'lingu_details':Config.lingu_details
    # Add more parameters if needed
    }

    # Upload collected log messages To SaaS
    try:
        logging.info('Uploading logs for the scan token %s',str(Config.scan_token))
    
        url = Config.boman_url+"/api/scan/logs/upload" 

        response = requests.post(url, data=body)

        if response.status_code == 200:
            #logging.info('Uploading logs for the scan token %s',str(Config.scan_token))
            logging.info('[COMPLETED]: Logs are pushed to SaaS')
            logging.info('Please visit: %s/findings/ALL/%s/ALL to View your results',Config.boman_base_url,Config.scan_token)
            return 1
        elif response.status_code == 401 :
            logging.error('Unauthorized Access Error occured while uploading logs. Please check the app/customer tokens')
            exit(2)  ## Auth error
        else:
            logging.error('Some Problem While uploading the Logs.')
            logging.error('Response code from SaaS is %s',response.status_code)
    except Exception as e:
        logging.error('Problem While uploading the Logs.[%s]',e)
        logging.info('Please use bomancli.log file for troubleshooting or contact admin for more details',Config.boman_url)

    #create a log file

    return 1

def remove_leading_slash(s):
    # Check if the first character is a slash and remove it
    return s[1:] if s.startswith('/') else s

def read_bomanignore(file_path):
    exclude_paths = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Skip comments and empty lines
                line = line.strip()
                if line and not line.startswith('#'):
                    full_command = " --exclude "+line
                    exclude_paths.append(full_command)
    except FileNotFoundError:
        logging.info(f"Error: {file_path} not found.")
        if Config.sca_ignore_folders_and_files is not None:
            for line in Config.sca_ignore_folders_and_files:
                line = line.strip()
                if line and not line.startswith('#'):
                    full_command = " --exclude "+line
                    exclude_paths.append(full_command)
            return ''.join(exclude_paths)                
        return False
    # Join the list into a space separated string
    return ''.join(exclude_paths)

def copy_file(source_path, dest_path):
    try:
        with open(source_path, 'r') as source_file:
            source_content = source_file.read()
        with open(dest_path, 'w') as dest_file:
            dest_file.write(source_content)
        return True  # Successfully copied
    except FileNotFoundError:
        logging.info(f"Error: {source_path} not found.")
        if Config.sast_ignore_folders_and_files is not None:
            with open(dest_path, 'w') as dest_file:
                for string in Config.sast_ignore_folders_and_files:
                    dest_file.write(string + "\n")
            return True 
            
        return False  # Source file not found
