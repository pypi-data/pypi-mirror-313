# CRUD APIs for model objects
# Each object must have create/read/update/delete methods
from datetime import datetime
from .models import Candidate, JobDescription, Interview, Questionnaire, CVEvaluation
from klabmodels.kiwi.api import read_company_by_name
from typing import Dict, List
from functools import partial
from pydantic import EmailStr
import logging
import time


### Job Descriptions/Vacancies
def create_vacancy(reference: str, title: str, company_name: str, **kwargs):
   try:
      if 'job_title' in kwargs: kwargs.pop('job_title', None)
      jd = JobDescription(reference=reference, job_title=title, company=company_name, **kwargs)
      jd.save()
      return jd
   except Exception as e:
      logging.error(f"Failed to create vacancy: {str(e)}")

def read_vacancy(vacancy_pk: str):
   try:
      vacancy = JobDescription.find(JobDescription.pk==vacancy_pk).first()
      logging.info(f"Vacancy {vacancy_pk} found")
      return vacancy
   except Exception:
     logging.error(f"Vacancy {vacancy_pk} not found.")


def read_vacancy_by_reference(reference: str):
   try:
      vacancy = JobDescription.find(JobDescription.reference==reference).first()
      logging.info(f"Vacancy with reference {reference} found")
      return vacancy
   except Exception:
     logging.error(f"Vacancy with reference {reference} not found.")


def read_vacancy_by_company(company: str):
   # Will return a list of vacancies 

   vacancies = JobDescription.find(JobDescription.company==company).all()
   if vacancies:
      logging.info(f"Found {len(vacancies)} for company {company}")
      return vacancies
   else:
     logging.error(f"No vacancy found for company {company}.")


def update_vacancy(pk: str, **kwargs):
   """
   Update a job description
   """
   try:
      jd = read_vacancy(pk)
      logging.info(f"Found job: {jd.reference}")
      if kwargs: 
         jd.__dict__.update(kwargs)
         jd.save()
         return jd
   except Exception as e:
      logging.info(f"Error updating vacancy {pk}: {str(e)}")

# Special case to make a vacancy inactive
make_vacancy_inactive = partial(update_vacancy, active=False, closed=time.time())


def toggle_vacancy(pk: str, **kwargs):
   """
   Toggle vacancy active status
   """
   try:
      jd = read_vacancy(pk)
      logging.info(f"Found job: {jd.reference}")
      jd.active = not(jd.active)
      jd.save()
   except Exception as e:
      logging.error(f"Error toggling vacancy status {pk}: {str(e)}")

def delete_vacancy(pk: str):

   # We do not want to actually delete it, just mark inactive
   try:
      jd = read_vacancy(pk)
      logging.info(f"Found job: {jd.reference}")
      if jd.active: 
         jd.active = False
         jd.save()
   except Exception as e:
      logging.error(f"Error toggling vacancy status {pk}: {str(e)}")
   
   """
   try:
      vacancy = read_vacancy(pk)
      if vacancy:
         vacancy.delete(pk)
         # The candidate references have to be removed too if they applied for these vacancies
         candidates = get_candidates_by_job(pk)
         for c in candidates:
            c .jobs_applied.remove(pk)
         c.save()

         return True
   except Exception as e:
      logging.error(f"Cannot delete vacancy. No vacancy {pk} found.")
   """
   


### Candidates APIs

def create_candidate(name:str, resume:str, **kwargs):
   """
   Create a new candidate object
   """
   try:
      c = Candidate(name=name, resume=resume, **kwargs)
      c.save()
      return c
   except Exception as e:
      logging.error(f"Failed to create candidate: {str(e)}")
   
def read_candidate(candidate_pk: str):
   try:
      candidate = Candidate.find(Candidate.pk==candidate_pk).first()
      logging.info(f"Candidate {candidate_pk} found")
      return candidate
   except Exception:
     logging.error(f"Candidate {candidate_pk} not found.")

def read_candidate_by_name(name: str):
   # Name is not necesarily unique, therefore returns a list
   candidates = Candidate.find(Candidate.name==name).all()
   if candidates:
      logging.info(f"Found {len (candidates)} candidates with name {name}")
      return candidates
   else:
     logging.error(f"No candidate named {name} not found.")


# This can be used to look for duplicated candidates
def read_candidate_by_pi(name: str, email:str):
   """
   Look for candidates usinf personal information like name and email
   """
   candidates = Candidate.find(Candidate.name==name).all()
   if candidates:
      samecandidates = [c for c in candidates if c.email==email]
      if samecandidates:
         logging.info(f"Candidate {samecandidates[0].name} found.")
         return samecandidates[0]
      
def read_candidate_by_email(email:str):
   """
   Look for candidates by email
   """
   candidates = Candidate.find().all()
   if candidates:
      samecandidates = [c for c in candidates if c.email==email]
      if samecandidates:
         logging.info(f"Candidate {samecandidates[0].name} found.")
         return samecandidates[0]


def update_candidate(pk:str, **kwargs):
   """
   Persist a candidate (create or update)
   Although there is an index on the name, that is not necessarily unique
   So the only unique value is the pk
   """
   try:
      c = Candidate.find(Candidate.pk==pk).first()
      if kwargs: 
         c.__dict__.update(kwargs)
         c.save()
      return c
   except Exception as e:
      logging.info(f"Error updating candidate {pk}: {str(e)}")
   

def delete_candidate(pk: str):
   try:
      candidate = read_candidate(pk)
      if candidate:
         candidate.delete(pk)
         logging.info(f"Candidate {pk} deleted.")
         return True
   except Exception as e:
      logging.error(f"Cannot delete candidate. No candidate {pk} found.")

# Other APIs    
def get_candidates_by_job(job_reference_pk: str):
   """
   Get candidates who have applied for a specific job
   """
  
   try:
      candidates = Candidate.find().all()
      if candidates:
        #candidates = [c for c in candidates if c.resume_classified] # CV has been processed
        candidates = [c for c in candidates if job_reference_pk in c.jobs_applied] # Has applied for the job
        if candidates:
          return candidates
        else:
           logging.error(f"No candidates retrieved for the job position {job_reference_pk}.")    
      else:
         logging.error(f"No candidates retrieved.")
   except Exception as e:
    logging.error(f"No candidates retrieved: {str(e)}")
    return None
   

def get_candidates_by_company(company: str):
   """
   Get candidates who have applied for jobs at the company
   Args:
      company (str): company name
   """
   #user = cl.user_session.get("account")
   try:
      candidates = Candidate.find().all()
      jobs = read_vacancy_by_company(company)
      if jobs:
         jobrefs = set([j.pk for j in jobs])
         #candidates = [c for c in candidates if c.resume_classified] # CV has been processed
         candidates = [c for c in candidates if set(c.jobs_applied) & jobrefs] # Has applied for jobs at the company
         if candidates:
            return candidates
         else:
           logging.error(f"No candidates retrieved for the job positions at  {company}.")    
      else:
         logging.error(f"No jobs advertised at company {company}.")
   except Exception as e:
    logging.error(f"No candidates retrieved.")
   return None


def apply_for_a_job(candidate_pk:str, job_pk: str):
  """
  A candidate applies for a job
  """

  try:
    candidate = read_candidate(candidate_pk)
    if candidate:
       if job_pk not in candidate.jobs_applied:
         candidate.jobs_applied.append(job_pk)
         candidate.save()
         logging.info(f"Candidate {candidate_pk} job application for job {job_pk} submitted.")
    else:
      logging.error(f"Candidate {candidate_pk} already applied for job {job_pk}, skipped...")
  except Exception:
   logging.error(f"Candidate {candidate_pk} not found.")

def rectract_job_application(candidate_pk:str, job_pk: str):
  """
  A candidate applies for a job
  """

  try:
    candidate = read_candidate(candidate_pk)
    if candidate:
       if job_pk in candidate.jobs_applied:
         candidate.jobs_applied.remove(job_pk)
         candidate.save()
         logging.info(f"Candidate {candidate_pk} job application for job {job_pk} removed.")
    else:
      logging.error(f"Candidate {candidate_pk} has not applied for job {job_pk}, skipped...")
  except Exception:
   logging.error(f"Candidate {candidate_pk} not found.")


### Interviews

def create_interview(job: JobDescription, candidate: Candidate, **kwargs):
    """
    Save Interview questionnaire creation to Redis DB
    Args:
      job: (JobDescription) Job Description
      candidate: (Candidate) name and resume
      kwargs: other attributes

    Returns: 
      interview:  interview id to be used to generate a link for the candidate interview
    """
    try:
       interview = Interview( 
                  date=time.time(), 
                  candidate=candidate.pk, 
                  job_description=job.pk,
                  **kwargs
                  )
       interview.save()
       return interview
    except Exception as e:
      logging.error(f"Failed to create interview: {str(e)}")


def read_interview(interview_pk: str):
   try:
      interview = Interview.find(Interview.pk==interview_pk).first()
      logging.info(f"Interview {interview_pk} found")
      return interview
   except Exception:
     logging.error(f"Interview {interview_pk} not found.")


def update_interview(interview_pk: str, **kwargs):
    """
    Save interview conversation into Interview object (existing)
    """
    #user = cl.user_session.get("account")
    try:
      interview = read_interview(interview_pk)
      if 'dialogue' in kwargs:
         dialogue = kwargs['dialogue'] 
         interview.interview = [msg for msg in dialogue if msg['role'] in ('user', 'assistant')]
         del kwargs['dialogue']
      if kwargs: interview.__dict__.update(kwargs)
      interview.save()
      logging.info(f"Interview saved for {interview.candidate}")
      return interview
    except Exception as e:
       logging.error(f"Error updating interview: {str(e)}")

def delete_interview(interview_pk: str):
   # TODO must delete references in the candidate object too
   pass

def read_interview_by_candidate(candidate_pk: str):
  """
  Retrieves stored interview(s) for a candidate
  """
  logging.info(f"Looking for candidate {candidate_pk} interviews... ")
  interviews = Interview.find(Interview.candidate==candidate_pk).all()
  if interviews: 
     return interviews
  else:
    logging.error(f"No interview found for Candidate {candidate_pk}.")


def read_interview_by_tenant_candidate(candidate_pk: str, tenant: str):
  """
  Retrieves stored interview(s) for a candidate
  """
  logging.info(f"Looking for candidate {candidate_pk} interviews... ")
  candidate_itws = []
  try:
   interviews = Interview.find(Interview.candidate==candidate_pk).all()
   if interviews:
      interviews = [i for i in interviews if read_company_by_name(read_vacancy(i.job_description).company).tenant == tenant]
      return interviews
   else:
      logging.error(f"No interview found for Candidate {candidate_pk}.")
  except Exception as e:
     logging.error(f"Error while retrieving candidate interviews: {str(e)}")

def read_interview_by_company_candidate(candidate_pk: str, company: str):
  """
  Retrieves stored interview(s) for a candidate
  """
  logging.info(f"Looking for candidate {candidate_pk} interviews... ")
  candidate_itws = []
  try:
   interviews = Interview.find(Interview.candidate==candidate_pk).all()
   if interviews:
      interviews = [i for i in interviews if read_company_by_name(read_vacancy(i.job_description)).name == company]
      return interviews
   else:
      logging.error(f"No interview found for Candidate {candidate_pk}.")
  except Exception as e:
     logging.error(f"Error while retrieving candidate interviews: {str(e)}")


def read_interview_by_vacancy(vacancy_pk: str):
  """
  Retrieves stored interview
  """
  logging.info(f"Looking for interviews related to {vacancy_pk} job desscriptions... ")
  interviews = Interview.find(Interview.job_description==vacancy_pk).all()
  if interviews:
     return interviews
  else:
     logging.error(f"No interview found for vacancy {vacancy_pk}.")
    

def read_interview_by_vacancy_and_candidate(vacancy_pk: str, candidate_pk: str):
  """
  Retrieves stored interview
  """
  logging.info(f"Looking for interviews related to vacancy {vacancy_pk} and candidate {candidate_pk} ")
  interviews = Interview.find(Interview.job_description==vacancy_pk and Interview.candidate==candidate_pk).all()
  if interviews:
     return interviews[0]
  else:
     logging.error(f"No interview found for candidate {candidate_pk} on vacancy {vacancy_pk}.")

def interview_completed_by_candidate(candidate_email: str, vacancy_pk: str):
   """
   Returns: True if a candidate as already submitted an interview for a position

   """

   candidate = read_candidate_by_email(candidate_email)
   if candidate:
      interview = read_interview_by_vacancy_and_candidate(vacancy_pk, candidate.pk)
      if interview and interview.interview:
         return True
   return False






### CV Evaluations

def create_cv_evaluation(candidate_pk: str, 
                         evaluation: Dict,
                         **kwargs):
   """
   Store a CV evaluation grading and summary on Redis
   """

   try:
      cv_evaluation = CVEvaluation(candidate=candidate_pk,
                                      date=time.time(), 
                   company=kwargs.get('company') if 'company' in kwargs else "",
                   jobdesc=kwargs.get('jobdesc') if 'jobdesc' in kwargs else "",
                   **evaluation
                   )
      cv_evaluation.save()
      return cv_evaluation
   except Exception as e:
         logging.error(f"Failed to create CV evaluation for candidate {candidate_pk}: {str(e)}")



def read_cv_evaluation(pk: str):
   try:
      cv_evaluation = CVEvaluation.find(CVEvaluation.pk==pk).first()
      logging.info(f"CV Evaluation {pk} found")
      return cv_evaluation
   except Exception:
     logging.error(f"CV Evaluation {pk} not found.")

def read_cv_evaluation_by_candidate(candidate_pk: str, company: str=None, jobdesc: str=None):
      """
      Returns most recent cv evaluation for a candidate
      Args:
      candidate_pk
      company: company name
      jobdesc: jobdesc pk
      """
      evaluations = CVEvaluation.find(CVEvaluation.candidate==candidate_pk).all()
      if evaluations:
         if company and jobdesc: 
            # Evaluations have company name not pk
            evaluations = [e for e in evaluations if e.company.casefold()==company.casefold() and e.jobdesc==jobdesc]
         elif company:
            evaluations = [e for e in evaluations if e.company.casefold()==company.casefold()]
         elif jobdesc:
            evaluations = [e for e in evaluations if e.jobdesc==jobdesc]
         if evaluations:
            #e_last = max(evaluations, key=lambda x: x.date)
            #logging.info(f"CV Evaluation {e_last.pk} found")
            return evaluations
            #return e_last
      
      logging.error(f"CV Evaluation not found for candidate {candidate_pk}.")


def update_cv_evaluation(pk: str, **kwargs):
   try:
      cv_eval = read_cv_evaluation(pk)
      if kwargs: 
         cv_eval.__dict__.update(kwargs)
         cv_eval.save()
         logging.info(f"CV Evaluation {pk} updated")
         return cv_eval
   except Exception as e:
       logging.error(f"Error updating CV Evaluation: {str(e)}")



def delete_cv_evaluation(pk: str):
   try:
      cv_eval = read_cv_evaluation(pk)
      if cv_eval: 
         cv_eval.delete()
         logging.info(f"CV Evaluation {pk} deleted")
   except Exception as e:
       logging.error(f"Error deleting CV Evaluation: {str(e)}")

   



