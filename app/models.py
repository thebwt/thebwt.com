from app import collection

Users = collection["users"]

ROLE_USER = 0
ROLE_ADMIN = 1

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
        
    def __getitem__(self, key):
        return self.doc[key]
        
    def __setitem__(self, key, value):
        self.doc[key]=value
        
    def __repr__(self):
        return '<User %r>' % (self.nickname)
        
