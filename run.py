#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
# Run a test server.
#from app import app
#from app.routes.church import *
from app.routes.index import *
from app.routes.user import *
from app.routes.church import *
from app.routes.paper import *
#app = Flask('psalm')

if __name__ == '__main__':
    # app.logger.debug('test'+__name__)
    # app.logger.debug('testdddddddddddd')
    # print (__name__)
    # print (app.root_path)
    # print (app.import_name)
    app.run(host='0.0.0.0', debug=True)
