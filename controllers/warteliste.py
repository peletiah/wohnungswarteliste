import logging
import datetime
import re
from sqlalchemy import and_

from wohnungswarteliste.lib.base import *

log = logging.getLogger(__name__)

class WartelisteController(BaseController):

   def index(self):
      try:
         newapplicant=model.applicants()
         birthdate=request.params['birthdate']
         datePattern = re.compile(r'^(\d{2})\.(\d{2})\.(\d{4})$')
         date=datePattern.search(birthdate)
         if date:
            newapplicant.birthdate=date.groups()[2]+'-'+date.groups()[1]+'-'+date.groups()[0]
         else:
            newapplicant.birthdate=birthdate
         newapplicant.firstname=request.params['firstname']
         newapplicant.lastname=request.params['lastname']
         newapplicant.ais=request.params['ais']
         newapplicant.origin=request.params['origin']
         newapplicant.contact=request.params['contact']
         newapplicant.comment=request.params['comment']
         model.Session.save(newapplicant)
         model.Session.commit()
         q = model.Session.query(model.applicants)
         c.applicants = q.all()
         redirect_to(controller='warteliste', action='index')
      except KeyError:
         q = model.Session.query(model.applicants)
         c.applicants = q.all()
         return render("/warteliste/index.html")

   def change(self,id):
      q = model.Session.query(model.applicants).filter(model.applicants.id==id)
      c.applicant = q.one()
      q = model.Session.query(model.presence).filter(model.presence.applicants==id)
      c.presence = q.all()
      return render("/warteliste/change.html")

   def update(self,id):
      q=model.Session.query(model.applicants)
      applicant=q.filter(model.applicants.id==id).one()
      applicant.firstname=request.params['firstname']
      applicant.lastname=request.params['lastname'].upper()
      applicant.ais=request.params['ais']
      birthdate=request.params['birthdate']
      datePattern = re.compile(r'^(\d{2})\.(\d{2})\.(\d{4})$')
      date=datePattern.search(birthdate)
      if date:
         applicant.birthdate=date.groups()[2]+'-'+date.groups()[1]+'-'+date.groups()[0]
      else:
         applicant.birthdate=birthdate
      applicant.origin=request.params['origin']
      applicant.contact=request.params['contact']
      applicant.comment=request.params['comment']
      model.Session.update(applicant)
      i=1
      while i < 50:
         try:
            date=request.params['date'+str(i)]
            if date:
               q=model.Session.query(model.presence)
               presence=model.presence()
               presence.applicants=id
               datePattern = re.compile(r'^(\d{2})\.(\d{2})\.(\d{4})$')
               datematch=datePattern.search(date)
               if datematch:
                  presence.date=datematch.groups()[2]+'-'+datematch.groups()[1]+'-'+datematch.groups()[0]
               else:
                  presence.date=date
               model.Session.save(presence)
            i=i+1
         except KeyError, (message):
            i=i+1
      model.Session.commit()
      redirect_to(controller='warteliste', action='index', id='')
     
   def presence(self,id):
      q=model.Session.query(model.presence)
      if q.filter(and_(model.presence.date==str(datetime.date.today())+' 00:00:00',model.presence.applicants==id)).count() >= 1:
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
      q=model.Session.query(model.presence)
      c.presence=q.filter(model.presence.applicants==id).all()
      return render("/warteliste/details.html") 
