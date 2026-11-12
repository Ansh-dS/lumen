from arq import Worker

from backend.lib.config import get_redis_settings

def startLangchaninFlow()-> None:
    a= 10 

startExectingTask = Worker(
    functions=[startLangchaninFlow],
    redis_settings=get_redis_settings(),
    max_jobs=1000,
    keep_result_forever=True,
    job_timeout=30,
    max_tries=3,
)
    
startExectingTask.run()