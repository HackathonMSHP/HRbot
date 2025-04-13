import asyncio 
from data.database import *
from utilities.find import match_score

employers = {}
workers = {}
koefs = {}

async def initialize_data():
    global employers, workers
    
    active_workers = await get_all_active_workers()
    for worker in active_workers:
        workers[worker["id"]] = worker
    
    active_employers = await get_all_active_employers()
    for employer in active_employers:
        employers[employer["id"]] = employer

async def find_best_workers_for_employer(employer_id: int, limit: int) -> list[list]:
    if not employers or not workers:
        await initialize_data()
    
    employer = employers.get(employer_id)
    if not employer:
        employer = await get_employer(employer_id)
        if not employer:
            return []
        employers[employer_id] = employer
    
    employer_tags = employer["need_tags"]
    skipped_ids = set(employer.get("skipped", []))
    
    scored_workers = []
    for worker_id, worker in workers.items():
        if worker["status"] != "active":
            continue
        if worker_id in skipped_ids:
            continue
        score = match_score(worker["tags"], employer_tags)
        scored_workers.append((worker, score))
    
    scored_workers.sort(key=lambda x: x[1], reverse=True)
    
    return [worker for worker, score in scored_workers[:limit]]

async def find_best_jobs_for_worker(worker_id: int, limit: int) -> list[list]:
    if not employers or not workers:
        await initialize_data()
    
    worker = workers.get(worker_id)
    if not worker:
        worker = await get_worker(worker_id)
        if not worker:
            return []
        workers[worker_id] = worker
    
    worker_tags = worker["tags"]
    skipped_ids = set(worker.get("skipped", []))
    
    scored_jobs = []
    for employer_id, employer in employers.items():
        if employer["status"] != "active":
            continue
        if employer_id in skipped_ids:
            continue
        score = match_score(worker_tags, employer["need_tags"])
        scored_jobs.append((employer, score))
    
    scored_jobs.sort(key=lambda x: x[1], reverse=True)    
    return [employer for employer, score in scored_jobs[:limit]]

async def skip_worker(employer_id: int, worker_id: int):
    success = await add_to_employer_skipped(employer_id, worker_id)
    if success and employer_id in employers:
        if "skipped" not in employers[employer_id]:
            employers[employer_id]["skipped"] = []
        employers[employer_id]["skipped"].append(worker_id)
    return success

async def skip_employer(worker_id: int, employer_id: int):
    success = await add_to_worker_skipped(worker_id, employer_id)
    if success and worker_id in workers:
        if "skipped" not in workers[worker_id]:
            workers[worker_id]["skipped"] = []
        workers[worker_id]["skipped"].append(employer_id)
    return success