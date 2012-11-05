from google.appengine.ext import db

class cust_account(db.Model):
    """Models each user accounts having unique userID and Mobile number."""
    UserID       = db.StringProperty(indexed=True)
    Username     = db.StringProperty(indexed=True)
    Password     = db.StringProperty()
    Mobile       = db.StringProperty(indexed=True)
    LastMobile   = db.StringProperty(indexed=True)
    Firstname    = db.StringProperty()
    Lastname     = db.StringProperty()
    Email        = db.EmailProperty(indexed=True)
    Sex          = db.StringProperty()
    Age          = db.IntegerProperty()
    City         = db.StringProperty()
    DOB          = db.DateProperty()
    LogFlag      = db.BooleanProperty()
    LoggedOn     = db.DateTimeProperty()
    LogValidity  = db.IntegerProperty()
    VerifyID     = db.IntegerProperty()
    VerifyFlag   = db.BooleanProperty()
    EmailFlag    = db.BooleanProperty()
    CreatedOn    = db.DateTimeProperty(auto_now_add=True)
    UpdatedOn    = db.DateTimeProperty(auto_now=True)
