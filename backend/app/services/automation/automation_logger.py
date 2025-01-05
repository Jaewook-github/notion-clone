# backend/app/services/automation_logger.py
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
import json


class LogLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class LogStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class AutomationLogger:
    def __init__(self, db_session):
        self.db = db_session

    async def log_execution(self,
                            rule_id: str,
                            rule_name: str,
                            trigger_type: str,
                            status: LogStatus,
                            details: Optional[Dict] = None,
                            error: Optional[str] = None) -> None:
        """자동화 규칙 실행 로그 기록"""
        log_entry = {
            "rule_id": rule_id,
            "rule_name": rule_name,
            "trigger_type": trigger_type,
            "status": status,
            "details": details or {},
            "error": error,
            "timestamp": datetime.utcnow()
        }

        await self.db.execute(
            """INSERT INTO automation_logs 
               (rule_id, rule_name, trigger_type, status, details, error, timestamp)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                log_entry["rule_id"],
                log_entry["rule_name"],
                log_entry["trigger_type"],
                log_entry["status"],
                json.dumps(log_entry["details"]),
                log_entry["error"],
                log_entry["timestamp"]
            )
        )

    async def get_logs(self,
                       rule_id: Optional[str] = None,
                       status: Optional[LogStatus] = None,
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None,
                       limit: int = 100) -> List[Dict]:
        """로그 조회"""
        query = "SELECT * FROM automation_logs WHERE 1=1"
        params = []

        if rule_id:
            query += " AND rule_id = %s"
            params.append(rule_id)

        if status:
            query += " AND status = %s"
            params.append(status)

        if start_date:
            query += " AND timestamp >= %s"
            params.append(start_date)

        if end_date:
            query += " AND timestamp <= %s"
            params.append(end_date)

        query += " ORDER BY timestamp DESC LIMIT %s"
        params.append(limit)

        logs = await self.db.fetch_all(query, params)
        return [dict(log) for log in logs]

    async def get_rule_statistics(self, rule_id: str) -> Dict:
        """규칙별 실행 통계"""
        query = """
            SELECT 
                COUNT(*) as total_executions,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_executions,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_executions,
                MAX(timestamp) as last_execution
            FROM automation_logs
            WHERE rule_id = %s
        """

        stats = await self.db.fetch_one(query, rule_id)
        return dict(stats)

    async def clear_old_logs(self, days: int = 30) -> int:
        """오래된 로그 삭제"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = "DELETE FROM automation_logs WHERE timestamp < %s"
        result = await self.db.execute(query, cutoff_date)
        return result