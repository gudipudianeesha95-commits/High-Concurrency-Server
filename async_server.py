import asyncio

HOST = "127.0.0.1"
PORT = 5001


async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")

    print(f"Client connected: {address}")

    data = await reader.read(1024)

    print(f"Received: {data.decode()}")

    # Simulate 100 ms of I/O waiting
    await asyncio.sleep(0.1)

    response = "Hello from Async Server!"

    writer.write(response.encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_client,
        HOST,
        PORT
    )

    print(f"Async server started on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()


asyncio.run(main())