import logging
from .models import User, Tenant, Application
from passlib.context import CryptContext
from fastapi import HTTPException
from typing import List
import uuid


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_tenant(name: str, apps:List[Application], max_users=100):
   """
   Create a tenant to implement multi-tenancy among the apps
   """
   tenant = Tenant.find(Tenant.name==name).all()
   if tenant:
      logging.error(f"A tenant with name {name} already exists.")
      raise HTTPException(status_code=404, detail=f"A tenant with name {name} already exists.") 
   else:
      api_key = uuid.uuid4()
      tenant = Tenant(name=name, api_key=str(api_key), apps=apps, max_users=max_users)
      tenant.save()
      return tenant


def read_tenant(tenant_pk: str):
   try:
      tenant = Tenant.find(Tenant.pk==tenant_pk).first()
      return tenant
   except Exception:
     logging.error(f"Tenant {tenant_pk} not found.")

def read_tenant_by_name(name: str):
   try:
      tenant = Tenant.find(Tenant.name==name).first()
      return tenant
   except Exception:
     logging.error(f"Tenant {name} not found.")
     

def read_tenant_by_apikey(api_key: str):
   try:
      tenant = Tenant.find(Tenant.api_key==api_key).first()
      return tenant
   except Exception:
     logging.error(f"Tenant {api_key} not found.")


def create_user(username, hashed_password, email, tenant, full_name=None, scopes=[]):
    # Add a new user
    user = User(username=username, email=email, hashed_password=hashed_password, tenant=tenant, full_name=full_name, disabled=False, scopes=scopes)
    user.save()
    return user


def register_user(username, password, email, tenant, full_name=None, scopes=[]):
   """
   Add a new user for an application, return None is user already exists
   """
   # Check if user exists with same username or email
   if read_user_by_name(username):
       logging.error(f"User {username} already exists.")
       raise HTTPException(status_code=404, detail=f"A user with username {username} already exists.") 
   elif read_user_by_email(email):
      logging.error(f"A user with email {email} already exists.")
      raise HTTPException(status_code=404, detail=f"A user with email {email} already exists.") 
   else:
      pwd_hash = pwd_context.hash(password)
      user = create_user(username, pwd_hash, email, tenant, full_name=full_name, scopes=scopes)   
      return user
   

def change_password(username, new_password):
   if user:=read_user_by_name(username):
      pwd_hash = pwd_context.hash(new_password)
      update_user(user.pk, hashed_password=pwd_context.hash(new_password))
      return user
   return False

def read_user(user_pk: str):
  try:
     user = User.find(User.pk==user_pk).first()
     return user
  except Exception:
     logging.info(f"User {user_pk} not found.")


def read_user_by_name(username: str):
   try:
     user = User.find(User.username==username).first()
     return user
   except Exception:
     logging.info(f"User {username} not found.")


def read_user_by_email(email: str):
   try:
     user = User.find(User.email==email).first()
     return user
   except Exception:
     logging.error(f"User {email} not found.")
   
  

def update_user(user_pk: str, **kwargs):
   # Update user email or name
   try:
      user = read_user(user_pk)
      logging.info(f"Found user: {user.username}")
      if kwargs: 
         user.__dict__.update(kwargs)
         user.save()
         return user
   except Exception as e:
      logging.info(f"Error updating user {user_pk}: {str(e)}")


def add_scopes_to_user(username: str, scopes: List[str]):
   """
   Add permissions to a user in the format list of "application.object.permission.attribute_value"
   """
   user = read_user_by_name(username)
   if user:
      try:
         #user.scopes = user.scopes.extend(scopes)
         update_user(user.pk, scopes=user.scopes+scopes)
         return user
      except Exception as e:
         logging.error(f"Error adding scopes to user: {str(e)}")
         raise e
   else:
      logging.error(f"User {user_pk} not found.")

  

def delete_user(user_pk: str):
  try:
      user = read_user(user_pk)
      if user:
         user.delete(user.pk)
         logging.info(f"User {user.username} deleted.")
      else:
         logging.error(f"User {user_pk} not found.")
  except Exception as e:
      logging.error(f"Error deleting user {user_pk}: {str(e)}")

def disable_user(user_pk: str):
  try:
      user = read_user(user_pk)
      if user: 
         user.disabled = True
         user.save()
         return user
      else:
         logging.error(f"User {user_pk} not found")
  except Exception as e:
      logging.error(f"Error disabling user {user_pk}: {str(e)}")


def enable_user(user_pk: str):
  try:
      user = read_user(user_pk)
      if user: 
         user.disabled = False
         user.save()
         return user
      else:
         logging.error(f"User {user_pk} not found")
  except Exception as e:
      logging.error(f"Error enabling user {user_pk}: {str(e)}")

