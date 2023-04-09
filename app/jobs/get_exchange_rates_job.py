from ..database import SessionLocal
from ..services.exchange_rate_service import ExchangeRateService

from datetime import date

def get_actual_exchange_rates():
    db = SessionLocal()
    service = ExchangeRateService(db=db)
    m_date = date.today()

    if not service.check_is_db_has_actual_data_form_date(m_date=m_date):
        service.synchronise_exrange_rate_data(m_date=m_date)

    return True
