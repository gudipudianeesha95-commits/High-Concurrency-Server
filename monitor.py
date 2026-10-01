import psutil
import time
import sys


pid = int(sys.argv[1])

process = psutil.Process(pid)

print(f"Monitoring process: {pid}")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        cpu = process.cpu_percent(interval=1)
        memory = process.memory_info().rss / (1024 * 1024)

        print(
            f"CPU Usage: {cpu:.2f}% | "
            f"Memory Usage: {memory:.2f} MB"
        )

except KeyboardInterrupt:
    print("\nMonitoring stopped.")