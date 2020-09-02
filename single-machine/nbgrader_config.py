import os
from nbgrader.auth import JupyterHubAuthPlugin

c = get_config()
#c.CourseDirectory.root = os.path.abspath('/home/admin/Klausur/')
#c.CourseDirectory.course_id = 'Klausur'

c.Exchange.path_includes_course = True
c.Authenticator.plugin_class = JupyterHubAuthPlugin
c.Exchange.root = '/srv/nbgrader/exchange'
c.ExecutePreprocessor.timeout = 3600
