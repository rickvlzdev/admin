import sys
import unittest
from flask.cli import FlaskGroup
from project import create_app, db
from project.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
  db.drop_all()
  db.create_all()
  db.session.commit()

@cli.command()
def test():
  """Runs the tests without code coverage"""
  tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
  result = unittest.TextTestRunner(verbosity=2).run(tests)
  if result.wasSuccessful():
    return 0
  sys.exit(result)

@cli.command('seed_db')
def seed_db():
  """Seeds the database."""
  michael = User(username='michael', email='michael@gmail.com')
  michael.set_password('michael_password')
  martha = User(username='martha', email='marth@yahoo.com')
  martha.set_password('martha_password')
  db.session.add(michael)
  db.session.add(martha)
  db.session.commit()

if __name__ == '__main__':
  cli()