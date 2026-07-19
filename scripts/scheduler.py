from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from scripts.add_cars.add_cars import get_new_cars
from scripts.exchange_service.exchange_service import exchange_service
from scripts.exchange_service.get_currency import update_currency_rate

scheduler = AsyncIOScheduler()


async def update_rate_currency():
    print(datetime.now().strftime("%d.%m.%Y %H:%M%S"))
    print("Обновление валют")

    data = await update_currency_rate()
    if data is None:
        return
    await exchange_service.update_currency_rate(data)


async def get_cars():
    print(datetime.now().strftime("%d.%m.%Y %H:%M%S"))
    print("Парсинг новых машин")

    await get_new_cars()


scheduler.add_job(
    update_rate_currency,
    trigger=IntervalTrigger(minutes=30),
    id="update_rate_currency",
)

scheduler.add_job(
    get_new_cars,
    trigger=IntervalTrigger(minutes=10),
    id="get_new_cars",
)
