from src.sessions.environment import env
from src.sessions.session import Session


domain = env['SERVER']['domain']

routes = {
    'INDEX' : '/',
    'SIGNIN': '/signin',
    'AUTHORIZE': '/authorize',
    'REVOKE': '/revoke',
    'SIGNINFULLPATH': domain + '/signin'
}

session = Session()