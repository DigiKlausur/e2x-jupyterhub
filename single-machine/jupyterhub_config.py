import os
import sys
import pandas as pd

c = get_config()
c.JupyterHub.ip = u'IP'
c.JupyterHub.port = PORT
c.JupyterHub.ssl_key = "/etc/jupyter/e2x-key.pem"
c.JupyterHub.ssl_cert = "/etc/jupyter/e2x-certificate.pem"

c.JupyterHub.cookie_secret_file = u'/srv/jupyterhub/jupyterhub_cookie_secret'
c.JupyterHub.db_url = u'/srv/jupyterhub/jupyterhub.sqlite'
c.ConfigurableHTTPProxy.auth_token = u'/srv/jupyterhub/proxy_auth_token'

#c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
# LDAP authenticator
c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.Authenticator.server_address = 'ldap.infcs.de'
c.Authenticator.bind_dn_template = ["uid={username},ou=staff,dc=fb02,dc=fh-bonn-rhein-sieg,dc=de"
                                    ,"uid={username},ou=students,dc=fb02,dc=fh-bonn-rhein-sieg,dc=de"]
c.Authenticator.use_ssl = True
c.Authenticator.server_port = 636

c.Authenticator.create_system_users = True

USER_ENV_PREFIX  = "/opt/e2x/envs/e2x"
c.SystemdSpawner.extra_paths = [os.path.join(USER_ENV_PREFIX, 'bin')]

# Allow admin to access single user hub
c.JupyterHub.admin_access = True

# Admin users
c.Authenticator.admin_users = {'e2x-admin', 'mwasil2m', 'tmetzl2m'}

# Load the allowlist
allowlisted_users = {'e2x-admin'}

# Update allowlist
allowlist_dir = "/etc/jupyter/allowlist"
if os.path.isdir(allowlist_dir):
    allowlist_files = [csv_file for csv_file in os.listdir(allowlist_dir) if os.path.splitext(csv_file)[1] == ".csv"]
else:
    print ("{} is not a directory".format(allowlist_dir))
    allowlist_files = []

print ("Found ",len(allowlist_files), " allowlist files")
print (allowlist_files)

for i,csv_file in enumerate(allowlist_files):
   csv_path = os.path.join(allowlist_dir, csv_file)
   session_pd = pd.read_csv(csv_path)
   for username in session_pd.Username:
      allowlisted_users.add(username)

c.Authenticator.allowlist = allowlisted_users
c.Authenticator.ldap_allowlist = allowlisted_users
print ("{} users added to allowlist".format(len(allowlisted_users)))
print ("Whitelist: ", allowlisted_users)

# Add the to blocklist, work with jhub 0.9.0 above
blocklist_dir = "/etc/jupyter/blocklist"
if os.path.isdir(blocklist_dir):
    blocklist_files = [csv_file for csv_file in os.listdir(blocklist_dir) if os.path.splitext(csv_file)[1] == ".csv"]
else:
    print ("{} is not a directory".format(blocklist_dir))
    allowlist_files = []

print ("Found ",len(blocklist_files), " blocklist files")
print (blocklist_files)

blocklisted_users = set()
for i,csv_file in enumerate(blocklist_files):
   csv_path = os.path.join(blocklist_dir, csv_file)
   session_pd = pd.read_csv(csv_path)
   for username in session_pd.Username:
      blocklisted_users.add(username)

c.Authenticator.blocklist = blocklisted_users
print ("{} users added to blocklist".format(len(blocklisted_users)))

#Enable check account to make black- and allowlist work
c.Authenticator.check_account = True

# SystemD spawner
c.SystemdSpawner.spawner_class = 'systemdspawner.SystemdSpawner'

# Limit memory and cpu usage
#c.SystemdSpawner.mem_limit = '6G'
#c.SystemdSpawner.cpu_limit = 4.0

c.SystemdSpawner.isolate_tmp = True
c.SystemdSpawner.isolate_devices = True

# ser default_shell
c.SystemdSpawner.default_shell = '/bin/false'

# All users should have local accounts
c.SystemdSpawner.dynamic_users = False
c.SystemdSpawner.disable_user_sudo = True

# Watch do for nbgrader exchange
#c.JupyterHub.services = [
#    {
#        'name': 'nbgrader-watch-dog',
#        'url': 'http://127.0.0.1:15142',
#        'command': [sys.executable, '/home/mwasil2s/envs/jupyterhub-services/watch_nbgrader_inbound_directory.py'],
#    }
#]

#c.JupyterHub.services = [
#    {
#        'name': 'submit-service',
#        'url': 'http://127.0.0.1:50000',
#        'command': [sys.executable, '/home/mwasil2s/repositories/simple-multiclients-http-server/simple_https_server.py'],
#    }
#]


# Shared grading services config
# all users have to be added to the group allowlist
#c.Authenticator.group_allowlist = {'nn-instructors', 'itr-instructors'}

# add instructors to the corresponding course group
# The group should be named <formgrade-{}> {}=course_id
# <nbgrader-{}> {}=course_id is the student list that has access to the course
c.JupyterHub.load_groups = {
    'formgrade-WuS-WS1920': ['wus-course','mwasil2m'],
    'formgrade-NLP-SS20': ['nlp-course','mwasil2m'],
    'formgrade-RP-SS20': ['rp-course','mwasil2m'],
    'formgrade-K8s-SS20': ['k8s-course','mwasil2m'],
    'formgrade-MRC-Exam': ['mrc-exam','mwasil2m' ],
    'formgrade-RP-Exam': ['rp-exam','mwasil2m'],
    'formgrade-WuS-Klausur': ['wus-klausur','mwasil2m'],
    'formgrade-ITR-Klausur': ['itr-klausur','mwasil2m'],
    'nbgrader-WuS-WS1920': ['wus-course'],
    'nbgrader-NLP-SS20': ['nlp-course'],
    'nbgrader-RP-SS20': ['rp-course'],
    'nbgrader-K8s-SS20': ['k8s-course'],
    'nbgrader-MRC-Exam': ['mrc-exam'],
    'nbgrader-RP-Exam': ['rp-exam'],
    'nbgrader-WuS-Klausur': ['wus-klausur'],
    'nbgrader-ITR-Klausur': ['itr-klausur'],
}

# Start the notebook server of the course as a service
admin_token = TOKEN_HERE
c.JupyterHub.services = [
    {
        'name': 'WuS-WS1920',
        'url': 'http://127.0.0.1:3333',
        'command': ['jupyterhub-singleuser','--group=formgrade-WuS-WS1920','--debug',],
        'user': 'wus-course',
        'cwd': '/home/wus-course/WahrscheinlichkeitstheorieUndStatistik',
	      'api_token': admin_token
    },
    {
        'name': 'NLP-SS20',
        'url': 'http://127.0.0.1:2323',     
        'command': ['jupyterhub-singleuser','--group=formgrade-NLP-SS20','--debug',], 
        'user': 'nlp-course',  
        'cwd': '/home/nlp-course/NLP',
	      'api_token': admin_token
    },
    {
        'name': 'RP-SS20',
        'url': 'http://127.0.0.1:5555',     
        'command': ['jupyterhub-singleuser','--group=formgrade-RP-SS20','--debug',], 
        'user': 'rp-course',  
        'cwd': '/home/rp-course/RobotPerception',
	      'api_token': admin_token
    },
    {
        'name': 'K8s-SS20',
        'url': 'http://127.0.0.1:6666',     
        'command': ['jupyterhub-singleuser','--group=formgrade-K8s-SS20','--debug',], 
        'user': 'k8s-course',  
        'cwd': '/home/k8s-course/K8s-Course',
	      'api_token': admin_token
    },
    {
        'name': 'MRC-Exam',
        'url': 'http://127.0.0.1:9797',     
        'command': ['jupyterhub-singleuser','--group=formgrade-MRC-Exam','--debug',], 
        'user': 'mrc-exam',  
        'cwd': '/home/mrc-exam/MRC',
	      'api_token': admin_token
    },
    {
        'name': 'RP-Exam',
        'url': 'http://127.0.0.1:9999',     
        'command': ['jupyterhub-singleuser','--group=formgrade-RP-Exam','--debug',], 
        'user': 'rp-exam',  
        'cwd': '/home/rp-exam/RobotPerception',
	      'api_token': admin_token
    },
    {
        'name': 'WuS-Klausur',
        'url': 'http://127.0.0.1:3333',     
        'command': ['jupyterhub-singleuser','--group=formgrade-WuS-Klausur','--debug',], 
        'user': 'wus-klausur',  
        'cwd': '/home/wus-klausur/WuS',
	      'api_token': admin_token
    },
    {
        'name': 'ITR-Klausur',
        'url': 'http://127.0.0.1:4444',     
        'command': ['jupyterhub-singleuser','--group=formgrade-ITR-Klausur','--debug',], 
        'user': 'itr-klausur',  
        'cwd': '/home/itr-klausur/IT-Recht',
	      'api_token': admin_token
    },

]

c.JupyterHub.services.append(
        {
            'name': 'cull-idle',
            'admin': True,
            'command': [sys.executable, '/etc/jupyter/cull_idle_servers.py', '--timeout=3600'],
        }
  )


