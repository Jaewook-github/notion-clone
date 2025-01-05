
from enum import Enum


class ActionType(str, Enum):
    # 기본 액션
    UPDATE_RECORD = "update_record"
    CREATE_RECORD = "create_record"
    DELETE_RECORD = "delete_record"
    SEND_NOTIFICATION = "send_notification"

    # 파일 관련 액션
    CREATE_BACKUP = "create_backup"
    EXPORT_TO_PDF = "export_to_pdf"
    EXPORT_TO_EXCEL = "export_to_excel"
    IMPORT_FROM_CSV = "import_from_csv"

    # 외부 연동 액션
    SYNC_CALENDAR = "sync_calendar"
    CREATE_GITHUB_ISSUE = "create_github_issue"
    POST_TO_SLACK = "post_to_slack"
    SEND_TO_DISCORD = "send_to_discord"
    CREATE_TRELLO_CARD = "create_trello_card"

    # 데이터 처리 액션
    CALCULATE_METRICS = "calculate_metrics"
    GENERATE_REPORT = "generate_report"
    UPDATE_DASHBOARD = "update_dashboard"
    RUN_DATA_ANALYSIS = "run_data_analysis"

    # 시스템 액션
    SCHEDULE_BACKUP = "schedule_backup"
    CLEAN_OLD_RECORDS = "clean_old_records"
    ARCHIVE_RECORDS = "archive_records"
    SET_PERMISSIONS = "set_permissions"

    # 고급 통신 액션
    SEND_SMS = "send_sms"
    MAKE_PHONE_CALL = "make_phone_call"
    SEND_TELEGRAM = "send_telegram"
    POST_TO_SOCIAL = "post_to_social"


# 액션 구현 예시
class AdvancedActions:
    async def export_to_pdf(self, data: Dict) -> Dict:
        """페이지나 데이터베이스를 PDF로 내보내기"""
        template = data.get("template", "default")
        content = data.get("content", {})

        pdf_options = {
            "format": "A4",
            "margin": {"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"},
            "headerTemplate": "<div>Header</div>",
            "footerTemplate": "<div>Footer</div>"
        }

        return {
            "file_path": "exports/document.pdf",
            "size": "1.2MB",
            "pages": 5
        }

    async def sync_calendar(self, data: Dict) -> Dict:
        """캘린더 동기화 (Google Calendar 등)"""
        calendar_id = data.get("calendar_id")
        events = data.get("events", [])

        return {
            "synced_events": len(events),
            "calendar": calendar_id
        }

    async def create_github_issue(self, data: Dict) -> Dict:
        """GitHub 이슈 생성"""
        repo = data.get("repository")
        title = data.get("title")
        body = data.get("body")
        labels = data.get("labels", [])

        return {
            "issue_number": 42,
            "url": f"https://github.com/{repo}/issues/42"
        }

    async def generate_report(self, data: Dict) -> Dict:
        """데이터 분석 리포트 생성"""
        report_type = data.get("type", "summary")
        metrics = data.get("metrics", [])

        return {
            "report_id": "rep_123",
            "url": "reports/analysis_2024_01.html",
            "metrics_calculated": len(metrics)
        }

    async def archive_records(self, data: Dict) -> Dict:
        """오래된 레코드 아카이브"""
        older_than = data.get("older_than", "30d")
        status = data.get("status", ["completed", "cancelled"])

        return {
            "archived_count": 150,
            "archive_date": "2024-01-02",
            "storage_path": "archives/2024_01"
        }