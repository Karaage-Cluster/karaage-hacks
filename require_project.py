__author__ = 'brian'

import sys
my_paths = [
    '/usr/local/pbs/default/python/lib/python2.5',
    '/usr/local/pbs/default/python/lib/python2.5/plat-linux2',
    '/usr/local/pbs/default/python/lib/python2.5/lib-tk',
    '/usr/local/pbs/default/python/lib/python2.5/lib-dynload',
    '/usr/local/pbs/default/python/lib/python2.5/site-packages',
]

for my_path in my_paths:
    if my_path not in sys.path:
        sys.path.append(my_path)

if "/usr/lib64/python2.6" in sys.path:
    sys.path.remove("/usr/lib64/python2.6")

import encodings.ascii

import pbs

try:
    # Python 3
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser

try:
    # Python 3
    import xmlrpc.client as xmlrpclib
except ImportError:
    # Python 2
    import xmlrpclib

e = pbs.event()
try:

    config_file = "/etc/karaage3/karaage-cluster-tools.cfg"

    f = open(config_file, "r")
    f.close()

    config = configparser.RawConfigParser()
    config.read(config_file)

    username = config.get('karaage', 'username')
    password = config.get('karaage', 'password')
    url = config.get('karaage', 'url')

    server = xmlrpclib.Server(url)

    if e.job.project is None:
        e.reject(
            "The project has not been supplied. Please specify project with '-P <project>'.")
    project = str(e.job.project)

    members = server.get_project_members(username, password, project)
    if isinstance(members, str):
        e.reject(
            "The project %s is invalid." % project)

    if e.requestor not in members:
        e.reject(
            "User %s is not a member of project %s." % (e.requestor, project))

    assert "," not in project
    e.job.group_list = pbs.group_list(project)

except SystemExit:
    pass

except:
    import traceback
    # traceback.print_exc()
    e.reject(
        "%s hook failed with %s. Please contact Admin." % (e.hook_name, sys.exc_info()[:2]))