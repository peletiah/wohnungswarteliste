import logging
import datetime
from sqlalchemy import and_

from wohnungswarteliste.lib.base import *

log = logging.getLogger(__name__)

class WartelisteController(BaseController):

   def index(self):
      try:
         newapplicant=model.applicants()
         newapplicant.firstname=request.params['firstname']
         newapplicant.lastname=request.params['lastname']
         newapplicant.ais=request.params['ais']
         newapplicant.birthdate=request.params['birthdate']
         newapplicant.origin=request.params['origin']
         newapplicant.contact=request.params['contact']
         newapplicant.comment=request.params['comment']
         model.Session.save(newapplicant)
         model.Session.commit()
         q = model.Session.query(model.applicants)
         c.applicants = q.limit(10)
         redirect_to(controller='warteliste', action='index')
      except KeyError:
         q = model.Session.query(model.applicants)
         c.applicants = q.limit(10)
         return render("/warteliste/index.html")

   def change(self,id):
      q = model.Session.query(model.applicants).filter(model.applicants.id==id)
      c.applicant = q.one()
      return render("/warteliste/change.html")

   def update(self,id):
      q=model.Session.query(model.applicants)
      applicant=q.filter(model.applicants.id==id).one()
      applicant.firstname=request.params['firstname']
      applicant.lastname=request.params['lastname']
      applicant.ais=request.params['ais']
      applicant.birthdate=request.params['birthdate']
      applicant.origin=request.params['origin']
      applicant.contact=request.params['contact']
      applicant.comment=request.params['comment']
      model.Session.update(applicant)
      model.Session.commit()
      redirect_to(controller='warteliste', action='index', id='')
     
   def presence(self,id):
      q=model.Session.query(model.presence)
      if q.filter(and_(model.presence.date==datetime.date.today(),model.presence.applicants==id)).count() >= 1:
         redirect_to(controller='warteliste', action='index', id='')
      else:
         presence=model.presence()
         presence.applicants=id
         model.Session.save(presence)
         model.Session.commit()
         redirect_to(controller='warteliste', action='index', id='')

   def details(self,id):
      q=model.Session.query(model.applicants)
      c.applicant=q.filter(model.applicants.id==id).one()
      q2=model.Session.query(model.presence)
      c.presence=q2.filter(model.presence.applicants==id).all()
      return render("/warteliste/details.html") 
