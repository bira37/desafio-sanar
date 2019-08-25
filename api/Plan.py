from app import db

#Modelo de tabela dos planos 
class Plan(db.Model):
    __bind__ = 'plan_db'
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(255))
    mundi_plan_id = db.Column(db.String(255))
    
    def __init__(self, id="", name="", mundi_plan_id=""):
      self.id = id
      self.name = name
      self.mundi_plan_id = mundi_plan_id
      
    def __repr__(self):
        return "<Plan Name: {}>".format(self.name)
