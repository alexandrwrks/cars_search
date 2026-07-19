from typing import List

from sqlalchemy.exc import SQLAlchemyError

from database.config import new_session
from scripts.exchange_service.repo import ExchangeRepo
from scripts.exchange_service.schemas import CurrencySchema
from utils.logger import logger


class ExchangeService:
    async def update_currency_rate(self, data: List[CurrencySchema]):
        """
        Обновление валютных данных

        :arg data: List[CurrencySchema] : данные о валюте
        """
        try:
            async with new_session() as session:
                exchange_repo = ExchangeRepo(session)

                async with session.begin():
                    await exchange_repo.update_currency_rate(data)

            logger.info("Успешное обновление валют")

        except SQLAlchemyError:
            logger.exception("ошибка базы данных при обновление валют")

        except Exception:
            logger.exception("Неожиданная ошибка при обновлении валют")

    async def insert_currency_rate(self, data: List[CurrencySchema]):
        """
        Добавление данных о валютах

        :arg data: List[CurrencySchema] : данные о валютах

        """
        try:
            async with new_session() as session:
                exchange_repo = ExchangeRepo(session)

                async with session.begin():

                    await exchange_repo.insert_currency_rate(data)
                    logger.info("Успешное обновление валют")
        except Exception:
            logger.error("Не удачное обновление валют")


exchange_service = ExchangeService()