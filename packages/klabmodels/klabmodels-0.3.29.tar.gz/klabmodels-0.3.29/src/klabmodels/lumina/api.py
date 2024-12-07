from .models import Chat, ChatMessage, Session, StatementOfWork, Invitation, Question, Split, Course
from typing import List, Dict
from datetime import datetime, timezone
import logging
import os
import uuid
from openai import OpenAI

import tiktoken
MAX_SUMMARY_TOKENS = 4096

def ntokens(string: str, encoding_name: str="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

######## Chats ########
def save_chat(user: str, agent: str, msgs:List[Dict]):
  """
  Save a new chat
  """
  try:
    chat_messages =[ChatMessage(role=msg['role'], content=msg['content']) for msg in msgs if msg['role']!='system']
    chat = Chat(user=user, agent=agent, msgs=chat_messages, ts=datetime.now())
    summary = summarize_chat(chat)
    chat.summary = summary.content
    chat.save()
    return chat
  except Exception as e:
    logging.error(f"Failed to save chat: {str(e)}")
    raise e
  

def students_chats(agent: str=None):
   """
   Return list of students chats
   """
   chats = Chat.find().all()
   if agent: chats = [chat for chat in chats if chat.agent==agent]
   chats = sorted(chats, key = lambda c: c.ts.astimezone(timezone.utc))
   if chats: return chats



def user_chats(user: str, agent: str=None):
  """
  Search for user's chat
  """
  chats = Chat.find(Chat.user==user).all()
  if agent:
    chats = [chat for chat in chats if chat.agent==agent]
  if chats: return chats

def user_long_term_memory(user: str, agent: str=None):
    """
    Extract most recent summaries from the user's previous chats (with an agent), 
    up to a limit of MAX_SUMMARY_TOKENS tokens
    """
    chats = user_chats(user, agent=agent)
    if chats:
      chats = sorted([c for c in chats if c.summary], key=lambda c: c.ts)
      tokens = 0
      summary = ""
      while tokens<MAX_SUMMARY_TOKENS and chats:
        chat = chats.pop()
        summary += '\n\n'+str(chat.ts)+': '+chat.summary
        tokens = ntokens(summary)    
      return summary


def summarize_chat(chat:Chat, max_words=100):
  """
  Summarize a chat text
  """
  assert os.environ.get('OPENAI_API_KEY')
  client = OpenAI()

  text = '\n'.join(msg.role+': '+msg.content for msg in chat.msgs)
  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
    {
      "role": "system",
      "content": f"Extract the subject of the conversation below and summarize in max {max_words} words. Please highlight the assistant conclusions in the end relating the student performance."
    },
    {
      "role": "user",
      "content": text
    }
    ],
    temperature=0.7,
    max_tokens=int(max_words*1.3),
    top_p=1)
  return response.choices[0].message


######## SOW CRUD APIs ########

def create_sow(course: str, level: str, sessions: List[Dict]=None, **other_kwargs):
   try:
      session_list = []
      if sessions: session_list = [Session(**s) for s in sessions]
      sow = StatementOfWork(course=course, level=level, sessions=session_list, **other_kwargs)
      sow.save()

   except Exception as e:
      logging.error(f"Failed to create SOW: {str(e)}")
      raise e

def add_session_to_sow(course: str, level: str, session: Dict):
   try:
      sow = read_sow_by_qualification(course, level=level)
      if sow:
         new_session = Session(**session)
      sow.sessions.append(new_session)
      sow.save()
      return sow
   except Exception as e:
      logging.error(f"Failed to create SOW: {str(e)}")
      raise e

def update_session_to_sow(course: str, level: str, session: Dict):
   try:
      sow = read_sow_by_qualification(course, level=level)
      if sow:
        try:
           prev_session = next(s for s in sow.sessions if s.session==session['session'])
        except StopIteration:
           logging.error(f"Session {session['session']} not found in SOW {sow.course} Level {sow.level}.")
           return False
        new_session = Session(**session)
        sow.sessions = [new_session if xsession.session == prev_session.session else xsession for xsession in sow.sessions]
        sow.save()
        return sow
   except Exception as e:
      logging.error(f"Failed to update SOW: {str(e)}")
      raise e


def read_sow(sow_pk: str):
   try:
      sow = StatementOfWork.find(StatementOfWork.pk==sow_pk).first()
      logging.info(f"sow_pk {sow_pk} found")
      return sow
   except Exception as e:
     logging.error(f"sow_pk {sow_pk} not found.")
     raise e


def read_sow_by_qualification(course: str, level:str=None):
   sow_list = StatementOfWork.find(StatementOfWork.course==course).all()
   if sow_list:
      if level: sow_list = [s for s in sow_list if s.level==level]
      return sow_list
         
def read_school_sow_list(school: str=None):
   sow_list = StatementOfWork.find().all()
   if school:
      sow_list = [s for s in sow_list if s.school==school]
   if sow_list: return sow_list


def update_sow(course: str, level: str, **other_kwargs):
  try:
    sow_list = read_sow_by_qualification(course, level=level)
    if sow_list:
      sow = sow_list[0]
      sow.__dict__.update(**other_kwargs)
      sow.save()
      logging.info(f"SOW {sow.pk} updated.")
      return sow
    else:
       logging.error(f"Sow for course {course} level {level} not found.")
  except Exception as e:
      logging.info(f"Error updating SOW: {str(e)}")
      raise e
     
######## User Invitations ########  
def add_invitation(email: str):
   """
   Add a user to invitation list
   """
   invite = Invitation.find(Invitation.email==email).all()
   if not invite:
      invite = Invitation(email=email, invitation_key=str(uuid.uuid4()))
      invite.save()
      return invite
   else:
      logging.error(f"An invitation for {email} already exists.")

   

def check_invitation(email: str, invite_key: str):
   """
   Check is a user has been invited
   """
   try:
      invite = Invitation.find(Invitation.email==email).first()
      if invite.accepted:
         logging.info(f"Invitation for {email} has already been accepted.")
         return {"result":False, "reason":"Invitation already accepted"}
      else:
         if invite.invitation_key==invite_key:
            return {"result":True} 
         else:
            logging.info(f"Wrong Key for invitation for {email}.")
            return {"result":False, "reason":"Invalid Invitation Key"}
      
   except Exception as e:
      logging.error(f"User {email} has not been invited to join the app: {str(e)}")
      raise e
   
def update_invitation(email: str, accepted:bool):
   try:
      invite = Invitation.find(Invitation.email==email).first()
      invite.accepted = accepted
      invite.accepted_on = datetime.now()
      invite.save()
   except Exception as e:
      logging.error(f"User {email} has not been invoted to join the app.")
      raise e
   

######## Questions ########  

def create_question(course: str, question:str, question_number: str,
                    level: str=None,
                    session: str=None,
                    session_name: str=None,
                    split: Split=None,
                    marks: int = 1,
                    answer_choices: Dict = {},
                    correct_answer: str = "",
                    **other_kwargs):

   try:
      q = Question(course=course, question=question, question_number=question_number,
                level=level,
                session=session,
                session_name=session_name,
                split=split,
                marks=marks,
                answer_choices=answer_choices,
                correct_answer=correct_answer,
                **other_kwargs
                )
      q.save()
      return q
   except Exception as e:
      logging.error(f"Failed to create question: {str(e)}")
      raise e

   

def read_questions(course: str, level: str=None, session: str=None):
   """
   Load sample questions
   """
   questions = Question.find(Question.course==course).all()
   if questions:
      if level: questions = [q for q in questions if q.level==level]
      if session: questions = [q for q in questions if q.session==session]
      return questions
   


def read_courses():
   """
   Get all Courses
   """
   courses = Course.find().all()
   return courses






