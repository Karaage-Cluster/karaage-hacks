#!/bin/sh

qmgr -c 'create hook RequireProject'
qmgr -c 'set hook RequireProject event = queuejob'
qmgr -c 'import hook RequireProject application/x-python default require_project.py'
