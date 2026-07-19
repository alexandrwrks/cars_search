import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from exchange_service.get_currency import get_need_currency


"""
scheduler.start()

scheduler.shutdown()

"""

async def main():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        get_need_currency,
        'interval',
        seconds=10,
    )

    scheduler.start()
    print("Планировщик запущен в фоновом режиме.")

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Планировщик остановлен.")
