from typing import Dict, List, Optional
from redis_om import JsonModel, EmbeddedJsonModel, Field
from pydantic import BaseModel, Extra, ValidationError
from enum import Enum
import time


### Models for Kiwi

#class Company(JsonModel, extra=Extra.allow):
#    name: str = Field(index=True)
#    vision: Optional[str]
#    mission: Optional[str]
#    description: Optional[str]
#
#    def __str__(self):
#        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk'})


### Models used by Pickey

class LLM(JsonModel):
    model: str = Field(index=True)
    provider: str = Field(index=True)
    api_key_name: str
    supports_structured_response: bool = False


class Agent(str, Enum):
    jobdesc_generator = "JobDescriptionGenerator"
    questions_generator = "QuestionGenerator"
    interviewer = "Interviewer"
    interview_evaluator = "InterviewEvaluator"
    cv_evaluator = "CVEvaluator"


class CompanyAgentLLMs(JsonModel):
    company: str = Field(index=True)
    agent: Agent = Field(index=True)
    model: str


class Question(EmbeddedJsonModel):
    qnum: str
    question: str
    category: str
    skill: str | None = None
    options: List[str] | None = None # for multiple choice questions

    def __str__(self):
        return f"{self.question}\n"+'\n'.join(f"{i+1}: {o}" for i,o in enumerate(self.options)) if self.options else f"{self.question}"
    
    def __str_with_skills__(self):
        qstr = f"Q: {self.question}\nCAT: {self.category}\nSKILL: {self.skill}"
        return qstr+'\nOPTIONS:\n'+'\n'.join(f"{i+1}: {o}" for i,o in enumerate(self.options)) if self.options else qstr



class Questionnaire(EmbeddedJsonModel):
    questions: List[Question]
    def __str__(self):
        return  f"Questions: ({len(self.questions)})\n"+'\n\n'.join(str(q) for q in self.questions)
    def __str_with_skills__(self):
        return  f"Questions: ({len(self.questions)})\n"+'\n\n'.join(q.__str_with_skills__() for q in self.questions)



# Evaluation of a CV by the Evaluator agent
class CVEvaluation(JsonModel, extra=Extra.allow):
    date: float 
    candidate: str = Field(index=True)# candidate pk
    company: Optional[str] = ""# company ref
    jobdesc: Optional[str] = ""# job description reftr
    skills_evaluation : List[Dict[str, List[Dict[str, str]]]] | Dict[str, Dict[str, str]]
    company_fit_grade: Optional[str] = None
    vacancy_fit_grade: Optional[str] = None
    cv_overall_grade: Optional[str] = None
    summary: str



# Interview contents
class Interview(JsonModel):
    date: float # unix epoch
    candidate: str = Field(index=True) # Link to candidate
    job_description: str = Field(index=True) # Link to Job description
    questions: Questionnaire # interview questions
    interview: List[Dict] = [] # Messages exchanged during the interview
    evaluation: List[Dict] | Dict = None
    elapsed: float | None = None

    def __str__(self):
         return self.questions.__str_with_skills__()+"\n\nINTERVIEW:\n"+"\n".join([f"{msg.get('role')}: {msg.get('content')}" for msg in self.interview])



class Candidate(JsonModel, extra=Extra.allow):
    name: str = Field(index=True)
    resume: str
    creation_date: int | None = None
    email: str|List[str]|None=None
    resume_classified: bool =False # processed resume with a local model
    jobs_applied: List[str] = [] # list of job pks the candidate applied for 
    interviews: List[str] = [] # reference to interviews (pk)
    questions: Questionnaire | None = None # questions generated for the candidate only (not a vacancy)

    def __str__(self):
        #if self.resume_classified:
        #    return '\n'.join({f"{k.upper()} : {v}" for k,v in self.resume_classified.items() if v})
        #else:
        return f"Name: {self.name}\n\nResume: {self.resume}"


class JobDescription(JsonModel, extra=Extra.allow):
    reference: str = Field(index=True)
    job_title: str
    company: str = Field(index=True) # Reference to the company
    job_description: Optional[str]
    active: bool = True # whether the job listing is still active
    n_questions: Optional[int] = 3  # questions to generate
    k_questions: Optional[int] = 3
    p_questions: Optional[int] = 3
    cv_questions: Optional[int] = 3
    cv_k_questions: Optional[int] = 0 
    questions: Optional[Questionnaire] = []# job-only questions
    opened: float = time.time()
    closed: Optional[float] = None

    def __str__(self):
         return f"Job title: {self.job_title}\n Job Description: {self.job_description}"



# Wrapper for langroid agents
#class Agent(BaseModel):
#    agent: lr.ChatAgent
#    task: lr.Task = None
#    msgs: int = 0
#    class Config:
#        arbitrary_types_allowed = True

### Models for Kopi

### Models for Lumina

### Other Models

# Define the ANSI escape sequences for various colors and reset
class Colors(BaseModel):
    RED: str = "\033[31m"
    BLUE: str = "\033[34m"
    GREEN: str = "\033[32m"
    ORANGE: str = "\033[33m"  # no standard ANSI color for orange; using yellow
    CYAN: str = "\033[36m"
    MAGENTA: str = "\033[35m"
    YELLOW: str = "\033[33m"
    BLACK: str = "\033[30m"
    RESET: str = "\033[0m"

