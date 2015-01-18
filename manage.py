#!/usr/bin/env python3
# imports go here
import os

#
# Free Coding session for 2015-01-13
# Written by Matt Warren
#

if os.path.isfile('.env'):
    for line in open('.env'):
        line = line.split('=')
        if len(line) == 2:
            os.environ[line[0]] = line[1]


from app import create_app, db
from app.models import User, Role, Nag, NagEntry
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Shell, Manager

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, User=User, Role=Role, db=db, Nag=Nag, NagEntry=NagEntry)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('migrate', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
