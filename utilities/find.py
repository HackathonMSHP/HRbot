from data.database import *

async def find_koef(id_worker, id_employer):
    worker = await get_worker(id_worker)
    employer = await get_employer(id_employer)

    koef = 0

    for tag in worker.tags:
        if tag in employer.tags:
            koef += 1

    if (employer.age_min <= worker.age <= employer.age_max):
        koef += 3

    if (not employer.work_experience_min <= worker.work_experience <= employer.work_experience_max):
        koef -= 5

    return koef