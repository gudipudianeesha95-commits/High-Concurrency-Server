import socket
import time
import sys
from concurrent.futures import ThreadPoolExecutor


HOST = "127.0.0.1"


def send_request(port, client_number):
    start_time = time.perf_counter()

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, port))

        client.sendall(b"Hello Server!")

        response = client.recv(1024)

        end_time = time.perf_counter()

        client.close()

        response_time = (end_time - start_time) * 1000

        return client_number, response_time, True

    except Exception as error:
        return client_number, 0, False


def test_server(port, number_of_clients):

    print(f"\nTesting port {port} with {number_of_clients} clients...\n")

    start_time = time.perf_counter()

    results = []

    with ThreadPoolExecutor(max_workers=number_of_clients) as executor:

        futures = [
            executor.submit(send_request, port, i + 1)
            for i in range(number_of_clients)
        ]

        for future in futures:
            results.append(future.result())

    end_time = time.perf_counter()

    total_time = end_time - start_time

    successful = 0
    failed = 0
    response_times = []

    for client_number, response_time, success in results:

        if success:
            successful += 1
            response_times.append(response_time)

            print(
                f"Client {client_number}: "
                f"{response_time:.2f} ms"
            )

        else:
            failed += 1

            print(
                f"Client {client_number}: FAILED"
            )

    if response_times:

        average_response = (
            sum(response_times) / len(response_times)
        )

        throughput = successful / total_time

        print("\n----- RESULTS -----")

        print(f"Total clients       : {number_of_clients}")
        print(f"Successful requests : {successful}")
        print(f"Failed requests     : {failed}")
        print(f"Total test time     : {total_time:.4f} seconds")
        print(
            f"Average response    : "
            f"{average_response:.2f} ms"
        )
        print(
            f"Throughput          : "
            f"{throughput:.2f} requests/sec"
        )

    else:
        print("\nNo successful requests.")


if __name__ == "__main__":

    port = int(sys.argv[1])
    clients = int(sys.argv[2])

    test_server(port, clients)