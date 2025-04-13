from data.database import *

async def find_koef(id_worker, id_employer):
    worker = await get_worker(id_worker)
    employer = await get_employer(id_employer)

    for tag in worker.tags:
        if tag in employer.tags:
            return 1

    return 0