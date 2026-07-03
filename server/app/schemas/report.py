from pydantic import BaseModel


class CountItem(BaseModel):
    name: str
    count: int


class DashboardReport(BaseModel):
    total_properties: int
    pending_surveys: int
    in_progress_surveys: int
    completed_surveys: int
    total_surveys: int
    total_users: int


class ReportsResponse(BaseModel):
    dashboard: DashboardReport
    ward_wise: list[CountItem]
    street_wise: list[CountItem]
    surveyor_wise: list[CountItem]
