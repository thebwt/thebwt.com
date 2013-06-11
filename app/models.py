from app import collection

from werkzeug.exceptions import NotFound

Users = collection["users"]

ROLE_USER = 0
ROLE_ADMIN = 1

def getUserByNick(userid):
    spec = {
        "email": userid
    }
    return Users.find_one(spec)

class Resource(object):

    def GET(self, request, **kwargs):
        return NotImplemented()

    def HEAD(self, request, **kwargs):
        return NotImplemented()

    def POST(self, request, **kwargs):
        return NotImplemented()

    def DELETE(self, request, **kwargs):
        return NotImplemented()

    def PUT(self, request, **kwargs):
        return NotImplemented()

    def __call__(self, request, **kwargs):
        handler = getattr(self, request.method)
        return handler(request, **kwargs)

class User(Resource):
    
    def __init__(self, id):
        self.doc = Users.find_one({'email':id})
        self.nickname = self.doc['nickname']
    
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        if self.doc:
            return self.doc['email']
        return None
        
    def GET(self, request, userid):
        doc = getUserByNick(userid)
        if not doc:
            return NotFound
        return doc
        
        
    def PUT(self, request, userid):
        doc = getUserByNick(userid)
        if not doc:
            return NotFound
        return doc
        
    def POST(self, request, userid):
        pass
    
    def __repr__(self):
        return '<User %r>' % (self.nickname)
        
