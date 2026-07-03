from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.property import Property
from app.models.survey import Survey
from app.models.user import User
from app.schemas.report import CountItem, DashboardReport, ReportsResponse


class ReportService:
    @staticmethod
    def get_reports(db: Session) -> ReportsResponse:
        total_properties = db.query(Property).count()
        pending = (
            db.query(Property)
            .filter(Property.survey_status == "Pending")
            .count()
        )
        in_progress = (
            db.query(Property)
            .filter(Property.survey_status == "In Progress")
            .count()
        )
        completed = (
            db.query(Property)
            .filter(Property.survey_status == "Completed")
            .count()
        )
        total_surveys = db.query(Survey).count()
        total_users = db.query(User).count()

        return ReportsResponse(
            dashboard=DashboardReport(
                total_properties=total_properties,
                pending_surveys=pending,
                in_progress_surveys=in_progress,
                completed_surveys=completed,
                total_surveys=total_surveys,
                total_users=total_users,
            ),
            ward_wise=ReportService._property_counts(db, Property.ward_name),
            street_wise=ReportService._property_counts(db, Property.street_name),
            surveyor_wise=ReportService._surveyor_counts(db),
        )

    @staticmethod
    def _property_counts(db: Session, column) -> list[CountItem]:
        rows = (
            db.query(column, func.count(Property.id))
            .group_by(column)
            .order_by(func.count(Property.id).desc())
            .all()
        )
        return [
            CountItem(name=str(name or "Unassigned"), count=count)
            for name, count in rows
        ]

    @staticmethod
    def _surveyor_counts(db: Session) -> list[CountItem]:
        rows = (
            db.query(User.full_name, func.count(Survey.id))
            .join(Survey, Survey.created_by == User.id)
            .group_by(User.full_name)
            .order_by(func.count(Survey.id).desc())
            .all()
        )
        return [CountItem(name=name, count=count) for name, count in rows]
