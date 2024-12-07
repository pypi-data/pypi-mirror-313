# -*- coding: UTF-8 -*-
# Copyright©2022 xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

"""
from queue import Queue
from threading import Thread
from time import sleep
from random import random
# Object that signals shutdown
_sentinel = object()

# A thread that produces data
def producer(out_q):
    i = 0
    while i < 20:
        # Produce some data
        i += 1
        out_q.put(i)
        # sleep(random())

    # Put the sentinel on the queue to indicate completion
    out_q.put(_sentinel)
    print('finish')


# A thread that consumes data
def consumer(in_q, idx):
    while True:
        # Get some data
        data = in_q.get()
        sleep(random())
        print(idx, '\t:', data)
        # Check for termination
        if data is _sentinel:
            in_q.put(_sentinel)
            break
    print('finish', idx)
        # Process the data


# Create the shared queue and launch both threads
q = Queue()

t2 = Thread(target=consumer, args=(q,'A'))
t3 = Thread(target=consumer, args=(q,'B'))
t4 = Thread(target=consumer, args=(q,'C'))
t1 = Thread(target=producer, args=(q,))
t1.start()
t2.start()
t3.start()
t4.start()

# 每隔1秒监控一下
for _ in range(10):
    print('len', q.qsize())
    sleep(1)

# Wait for all produced items to be consumed
t1.join()
t2.join()
t3.join()
t4.join()

print('FInis')
