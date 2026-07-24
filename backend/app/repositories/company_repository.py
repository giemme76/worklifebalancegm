from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanySettingsUpdate, CompanySetup


class CompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CompanySetup, website: str | None = None) -> Company:
        company = Company(
            name=data.name,
            website=website or data.website,
            headquarters=data.headquarters,
            policy_type=data.policy_type,
            smart_working_percentage=data.smart_working_percentage,
            office_days_per_week=data.office_days_per_week,
            work_days_per_week=data.work_days_per_week,
            monitoring_start_date=data.monitoring_start_date,
        )
        self.db.add(company)
        self.db.flush()
        return company

    def get(self, company_id: int) -> Company | None:
        return self.db.get(Company, company_id)

    def update(self, company: Company, data: CompanySettingsUpdate) -> Company:
        company.policy_type = data.policy_type
        company.smart_working_percentage = data.smart_working_percentage
        company.office_days_per_week = data.office_days_per_week
        company.work_days_per_week = data.work_days_per_week
        company.monitoring_start_date = data.monitoring_start_date
        self.db.flush()
        return company

    def delete(self, company: Company) -> None:
        self.db.delete(company)
        self.db.flush()
