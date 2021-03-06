#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'app', 'coheoka'))

from app import create_app, db
from app.models import Essay
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from coheoka.coherence_probability import ProbabilityVector  # NOQA
from coheoka.evaluator import Evaluator  # NOQA

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Essay=Essay)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
