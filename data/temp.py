import asyncio
from data.database import *
from utilities.find import match_score
import heapq

employers = {}
workers = {}
koefs = {}
data_initialized = False
data_lock = asyncio.Lock()
employers_lock = asyncio.Lock()
workers_lock = asyncio.Lock()

async def initialize_data():
    global employers, workers, data_initialized
    async with data_lock:
        if data_initialized:
            return
        try:
            active_workers = await get_all_active_workers()
            async with workers_lock:
                for worker in active_workers:
                    workers[worker["id"]] = worker
            
            active_employers = await get_all_active_employers()
            async with employers_lock:
                for employer in active_employers:
                    employers[employer["id"]] = employer
            
            data_initialized = True
        except Exception as e:
            print(f"Error initializing data: {e}")

async def find_best_workers_for_employer(employer_id: int, limit: int) -> list[dict]:
    if not data_initialized:
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
    async with workers_lock:
        for worker_id, worker in workers.items():
            if worker["status"] != "active" or worker_id in skipped_ids:
                continue
            score = match_score(worker["tags"], employer_tags)
            scored_workers.append((worker, score))
    
    return [worker for worker, score in heapq.nlargest(limit, scored_workers, key=lambda x: x[1])]

async def find_best_jobs_for_worker(worker_id: int, limit: int) -> list[dict]:
    if not data_initialized:
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
    async with employers_lock:
        for employer_id, employer in employers.items():
            if employer["status"] != "active" or employer_id in skipped_ids:
                continue
            score = match_score(worker_tags, employer["need_tags"])
            scored_jobs.append((employer, score))
    
    return [employer for employer, score in heapq.nlargest(limit, scored_jobs, key=lambda x: x[1])]


async def skip_worker(employer_id: int, worker_id: int):
    success = await add_to_employer_skipped(employer_id, worker_id)
    if success:
        async with employers_lock:
            if employer_id in employers:
                if "skipped" not in employers[employer_id]:
                    employers[employer_id]["skipped"] = []
                employers[employer_id]["skipped"].append(worker_id)
    return success
