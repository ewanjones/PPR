#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/PPR/")

from ppr_app.PPR import app as application
application.secret_key = 'devkey1'
