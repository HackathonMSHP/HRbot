
import asyncio 

from data.database import *
from utilities.find import match_score




employers = {}
workers = {}



async def find_best_workers_for_employer(employer_id: int, limit: int) -> list[dict]:
    employer = await get_employer(employer_id)
    if not employer:
        return []
    
    active_workers = await get_all_active_workers()
    employer_tags = employer["need_tags"]
    
    scored_workers = []
    for worker in active_workers:
        score = match_score(worker["tags"], employer_tags)
        scored_workers.append((worker, score))
    
    scored_workers.sort(key=lambda x: x[1], reverse=True)
    
    return [worker for worker, score in scored_workers[:limit]]

async def find_best_jobs_for_worker(worker_id: int, limit: int) -> list[dict]:
    worker = await get_worker(worker_id)
    if not worker:
        return []
    
    active_employers = await get_all_active_employers()
    worker_tags = worker["tags"]
    
    scored_jobs = []
    for employer in active_employers:
        score = match_score(worker_tags, employer["need_tags"])
        scored_jobs.append((employer, score))
    

    scored_jobs.sort(key=lambda x: x[1], reverse=True)    
    return [employer for employer, score in scored_jobs[:limit]]


koefs = {}