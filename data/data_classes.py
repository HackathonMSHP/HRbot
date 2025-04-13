from aiogram.fsm.state import State, StatesGroup

class Worker:
    name = ""
    age = ""
    sphere = ""
    gender = ""
    about = ""
    status = "pause"
    work_experience = 0
    tags = []
    likes = []
    was_likes = []

class Employer:
    name_company = ""
    age_min = ""
    age_max = ""
    sphere = ""
    gender = ""
    status = "pause"
    work_experience_min = ""
    work_experience_max = ""
    need_tags = []
    likes = []
    was_likes = []

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
    wait = State()
    sphere = State()
    status = State()
    work_experience = State()
    about = State()
    hashtags = State()
    find = State()
