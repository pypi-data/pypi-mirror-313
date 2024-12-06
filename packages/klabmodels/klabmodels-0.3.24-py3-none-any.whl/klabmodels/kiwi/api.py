from .models import Company, Service, Product, ClientCompany
from typing import Dict
import logging
from datetime import date

def read_service(pk:str):
   try:
      service = Service.find(Service.pk==pk).first()
      #logging.info(f"Service {pk} found")
      return service
   except Exception:
     logging.error(f"Service {pk} not found.")


def read_product(pk:str):
   try:
      product = Product.find(Product.pk==pk).first()
      #logging.info(f"Service {pk} found")
      return product
   except Exception:
     logging.error(f"Product {pk} not found.")


def create_company(name: str, **kwargs):
   try:
      if 'name' in kwargs: kwargs.pop('name', None)
      c = Company(name=name, **kwargs)
      c.save()
      return c
   except Exception as e:
      logging.error(f"Failed to create company: {str(e)}")
      raise e

def read_company(pk: str):
   try:
      company = Company.find(Company.pk==pk).first()
      logging.info(f"Company {pk} found")
      return company
   except Exception:
     logging.error(f"Company {pk} not found.")

def read_company_by_name(name: str):
   try:
      company = Company.find(Company.name==name).first()
      logging.info(f"Company {name} found")
      return company
   except Exception:
     logging.error(f"Company {name} not found.")

def update_company(pk: str, **kwargs):
   try:
      c = read_company(pk)
      logging.info(f"Found company: {c.name}")
      if kwargs: 
         c.__dict__.update(kwargs)
         c.save()
         return c
   except Exception as e:
      logging.info(f"Error updating company {pk}: {str(e)}")


def read_companies():
   """
   Should return the companies a user is authorised to access
   """
   companies = Company.find().all()
   if companies:
      return companies
   else:
     logging.error(f"No Company found.")

def read_tenant_companies(tenant: str):
   """
   Should return the companies a user is authorised to access
   """

   companies = Company.find().all()
   companies = [c for c in companies if c.tenant==tenant]
   if companies:
      return companies
   else:
     logging.error(f"No Company found for tenant {tenant}.")


def delete_company(pk: str):
   pass


def create_client_company(name: str, user: str, **kwargs):
   try:
      if 'name' in kwargs: kwargs.pop('name', None)
      c = ClientCompany(name=name, created_by=user, created_on=date.today(), **kwargs)
      c.save()
      return c
   except Exception as e:
      logging.error(f"Failed to create client company: {str(e)}")
      raise e
   

def read_client_company(pk: str):
   try:
      company = ClientCompany.find(ClientCompany.pk==pk).first()
      logging.info(f"Client Company {pk} found")
      return company
   except Exception:
     logging.error(f"Client Company {pk} not found.")

def update_client_company(pk: str, **kwargs):
   try:
      c = read_client_company(pk)
      logging.info(f"Found company: {c.name}")
      if kwargs: 
         c.__dict__.update(kwargs)
         c.save()
         return c
   except Exception as e:
      logging.info(f"Error updating company {pk}: {str(e)}")



def add_service_to_company(company_pk: str, service: Dict):
   """
   Create a service and add to company services
   """
   company = read_company(company_pk)
   if company:
      try:
         service2add = Service(**service)
         service2add.save()
         # TODO: check duplicates
         company.services.append(service2add.pk)
         company.save()
         return service2add
      except Exception as e:
         logging.error(f"Failed to add service to company {company_pk}: {str(e)}")
         raise e
   else:
      logging.error(f"No company {company_pk} found.")

def remove_service_from_company(company_pk: str, service_pk: str):
   company = read_company(company_pk)
   if company:
      if service_pk in company.services:
         try:
            service = Service.find(Service.pk==service_pk).first()
            service.delete(service_pk)
            company.services.remove(service_pk)
            company.save()
            return company
         except Exception as e:
            logging.error(f"Failed removing service {service_pk} from company {company_pk}: {str(e)}")
            raise e
      else:
         logging.error(f"No service {service_pk} found in company {company_pk}")
   else:
      logging.error(f"No company {company_pk} found.")


def remove_product_from_company(company_pk: str, product_pk: str):
   company = read_company(company_pk)
   if company:
      if product_pk in company.products:
         try:
            product = Product.find(Product.pk==product_pk).first()
            product.delete(Product.pk)
            company.products.remove(product_pk)
            company.save()
            return company
         except Exception as e:
            logging.error(f"Failed removing product {product_pk} from company {company_pk}: {str(e)}")
            raise e
      else:
         logging.error(f"No product {product_pk} found in company {company_pk}")
   else:
      logging.error(f"No company {company_pk} found.")



def add_product_to_company(company_pk: str, product: Dict):
   company = read_company(company_pk)
   if company:
      try:
         product2add = Product(**product)
         product2add.save()
         # TODO: check duplicates
         company.products.append(product2add.pk)
         company.save()
         return product2add
      except Exception as e:
         logging.error(f"Failed to add product to company {company_pk}: {str(e)}")
         raise e
   else:
      logging.error(f"No company {company_pk} found.")

      
def read_product_by_name(name: str):
    try:
        product = Product.find(Product.name==name).first()
        return product
    except Exception as e:
        logging.error(f"Could not find product {name}: {str(e)}")



def read_service_by_name(name: str):
    try:
        service = Service.find(Service.name==name).first()
        return service
    except Exception as e:
        logging.error(f"Could not find service {name}: {str(e)}")

