import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger


scheduler = AsyncIOScheduler()


async def update_rete_currency():
    print(datetime.now().strftime("%d.%m.%Y %H:%M%S"))
    print("Обновление валют")


async def parse_new_cars():
    print(datetime.now().strftime("%d.%m.%Y %H:%M%S"))
    print("Парсинг новых машин")


async def send_news():
    print(datetime.now().strftime("%d.%m.%Y %H:%M%S"))
    print("Отправка сообщения об успехе")

scheduler.add_job(
    update_rete_currency,
    trigger=IntervalTrigger(seconds=30),
    id="update_rete_currency",
)

scheduler.add_job(
    send_news,
    trigger=CronTrigger(hour=17, minute=45),
    id="send_news",
)

scheduler.add_job(
    parse_new_cars,
    trigger=IntervalTrigger(minutes=1),
    id="parse_new_cars",
)

async def main():

    scheduler.start()

    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Конец...")