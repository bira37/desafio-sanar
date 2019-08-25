from app import db

#Modelo de tabela do usuario 
class User(db.Model):
    __bind__ = 'user_db'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    plan_name = db.Column(db.String(255))
    mundi_customer_id = db.Column(db.String(80))
    mundi_subscription_id = db.Column(db.String(80))
    def __init__(self, name="", plan_name="", mundi_customer_id="", mundi_subscription_id=""):
      self.name = name
      self.plan_name = plan_name
      self.mundi_customer_id = mundi_customer_id
      self.mundi_subscription_id = mundi_subscription_id
      
    def __repr__(self):
        return "<ID: {}>".format(self.id)
