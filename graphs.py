import matplotlib.pyplot as plt

# Number of concurrent clients
clients = [10, 25, 50]

# ============================================================
# 1. AVERAGE RESPONSE TIME
# ============================================================

blocking_response = [678.55, 1538.26, 2749.48]
async_response = [111.78, 108.86, 131.57]

plt.figure(figsize=(8, 5))

plt.plot(
    clients,
    blocking_response,
    marker="o",
    label="Blocking"
)

plt.plot(
    clients,
    async_response,
    marker="o",
    label="Asynchronous"
)

plt.xlabel("Number of Clients")
plt.ylabel("Average Response Time (ms)")
plt.title("Blocking vs Asynchronous - Average Response Time")
plt.legend()
plt.grid(True)

plt.tight_layout()

# Save graph
plt.savefig("average_response_time.png", dpi=300)

# Display graph
plt.show()


# ============================================================
# 2. THROUGHPUT
# ============================================================

blocking_throughput = [8.03, 8.74, 9.37]
async_throughput = [68.67, 129.20, 285.29]

plt.figure(figsize=(8, 5))

plt.plot(
    clients,
    blocking_throughput,
    marker="o",
    label="Blocking"
)

plt.plot(
    clients,
    async_throughput,
    marker="o",
    label="Asynchronous"
)

plt.xlabel("Number of Clients")
plt.ylabel("Throughput (Requests/Second)")
plt.title("Blocking vs Asynchronous - Throughput")
plt.legend()
plt.grid(True)

plt.tight_layout()

# Save graph
plt.savefig("throughput.png", dpi=300)

# Display graph
plt.show()


# ============================================================
# 3. TOTAL TEST TIME
# ============================================================

blocking_time = [1.2451, 2.8619, 5.3375]
async_time = [0.1456, 0.1935, 0.1753]

plt.figure(figsize=(8, 5))

plt.plot(
    clients,
    blocking_time,
    marker="o",
    label="Blocking"
)

plt.plot(
    clients,
    async_time,
    marker="o",
    label="Asynchronous"
)

plt.xlabel("Number of Clients")
plt.ylabel("Total Test Time (seconds)")
plt.title("Blocking vs Asynchronous - Total Test Time")
plt.legend()
plt.grid(True)

plt.tight_layout()

# Save graph
plt.savefig("total_test_time.png", dpi=300)

# Display graph
plt.show()


print("\n========================================")
print("All 3 graphs generated successfully!")
print("========================================")
print("1. average_response_time.png")
print("2. throughput.png")
print("3. total_test_time.png")