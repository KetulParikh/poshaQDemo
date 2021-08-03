import os
import sys
import json
import time
from threading import Thread
import requests


NUM_REQUESTS = 1000
SLEEP_COUNT = 0.01
ENDPOINT = "http://localhost"

# Simple get request stress test - Benchmark (4.1141) seconds
def call_predict_endpoint(n):
    # submit the request
    r = requests.get(ENDPOINT)
    # ensure the request was sucessful
    # print(r.text)

# start timer
start = time.process_time()

# loop over the number of threads
for i in range(0, NUM_REQUESTS):
    # start a new thread to call the API
    t = Thread(target=call_predict_endpoint, args=(None,))
    t.daemon = True
    t.start()
    time.sleep(SLEEP_COUNT)

# stop timer
stop = time.process_time()

print("pipeline took (%.4f) seconds of process time to complete" %
      (stop - start))
