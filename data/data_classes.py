from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class Worker:
    type = "worker"
    name = ""
    age = ""
    sphere = ""
    gender = ""
    about = ""
    status = "pause"
    work_experience = 0
    hashtags = []

class Employer:
    type = "Employer"
    name_company = ""
    age_min = ""
    age_max = ""
    sphere = ""
    gender = ""
    status = "pause"
    work_experience_min = ""
    work_experience_max = ""
    hashtags = {}
    mandatory = {}

class WorkerState(StatesGroup):
    wait = State()
    start = State()
    name = State() #+
    age = State() #+
    sphere = State() #+
    gender = State() 
    status = State() 
    work_experience = State() #+
    about = State() 
    hashtags = State()
    find = State()

class EmployerState(StatesGroup):
    start = State()
    name_company = State()
    age = State()
    sphere = State()
    gender = State()
    status = State()
    work_experience = State()
    about = State()
    hashtags = State()
    find = State()
