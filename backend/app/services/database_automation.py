
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import asyncio
from app.core.config import settings


class TriggerType(str, Enum):
    ON_CREATE = "on_create"
    ON_UPDATE = "on_update"
    ON_DELETE = "on_delete"
    SCHEDULED = "scheduled"
    CONDITION_MET = "condition_met"


class ActionType(str, Enum):
    UPDATE_RECORD = "update_record"
    CREATE_RECORD = "create_record"
    DELETE_RECORD = "delete_record"
    SEND_NOTIFICATION = "send_notification"
    EXECUTE_SCRIPT = "execute_script"
    API_CALL = "api_call"


class AutomationRule:
    def __init__(self,
                 name: str,
                 trigger: Dict,
                 actions: List[Dict],
                 conditions: Optional[Dict] = None,
                 enabled: bool = True):
        self.name = name
        self.trigger = trigger
        self.actions = actions
        self.conditions = conditions
        self.enabled = enabled


class DatabaseAutomation:
    def __init__(self):
        self._rules: List[AutomationRule] = []
        self._scheduled_tasks = {}

    async def add_rule(self, rule: AutomationRule):
        """자동화 규칙 추가"""
        self._rules.append(rule)

        # 스케줄된 트리거인 경우 스케줄러에 등록
        if rule.trigger["type"] == TriggerType.SCHEDULED:
            await self._schedule_rule(rule)

    async def remove_rule(self, rule_name: str):
        """자동화 규칙 제거"""
        self._rules = [r for r in self._rules if r.name != rule_name]
        if rule_name in self._scheduled_tasks:
            self._scheduled_tasks[rule_name].cancel()
            del self._scheduled_tasks[rule_name]

    async def handle_event(self, event_type: TriggerType, record: Dict, database_id: str):
        """이벤트 처리"""
        for rule in self._rules:
            if not rule.enabled or rule.trigger["type"] != event_type:
                continue

            if await self._check_conditions(rule.conditions, record):
                await self._execute_actions(rule.actions, record, database_id)

    async def _check_conditions(self, conditions: Optional[Dict], record: Dict) -> bool:
        """조건 검사"""
        if not conditions:
            return True

        from app.services.database_filter import DatabaseFilter
        filter_service = DatabaseFilter()

        return filter_service.apply_filters([record], conditions) != []

    async def _execute_actions(self, actions: List[Dict], record: Dict, database_id: str):
        """액션 실행"""
        for action in actions:
            try:
                if action["type"] == ActionType.UPDATE_RECORD:
                    await self._update_record(database_id, record["id"], action["data"])

                elif action["type"] == ActionType.CREATE_RECORD:
                    new_record = action["data"].copy()
                    for key, value in new_record.items():
                        if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                            field_name = value[2:-2].strip()
                            new_record[key] = record.get(field_name)

                    await self._create_record(database_id, new_record)

                elif action["type"] == ActionType.DELETE_RECORD:
                    await self._delete_record(database_id, record["id"])

                elif action["type"] == ActionType.SEND_NOTIFICATION:
                    await self._send_notification(action["template"], record)

                elif action["type"] == ActionType.EXECUTE_SCRIPT:
                    await self._execute_script(action["script"], record)

                elif action["type"] == ActionType.API_CALL:
                    await self._make_api_call(action["config"], record)

            except Exception as e:
                print(f"Error executing action {action['type']}: {e}")

    async def _schedule_rule(self, rule: AutomationRule):
        """규칙 스케줄링"""
        schedule = rule.trigger.get("schedule", {})

        if "interval" in schedule:
            interval = self._parse_interval(schedule["interval"])
            task = asyncio.create_task(self._run_scheduled_task(rule, interval))
            self._scheduled_tasks[rule.name] = task

        elif "cron" in schedule:
            # TODO: Implement cron-style scheduling
            pass

        async def _run_scheduled_task(self, rule: AutomationRule, interval: timedelta):
            """스케줄된 태스크 실행"""
            while True:
                try:
                    if not rule.enabled:
                        break

                    databases = await self._get_relevant_databases(rule)
                    for db_id in databases:
                        records = await self._get_database_records(db_id)
                        for record in records:
                            if await self._check_conditions(rule.conditions, record):
                                await self._execute_actions(rule.actions, record, db_id)

                    await asyncio.sleep(interval.total_seconds())
                except Exception as e:
                    print(f"Error in scheduled task {rule.name}: {e}")
                    await asyncio.sleep(60)  # 오류 발생 시 1분 대기

        def _parse_interval(self, interval_str: str) -> timedelta:
            """간격 문자열 파싱"""
            value = int(interval_str[:-1])
            unit = interval_str[-1].lower()

            if unit == 'm':
                return timedelta(minutes=value)
            elif unit == 'h':
                return timedelta(hours=value)
            elif unit == 'd':
                return timedelta(days=value)
            else:
                raise ValueError(f"Invalid interval format: {interval_str}")

        async def _update_record(self, database_id: str, record_id: str, data: Dict):
            """레코드 업데이트"""
            async with DatabaseSession() as db:
                await db.execute(
                    """UPDATE database_records 
                       SET data = jsonb_set(data, '{%s}', '%s'::jsonb)
                       WHERE id = %s AND database_id = %s""",
                    (data,)
                )

        async def _create_record(self, database_id: str, data: Dict):
            """레코드 생성"""
            async with DatabaseSession() as db:
                await db.execute(
                    """INSERT INTO database_records (database_id, data)
                       VALUES (%s, %s)""",
                    (database_id, json.dumps(data))
                )

        async def _delete_record(self, database_id: str, record_id: str):
            """레코드 삭제"""
            async with DatabaseSession() as db:
                await db.execute(
                    """DELETE FROM database_records 
                       WHERE id = %s AND database_id = %s""",
                    (record_id, database_id)
                )

        async def _send_notification(self, template: Dict, record: Dict):
            """알림 전송"""
            # 템플릿의 플레이스홀더를 레코드 데이터로 대체
            message = template["message"]
            for key, value in record.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in message:
                    message = message.replace(placeholder, str(value))

            # 알림 채널에 따른 전송 처리
            if template["channel"] == "email":
                await self._send_email(
                    template["to"],
                    template["subject"],
                    message
                )
            elif template["channel"] == "webhook":
                await self._send_webhook(
                    template["url"],
                    message
                )

        async def _execute_script(self, script: Dict, record: Dict):
            """스크립트 실행"""
            # 샌드박스 환경에서 스크립트 실행
            context = {
                "record": record,
                "utilities": ScriptUtilities(),
                "result": None
            }

            try:
                exec(script["code"], context)
                return context.get("result")
            except Exception as e:
                print(f"Script execution error: {e}")
                return None

        async def _make_api_call(self, config: Dict, record: Dict):
            """외부 API 호출"""
            import aiohttp

            # URL의 플레이스홀더 대체
            url = config["url"]
            for key, value in record.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in url:
                    url = url.replace(placeholder, str(value))

            # 요청 데이터 준비
            headers = config.get("headers", {})
            data = config.get("data", {}).copy()
            for key, value in data.items():
                if isinstance(value, str):
                    for field, field_value in record.items():
                        placeholder = f"{{{{{field}}}}}"
                        if placeholder in value:
                            data[key] = value.replace(placeholder, str(field_value))

            # API 호출
            async with aiohttp.ClientSession() as session:
                method = config.get("method", "GET").upper()
                try:
                    if method == "GET":
                        async with session.get(url, headers=headers, params=data) as response:
                            return await response.json()
                    else:
                        async with session.request(method, url, headers=headers, json=data) as response:
                            return await response.json()
                except Exception as e:
                    print(f"API call error: {e}")
                    return None

    class ScriptUtilities:
        """스크립트에서 사용할 수 있는 유틸리티 함수들"""

        def format_date(self, date: datetime, format_str: str = "%Y-%m-%d") -> str:
            """날짜 포맷팅"""
            return date.strftime(format_str)

        def calculate_duration(self, start: datetime, end: datetime) -> timedelta:
            """기간 계산"""
            return end - start

        def parse_date(self, date_str: str) -> datetime:
            """날짜 문자열 파싱"""
            return datetime.fromisoformat(date_str)

    # 자동화 규칙 예시:
    """
    # 프로젝트가 완료되면 관련된 모든 작업을 완료 상태로 변경
    project_completion_rule = AutomationRule(
        name="project_completion",
        trigger={
            "type": TriggerType.ON_UPDATE,
            "database": "projects"
        },
        conditions={
            "type": "and",
            "conditions": [
                {"property": "status", "operator": "equals", "value": "완료"}
            ]
        },
        actions=[
            {
                "type": ActionType.UPDATE_RECORD,
                "database": "tasks",
                "data": {
                    "status": "완료",
                    "completed_at": "{{now}}"
                },
                "filter": {
                    "property": "project_id",
                    "operator": "equals",
                    "value": "{{id}}"
                }
            },
            {
                "type": ActionType.SEND_NOTIFICATION,
                "template": {
                    "channel": "email",
                    "to": "{{assignee_email}}",
                    "subject": "프로젝트 완료 알림",
                    "message": "프로젝트 '{{name}}'가 완료되었습니다."
                }
            }
        ]
    )

    # 매일 자정에 기한이 지난 작업 체크
    overdue_task_check = AutomationRule(
        name="overdue_task_check",
        trigger={
            "type": TriggerType.SCHEDULED,
            "schedule": {
                "cron": "0 0 * * *"  # 매일 자정
            }
        },
        conditions={
            "type": "and",
            "conditions": [
                {"property": "due_date", "operator": "less_than", "value": "{{today}}"},
                {"property": "status", "operator": "not_equals", "value": "완료"}
            ]
        },
        actions=[
            {
                "type": ActionType.SEND_NOTIFICATION,
                "template": {
                    "channel": "email",
                    "to": "{{assignee_email}}",
                    "subject": "기한 초과 작업 알림",
                    "message": "작업 '{{name}}'의 기한이 지났습니다."
                }
            }
        ]
    )
    """