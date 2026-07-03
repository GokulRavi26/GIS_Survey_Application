from io import BytesIO
import json
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import UploadFile
from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.core.config import EXPORT_DIR, UPLOAD_DIR
from app.models.import_history import ImportHistory
from app.models.property import Property
from app.models.user import User
from app.repositories.import_history_repository import ImportHistoryRepository
from app.repositories.property_repository import PropertyRepository
from app.schemas.excel import ImportReport


class ExcelService:
    HEADER_MAP = {
        "assessment_number": {
            "assessment_number",
            "assessment no",
            "assessment number",
            "assessmentnumber",
            "assessment_no",
        },
        "ward_name": {"ward", "ward_name", "ward name"},
        "street_name": {"street", "street_name", "street name"},
        "owner_name": {"owner", "owner_name", "owner name", "tax payer name"},
        "door_number": {"door", "door_no", "door number", "door_number"},
        "mobile_number": {"mobile", "mobile number", "mobile_number", "phone"},
        "half_year_tax": {
            "half year tax",
            "half_year_tax",
            "half yearly tax",
            "tax",
        },
        "balance": {"balance", "pending", "arrears"},
        "survey_status": {"survey status", "survey_status", "status"},
    }

    @staticmethod
    def import_properties(
        db: Session,
        file: UploadFile,
        current_user: User,
        update_existing: bool = True,
    ) -> ImportReport:
        file_name = file.filename or "property-register.xlsx"
        suffix = Path(file_name).suffix.lower()
        if suffix not in {".xlsx", ".xls"}:
            raise ValueError("Only .xlsx and .xls files are supported.")

        upload_dir = UPLOAD_DIR / "imports"
        upload_dir.mkdir(parents=True, exist_ok=True)
        saved_path = upload_dir / file_name
        content = file.file.read()
        saved_path.write_bytes(content)

        dataframe = pd.read_excel(BytesIO(content))
        dataframe = ExcelService._normalize_columns(dataframe)
        if "assessment_number" not in dataframe.columns:
            raise ValueError("Excel must contain an assessment number column.")

        inserted = 0
        updated = 0
        skipped = 0
        failed = 0
        errors: list[str] = []

        for row_number, row in enumerate(dataframe.to_dict("records"), start=2):
            try:
                payload = ExcelService._row_to_property_payload(row)
                if not payload["assessment_number"]:
                    skipped += 1
                    errors.append(f"Row {row_number}: missing assessment number.")
                    continue

                existing = PropertyRepository.get_by_assessment_number(
                    db,
                    payload["assessment_number"],
                )
                if existing is None:
                    PropertyRepository.create(db, Property(**payload))
                    inserted += 1
                    continue

                if not update_existing:
                    skipped += 1
                    continue

                for field, value in payload.items():
                    setattr(existing, field, value)
                PropertyRepository.update(db, existing)
                updated += 1
            except Exception as exc:
                failed += 1
                errors.append(f"Row {row_number}: {exc}")

        report = ImportReport(
            total_rows=len(dataframe.index),
            inserted_rows=inserted,
            updated_rows=updated,
            skipped_rows=skipped,
            failed_rows=failed,
            errors=errors,
        )

        ImportHistoryRepository.create(
            db,
            ImportHistory(
                file_name=file_name,
                imported_by=current_user.id,
                total_rows=report.total_rows,
                inserted_rows=report.inserted_rows,
                updated_rows=report.updated_rows,
                skipped_rows=report.skipped_rows,
                failed_rows=report.failed_rows,
                status="COMPLETED" if failed == 0 else "COMPLETED_WITH_ERRORS",
                report=json.dumps(errors),
            ),
        )
        return report

    @staticmethod
    def export_properties(db: Session) -> Path:
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = EXPORT_DIR / "property-register-export.xlsx"
        properties, _ = PropertyRepository.search(db, offset=0, limit=1_000_000)

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Properties"
        headers = [
            "Assessment Number",
            "Ward",
            "Street",
            "Owner",
            "Door Number",
            "Mobile Number",
            "Half Year Tax",
            "Balance",
            "Survey Status",
        ]
        worksheet.append(headers)
        for property_record in properties:
            worksheet.append(
                [
                    property_record.assessment_number,
                    property_record.ward_name,
                    property_record.street_name,
                    property_record.owner_name,
                    property_record.door_number,
                    property_record.mobile_number,
                    property_record.half_year_tax,
                    property_record.balance,
                    property_record.survey_status,
                ]
            )

        workbook.save(output_path)
        return output_path

    @staticmethod
    def list_import_history(db: Session):
        return ImportHistoryRepository.list_recent(db)

    @staticmethod
    def _normalize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
        normalized_columns: dict[str, str] = {}
        for column in dataframe.columns:
            normalized = str(column).strip().lower().replace("-", " ")
            normalized = " ".join(normalized.split())
            target = None
            for field, aliases in ExcelService.HEADER_MAP.items():
                if normalized in aliases:
                    target = field
                    break
            normalized_columns[column] = target or normalized.replace(" ", "_")
        return dataframe.rename(columns=normalized_columns)

    @staticmethod
    def _row_to_property_payload(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "assessment_number": ExcelService._clean_text(
                row.get("assessment_number")
            ),
            "ward_name": ExcelService._clean_text(row.get("ward_name")),
            "street_name": ExcelService._clean_text(row.get("street_name")),
            "owner_name": ExcelService._clean_text(row.get("owner_name")),
            "door_number": ExcelService._clean_text(row.get("door_number")),
            "mobile_number": ExcelService._clean_text(row.get("mobile_number")),
            "half_year_tax": ExcelService._clean_float(row.get("half_year_tax")),
            "balance": ExcelService._clean_float(row.get("balance")),
            "survey_status": (
                ExcelService._clean_text(row.get("survey_status")) or "Pending"
            ),
        }

    @staticmethod
    def _clean_text(value: Any) -> str | None:
        if value is None or pd.isna(value):
            return None
        cleaned = str(value).strip()
        if cleaned.endswith(".0"):
            cleaned = cleaned[:-2]
        return cleaned or None

    @staticmethod
    def _clean_float(value: Any) -> float:
        if value is None or pd.isna(value) or value == "":
            return 0
        return float(value)


def export_excel():
    return b""
