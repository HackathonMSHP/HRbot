from data.database import *

def match_score(worker_tags: list, employer_need_tags: list) -> float:
    if not worker_tags or not employer_need_tags:
        return 0.0
    set_worker = set(worker_tags)
    set_employer = set(employer_need_tags)
    
    intersection = set_worker & set_employer
    union = set_worker | set_employer
    
    return len(intersection) / len(union) if union else 0.0