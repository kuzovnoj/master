import asyncio


async def main():
    future = asyncio.Future()
    print(future.done())  # False, Future находится в состоянии pending

    # Устанавливаем результат
    future.set_result(42)
    print(future.done())  # True


asyncio.run(main())