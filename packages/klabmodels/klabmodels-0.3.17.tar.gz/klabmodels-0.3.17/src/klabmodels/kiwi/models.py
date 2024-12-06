from pydantic import Extra, HttpUrl, EmailStr
from typing import Tuple, List, Optional, Dict
from redis_om import JsonModel, Field
from datetime import date


### Models for Kiwi
class Product(JsonModel):
    name: str = Field(..., description="Name of the product", index=True)
    description: str = Field(..., description="Description of the product")

    product_id: str | None = None
    category: str | None = None 
    price: float | None = None 
    currency: str | None = None 
    stock_quantity: int | None = None
    sku: str | None = None  # Stock Keeping Unit identifier
    manufacturer: str | None = None  # Manufacturer of the product
    warranty: str | None = None  # Field(None, description="Warranty period for the product
    dimensions: List[str] = [] #  Dimensions of the product (length, width, height)
    weight: float | None = None # eight of the product
    color: str | None = None #  olor of the product
    release_date: date | None = None # Release date of the product
    end_of_life_date: date | None = None # End of life date of the product
    download_url: HttpUrl | None = None # URL to download the product, if applicable
    documentation_url: HttpUrl | None = None # URL to the documentation, if applicable
    features: Dict[str, str] | None = {}

    def get_summary(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k !='pk' and type(v) not in (list, dict)})

    def __str__(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk' and type(v) not in (list, dict)})

    def get_long_description(self):
        summary = self.get_summary()
        features = "\nFEATURES: \n"+"\n".join(f"{k} : {v}" for k,v in self.features) if self.features else ""
        return summary+features

class Service(JsonModel):
    
    name: str = Field(..., description="Name of the service", index=True)
    description: str = Field(..., description="Description of the service")
    service_id: str | None = None #Unique identifier for the service
    category: str | None = None # Category the service belongs to
    price: float | None = None #Price of the service
    currency: str | None = None #Currency for the price
    availability: str | None = None #Availability status of the service
    provider: str | None = None #Provider of the service
    contact_email: EmailStr | None = None # Contact email for the service provider
    contact_phone: str | None = None #Contact phone number for the service provider
    website: HttpUrl|None = None # Website URL for the service
    service_area: str | None = None  #Geographical area where the service is offered
    service_start_date: date | None = None # Start date of the service availability")
    service_end_date: date | None = None # End date of the service availability
    features: Optional[Dict[str, str]] = {}

    def get_long_description(self):
        summary = self.get_summary()
        features = "\nFEATURES: \n"+"\n".join(f"{k} : {v}" for k,v in self.features) if self.features else ""
        return summary+features
    
    def get_summary(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk' and type(v) not in (list, dict)})
        
    def __str__(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk' and type(v) not in (list, dict)})

class Company(JsonModel, extra=Extra.allow):
    name: str = Field(index=True)
    created_by_user: str | None = None
    creation_date: int | None = None
    tenant: str | None = None
    vision: str | None = None
    mission: str | None = None
    description: str | None = None
    company_culture: str | None = None
    values: Dict[str, str] = {}
    industry: str | None = None
    founded: str | None = None
    num_employees: int|None = None
    headquarters: str | None = None
    website: HttpUrl | None = None
    email: EmailStr | None = None 
    phone: str | None = None
    other_addresses: List[str] = []
    social_media: Dict|None = None
    benefits_perks: Dict[str, str] = {}

    products: List[str] = []
    services: List[str] =[]



    def get_contact_info(self) -> str:
        contact_info = f"Email: {self.email}, Phone: {self.phone}, Website: {self.website}"
        return contact_info

    def get_summary(self) -> str:
        summary = [
            f"Company Name: {self.name}\n",
            f"Industry: {self.industry}\n",
            f"Founded: {self.founded}\n",
            f"Number of Employees: {self.num_employees}\n",
            f"Headquarters: {self.headquarters}\n",
            f"Website: {self.website}\n",
            f"Description: {self.description}\n",
        ]
        summary = [i for i in summary if 'None' not in i]
        return "".join(summary)

    
    def get_description(self) -> str:
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and 
                          k not in ('pk', 'products', 'services')})

    def get_long_description(self) -> str:
        products_descriptions, services_descriptions = "", ""
        products = [Product.find(Product.pk==p).first() for p in self.products]
        services = [Service.find(Service.pk==s).first() for s in self.services]
        if products:
            products_descriptions = "\n#### START PRODUCTS ####\n"+"\n".join(p.get_summary() for p in products)+"\n#### END PRODUCTS ####\n"
        if services:
            services_descriptions = "\#### START SERVICES ####\n"+"\n".join(s.get_summary() for s in services)+"\n#### END SERVICES ####\n"
            
        return self.get_description()+products_descriptions+services_descriptions
        
    def __str__(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk'})


class ClientCompany(Company):
    created_by: str
    created_on: date
    parent: str # parent company







