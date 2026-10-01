**# High-Concurrency Server Design: Blocking vs Asynchronous I/O**

The explanation below is based on the actual code and benchmark results you obtained.

**## 1. First understand the project in one sentence**

**This project compares a traditional blocking server with an asynchronous server to see how they handle many clients at the same time.**

The main idea is:

**Blocking server → handles waiting one by one**

**Asynchronous server → overlaps waiting and handles multiple clients efficiently**

**# 2. What problem are we solving?**

Imagine a server receives requests from **50 users at the same time**.

Each request requires some I/O operation that takes around **100 ms**.

### Blocking approach

The server essentially does:

```text
Client 1 → wait 100 ms → response
Client 2 → wait 100 ms → response
Client 3 → wait 100 ms → response
...
```

So the waiting happens one after another.

### Asynchronous approach

The server can do:

```text
Client 1 → waiting ─────┐
Client 2 → waiting ────┤
Client 3 → waiting ────┤
Client 4 → waiting ────┤
                        ↓
                    responses
```

The server does not sit idle while one client is waiting.

That's the main concept demonstrated by this project.

---

**# 3. Why did we use 100 ms?**

We intentionally added:

### Blocking server

```python
time.sleep(0.1)
```

### Async server

```python
await asyncio.sleep(0.1)
```

`0.1 seconds = 100 milliseconds`.

This represents an **I/O waiting period** such as:

* Database access
* File access
* Network communication
* API request
* External service response

We used the **same 100 ms delay in both servers** so that the comparison is controlled and fair.

---

**# 4. Project Architecture**

Our project contains these files:

```text
High-Concurrency-Server/
│
├── blocking_server.py
├── async_server.py
├── client.py
├── load_test.py
├── monitor.py
├── graphs.py
│
├── average_response_time.png
├── throughput.png
└── total_test_time.png
```

Each file has a specific purpose.

---

**# 5. `blocking_server.py`**

This is our traditional server.

It uses Python's:

```python
socket
```

library.

The server listens on:

```text
127.0.0.1:5000
```

### Important part

```python
conn, addr = server.accept()
```

The server waits for a client.

Then:

```python
data = conn.recv(1024)
```

It receives data.

Then we simulate I/O waiting:

```python
time.sleep(0.1)
```

Then:

```python
conn.sendall(response.encode())
```

It sends the response.

Finally:

```python
conn.close()
```

The connection is closed.

### Simple flow

```text
Client
   ↓
accept()
   ↓
receive data
   ↓
wait 100 ms
   ↓
send response
   ↓
close connection
```

The important point is that the server processes the clients sequentially.

---

**# 6. `async_server.py`**

This is our asynchronous server.

It uses:

```python
asyncio
```

and listens on:

```text
127.0.0.1:5001
```

The important function is:

```python
async def handle_client(reader, writer):
```

Each client gets its own asynchronous task.

The server receives data:

```python
data = await reader.read(1024)
```

Then:

```python
await asyncio.sleep(0.1)
```

This is very important.

Instead of blocking the entire server for 100 ms, the event loop can work on other client tasks during this waiting period.

Then the response is sent:

```python
writer.write(response.encode())
await writer.drain()
```

Finally:

```python
writer.close()
await writer.wait_closed()
```

---

**# 7. What is the difference between `sleep()` and `await sleep()`?**

This is one of the most important viva questions.

### Blocking

```python
time.sleep(0.1)
```

The current execution is blocked for 100 ms.

### Async

```python
await asyncio.sleep(0.1)
```

The current task waits, but the **event loop can handle other tasks** during that time.

So:

> `time.sleep()` blocks the execution, while `await asyncio.sleep()` allows other asynchronous tasks to run during the wait.

---

**# 8. `client.py`**

This is a simple client used to test the server.

It:

1. Creates a socket.
2. Connects to the server.
3. Sends:

```text
Hello Server!
```

4. Receives the response.
5. Prints the response.
6. Closes the connection.

For the blocking server, it uses:

```text
Port 5000
```

For the async server, you would use:

```text
Port 5001
```

---

**# 9. `load_test.py`**

This is one of the most important files.

It allows us to test multiple clients.

We used:

```python
ThreadPoolExecutor
```

to generate concurrent client requests.

We tested:

```text
10 clients
25 clients
50 clients
```

For every client, we measure:

### Response time

How long that particular request took.

### Total test time

How long the complete group of requests took.

### Throughput

How many requests the server processed per second.

Formula:

```text
Throughput = Successful Requests / Total Test Time
```

---

**# 10. Why do we use concurrent clients?**

If we tested only one client, we wouldn't really be testing **high concurrency**.

Our goal is to see what happens when many clients arrive at nearly the same time.

Therefore:

```text
10 clients
25 clients
50 clients
```

give us increasing workload levels.

---

**# 11. `monitor.py`**

This program monitors the server's resource usage.

We use:

```python
psutil
```

It measures:

### CPU usage

```python
process.cpu_percent(interval=1)
```

### Memory usage

```python
process.memory_info().rss
```

Memory is converted into MB.

The output looks like:

```text
CPU Usage: 0.00% | Memory Usage: 10.35 MB
```

This allows us to compare resource consumption.

---

**# 12. `graphs.py`**

This program creates three graphs.

### Graph 1

```text
Average Response Time
```

### Graph 2

```text
Throughput
```

### Graph 3

```text
Total Test Time
```

The graphs make the performance difference easier to understand visually.

---

**# 13. Experimental Methodology**

We performed a controlled experiment.

### Same machine

Both servers were tested on the same system.

### Same client workload

Both servers received:

```text
10 clients
25 clients
50 clients
```

### Same simulated I/O wait

Both used:

```text
100 ms
```

### Same request

Each client sent:

```text
Hello Server!
```

### Measurements

We measured:

* Total test time
* Average response time
* Throughput
* Successful requests
* CPU usage
* Memory usage

This makes the comparison more meaningful.

---

**# 14. Results**

These are your actual controlled benchmark results.

| Clients | Server   | Total Time | Avg Response |   Throughput | Success |
| ------: | -------- | ---------: | -----------: | -----------: | ------: |
|      10 | Blocking |   1.2451 s |    678.55 ms |   8.03 req/s |   10/10 |
|      10 | Async    |   0.1456 s |    111.78 ms |  68.67 req/s |   10/10 |
|      25 | Blocking |   2.8619 s |   1538.26 ms |   8.74 req/s |   25/25 |
|      25 | Async    |   0.1935 s |    108.86 ms | 129.20 req/s |   25/25 |
|      50 | Blocking |   5.3375 s |   2749.48 ms |   9.37 req/s |   50/50 |
|      50 | Async    |   0.1753 s |    131.57 ms | 285.29 req/s |   50/50 |

---

**# 15. Understanding the 10-client result**

### Blocking

```text
Total time = 1.2451 s
Average response = 678.55 ms
Throughput = 8.03 req/s
```

### Async

```text
Total time = 0.1456 s
Average response = 111.78 ms
Throughput = 68.67 req/s
```

The asynchronous server completes the group of requests much faster because the 100 ms waits overlap.

---

**# 16. Understanding the 25-client result**

### Blocking

```text
2.8619 seconds
1538.26 ms average response
8.74 requests/sec
```

### Async

```text
0.1935 seconds
108.86 ms average response
129.20 requests/sec
```

As the number of clients increases, the difference becomes much more visible.

---

**# 17. Understanding the 50-client result**

This is our most important test.

### Blocking

```text
Total time       = 5.3375 seconds
Average response = 2749.48 ms
Throughput       = 9.37 requests/sec
Success          = 50/50
```

### Async

```text
Total time       = 0.1753 seconds
Average response = 131.57 ms
Throughput       = 285.29 requests/sec
Success          = 50/50
```

The asynchronous server processed the 50-client workload while allowing the I/O waits to overlap.

---

**# 18. Throughput comparison**

At 50 clients:

```text
Blocking = 9.37 requests/sec

Async = 285.29 requests/sec
```

The measured async throughput is about **30.4 times** the blocking throughput in this particular controlled test.

This is a descriptive result from our experiment, not a universal factor for every workload or machine.

---

**# 19. Response-time comparison**

At 50 clients:

```text
Blocking = 2749.48 ms

Async = 131.57 ms
```

The blocking server's average response time increases substantially as more clients are added.

The async server remains much closer to the 100 ms simulated I/O wait.

---

**# 20. Why does blocking become slower?**

Suppose there are 50 clients.

The blocking server essentially has to wait for one request before proceeding to the next.

Conceptually:

```text
Client 1 → 100 ms
Client 2 → 100 ms
Client 3 → 100 ms
Client 4 → 100 ms
...
Client 50 → 100 ms
```

The waits accumulate.

Therefore, clients later in the queue experience larger response times.

---

**# 21. Why is async faster?**

The async server can start multiple tasks.

Conceptually:

```text
Client 1 ── waiting ──┐
Client 2 ── waiting ──┤
Client 3 ── waiting ──┤
Client 4 ── waiting ──┤
Client 5 ── waiting ──┤
                      ↓
                 responses
```

While one task is waiting for I/O, the event loop can work on another task.

This is called **overlapping I/O waits**.

---

**# 22. CPU and memory results**

We also monitored the processes.

### Blocking server

For the 50-client test:

```text
CPU: mostly 0.00% in the 1-second samples
Memory: approximately 10.35–10.40 MB
```

### Async server

For the 50-client test:

```text
CPU: mostly 0.00%
One sampled value: 6.20%
Memory: approximately 8.43–12.56 MB
```

Important:

The CPU values are **sampled observations**, not proof that the servers used zero CPU.

The monitor samples CPU at intervals, so short bursts of CPU activity may not be captured.

---

**# 23. What does "high concurrency" mean?**

**Concurrency** means dealing with multiple tasks that are in progress during overlapping periods.

It does not necessarily mean executing everything simultaneously on different CPU cores.

In our project:

```text
Many clients
     ↓
Many requests waiting/processing
     ↓
Server manages them
```

The async server is particularly suitable for I/O-bound concurrency.

---

**# 24. What is I/O-bound work?**

I/O-bound work is work where the program spends significant time waiting for something external.

Examples:

```text
Database
Network
File system
API
Web service
Disk
```

For example:

```text
Application → request database
             ↓
           WAIT
             ↓
       database responds
```

During this waiting time, an asynchronous program can work on other tasks.

---

**# 25. Why is asynchronous I/O useful for servers?**

Servers frequently handle:

* Web requests
* API calls
* Database operations
* Network communication
* File operations
* Chat applications

Many of these operations involve waiting.

Asynchronous programming can use those waiting periods more efficiently.

---

**# 26. What technology did we use?**

### Programming language

**Python**

### Networking

**TCP sockets**

### Blocking implementation

```text
socket
```

### Asynchronous implementation

```text
asyncio
```

### Concurrent load generation

```text
ThreadPoolExecutor
```

### Resource monitoring

```text
psutil
```

### Graphs

```text
Matplotlib
```

---

**# 27. Project workflow**

You can explain the complete workflow like this:

```text
                START
                  ↓
        Create Blocking Server
                  ↓
        Create Async Server
                  ↓
          Create Client
                  ↓
       Generate Concurrent Load
                  ↓
       Test 10 / 25 / 50 Clients
                  ↓
    Measure Response Time & Throughput
                  ↓
        Monitor CPU & Memory
                  ↓
             Generate Graphs
                  ↓
          Compare the Results
                  ↓
               CONCLUSION
```

---

**# 28. Simple example for your sir**

If your sir asks:

**"Explain your project in simple words."**

You can say:

> "Sir, our project is a comparison between blocking and asynchronous I/O servers. We created two TCP servers using Python. The blocking server handles client requests sequentially, while the asynchronous server uses Python asyncio to handle multiple client tasks without blocking during I/O waits. We simulated the same 100 millisecond I/O delay in both servers and tested them with 10, 25, and 50 concurrent clients. We measured total execution time, average response time, throughput, CPU usage, and memory usage. In our 50-client test, the blocking server took 5.3375 seconds with an average response time of 2749.48 ms, while the asynchronous server took only 0.1753 seconds with an average response time of 131.57 ms. Both successfully handled all 50 requests. The experiment demonstrates the advantage of asynchronous I/O for I/O-bound workloads."

That's a very good **1-minute explanation**.

---

**# 29. Important viva questions**

### Q1. What is blocking I/O?

**Answer:**

> Blocking I/O makes the program wait until the current I/O operation finishes before continuing.

---

### Q2. What is asynchronous I/O?

**Answer:**

> Asynchronous I/O allows a program to start an I/O operation and perform other tasks while waiting for that operation to complete.

---

### Q3. Why did you use asyncio?

**Answer:**

> We used Python's asyncio library to implement asynchronous client handling using an event loop.

---

### Q4. Why did you use 100 ms delay?

**Answer:**

> We used the same 100 ms simulated I/O wait in both servers to create a controlled and fair comparison.

---

### Q5. Why did you test 10, 25 and 50 clients?

**Answer:**

> To observe how both servers behave as the level of concurrent workload increases.

---

### Q6. What is throughput?

**Answer:**

> Throughput is the number of successfully completed requests per second.

Formula:

```text
Throughput = Successful Requests / Total Test Time
```

---

### Q7. What is response time?

**Answer:**

> Response time is the time taken from sending a request until receiving the server's response.

---

### Q8. Why does blocking response time increase?

**Answer:**

> Because requests are handled sequentially, so clients have to wait for earlier requests to finish.

---

### Q9. Why does async perform better for this workload?

**Answer:**

> Because the simulated work is I/O-bound. While one asynchronous task is waiting, the event loop can handle other tasks.

---

### Q10. Is async always faster?

**Answer:**

> No. Its advantages are especially relevant for I/O-bound workloads with many concurrent operations. CPU-bound workloads can require different approaches.

This is an important answer because you should **not claim that async is always faster**.

---

### Q11. What happens if the workload is CPU-bound?

**Answer:**

> Asynchronous I/O does not automatically make CPU-heavy calculations faster. CPU-bound workloads may require multiprocessing, optimized native code, GPUs, or other approaches.

---

### Q12. What is the role of `await`?

**Answer:**

> `await` suspends the current asynchronous task while it waits for an operation, allowing the event loop to run other tasks.

---

### Q13. What is an event loop?

**Answer:**

> An event loop manages asynchronous tasks and decides which task can run when another task is waiting for I/O.

---

### Q14. Why are there two ports?

```text
Blocking → 5000
Async → 5001
```

**Answer:**

> We used separate ports so that both servers could be run independently without a port conflict.

---

### Q15. Did all requests succeed?

**Answer:**

> Yes. In the controlled benchmark, all 170 requests across the 10, 25, and 50-client tests succeeded.

---

**# 30. Advanced extension — io_uring**

Your professor mentioned:

> "An advanced extension can explore io_uring."

You **do not need to implement this unless your professor specifically requires it**.

`io_uring` is a Linux kernel interface designed for efficient asynchronous I/O.

Your current project already satisfies the core comparison:

```text
Blocking I/O
       vs
Asynchronous I/O
```

So you can mention:

> "io_uring was considered as an advanced extension, but the current implementation focuses on comparing Python blocking sockets with asyncio-based asynchronous I/O."

---

**# 31. Project limitations**

It is good to mention limitations honestly.

### Limitation 1

The test was performed on a local machine:

```text
127.0.0.1
```

So it does not represent Internet-scale networking.

### Limitation 2

The 100 ms delay is simulated.

It represents an I/O wait rather than an actual database or remote API.

### Limitation 3

CPU monitoring uses periodic sampling, so short CPU bursts may not be captured.

### Limitation 4

The exact performance numbers depend on the computer, Python version, operating system, and workload.

---

**# 32. Future improvements**

You can add these to your README:

* Test with 100, 500, and 1000 clients.
* Use real database I/O.
* Test actual HTTP requests.
* Add latency percentiles such as P50, P95 and P99.
* Measure CPU and memory more continuously.
* Run the servers on separate machines.
* Compare threads, processes and asyncio.
* Implement the optional Linux `io_uring` version.
* Add a web-based dashboard for monitoring.

---

**# 33. Final conclusion**

Your conclusion can be:

> Under the controlled workload with a simulated 100 ms I/O wait, the asynchronous server completed 50 concurrent client requests in 0.1753 seconds with an average response time of 131.57 ms and throughput of 285.29 requests/sec. The blocking server required 5.3375 seconds, with an average response time of 2749.48 ms and throughput of 9.37 requests/sec. Both servers successfully handled all 50 requests. The results demonstrate how asynchronous I/O can overlap waiting periods and improve concurrency for I/O-bound workloads.

---

**# 34. Complete README**

For GitHub, I recommend putting the above information into a structured README with sections like:

