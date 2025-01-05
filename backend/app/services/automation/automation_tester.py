# backend/app/services/automation_tester.py
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import copy


class AutomationTester:
    def __init__(self, automation_service, logger):
        self.automation_service = automation_service
        self.logger = logger

    async def test_rule(self, rule: Dict, test_data: Optional[Dict] = None) -> Dict:
        """자동화 규칙 테스트 실행"""
        test_result = {
            "success": False,
            "stages": [],
            "error": None
        }

        try:
            # 1. 트리거 조건 검사
            trigger_result = await self._test_trigger(rule["trigger"], test_data)
            test_result["stages"].append({
                "stage": "trigger",
                "success": trigger_result["success"],
                "details": trigger_result["details"]
            })

            if not trigger_result["success"]:
                return test_result

            # 2. 조건 검사
            if rule.get("conditions"):
                condition_result = await self._test_conditions(rule["conditions"], test_data)
                test_result["stages"].append({
                    "stage": "conditions",
                    "success": condition_result["success"],
                    "details": condition_result["details"]
                })

                if not condition_result["success"]:
                    return test_result

            # 3. 액션 시뮬레이션
            action_results = await self._simulate_actions(rule["actions"], test_data)
            test_result["stages"].append({
                "stage": "actions",
                "success": all(r["success"] for r in action_results),
                "details": action_results
            })

            test_result["success"] = all(
                stage["success"] for stage in test_result["stages"]
            )

        except Exception as e:
            test_result["error"] = str(e)

        return test_result

    async def _test_trigger(self, trigger: Dict, test_data: Optional[Dict]) -> Dict:
        """트리거 조건 테스트"""
        trigger_type = trigger["type"]

        if trigger_type == "scheduled":
            return {
                "success": True,
                "details": {
                    "next_execution": self._calculate_next_execution(trigger["schedule"])
                }
            }

        elif trigger_type in ["on_create", "on_update", "on_delete"]:
            return {
                "success": True,
                "details": {
                    "triggered_by": test_data if test_data else "테스트 데이터 필요"
                }
            }

        else:
            return {
                "success": False,
                "details": {"error": f"지원하지 않는 트리거 타입: {trigger_type}"}
            }

    async def _test_conditions(self, conditions: Dict, test_data: Dict) -> Dict:
        """조건 테스트"""
        from app.services.database_filter import DatabaseFilter
        filter_service = DatabaseFilter()

        try:
            matches = filter_service.apply_filters([test_data], conditions) != []
            return {
                "success": matches,
                "details": {
                    "conditions": conditions,
                    "test_data": test_data,
                    "matches": matches
                }
            }
        except Exception as e:
            return {
                "success": False,
                "details": {"error": str(e)}
            }

        async def _simulate_actions(self, actions: List[Dict], test_data: Dict) -> List[Dict]:
            """액션 시뮬레이션"""
            results = []

            for action in actions:
                action_type = action["type"]
                try:
                    if action_type == "update_record":
                        result = await self._simulate_update_record(action, test_data)

                    elif action_type == "create_record":
                        result = await self._simulate_create_record(action, test_data)

                    elif action_type == "send_notification":
                        result = await self._simulate_notification(action, test_data)

                    elif action_type == "api_call":
                        result = await self._simulate_api_call(action, test_data)

                    else:
                        result = {
                            "success": False,
                            "action_type": action_type,
                            "error": f"지원하지 않는 액션 타입: {action_type}"
                        }

                    results.append(result)

                except Exception as e:
                    results.append({
                        "success": False,
                        "action_type": action_type,
                        "error": str(e)
                    })

            return results

        async def _simulate_update_record(self, action: Dict, test_data: Dict) -> Dict:
            """레코드 업데이트 시뮬레이션"""
            try:
                # 실제 데이터베이스를 수정하지 않고 변경사항만 계산
                original_data = copy.deepcopy(test_data)
                updated_data = copy.deepcopy(test_data)

                for field, value in action["data"].items():
                    if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                        field_name = value[2:-2].strip()
                        value = test_data.get(field_name, value)
                    updated_data[field] = value

                return {
                    "success": True,
                    "action_type": "update_record",
                    "changes": {
                        "before": original_data,
                        "after": updated_data,
                        "modified_fields": list(action["data"].keys())
                    }
                }
            except Exception as e:
                return {
                    "success": False,
                    "action_type": "update_record",
                    "error": str(e)
                }

        async def _simulate_create_record(self, action: Dict, test_data: Dict) -> Dict:
            """레코드 생성 시뮬레이션"""
            try:
                new_record = {}
                for field, value in action["data"].items():
                    if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                        field_name = value[2:-2].strip()
                        value = test_data.get(field_name, value)
                    new_record[field] = value

                return {
                    "success": True,
                    "action_type": "create_record",
                    "new_record": new_record
                }
            except Exception as e:
                return {
                    "success": False,
                    "action_type": "create_record",
                    "error": str(e)
                }

        async def _simulate_notification(self, action: Dict, test_data: Dict) -> Dict:
            """알림 전송 시뮬레이션"""
            try:
                template = action["template"]
                message = template["message"]
                subject = template.get("subject", "")

                # 플레이스홀더 대체
                for key, value in test_data.items():
                    placeholder = f"{{{{{key}}}}}"
                    message = message.replace(placeholder, str(value))
                    subject = subject.replace(placeholder, str(value))

                return {
                    "success": True,
                    "action_type": "send_notification",
                    "notification": {
                        "channel": template["channel"],
                        "to": template["to"],
                        "subject": subject,
                        "message": message
                    }
                }
            except Exception as e:
                return {
                    "success": False,
                    "action_type": "send_notification",
                    "error": str(e)
                }

        async def _simulate_api_call(self, action: Dict, test_data: Dict) -> Dict:
            """API 호출 시뮬레이션"""
            try:
                # URL의 플레이스홀더 대체
                url = action["url"]
                for key, value in test_data.items():
                    placeholder = f"{{{{{key}}}}}"
                    url = url.replace(placeholder, str(value))

                # 요청 데이터 준비
                headers = action.get("headers", {})
                data = action.get("data", {}).copy()
                for key, value in data.items():
                    if isinstance(value, str):
                        for field, field_value in test_data.items():
                            placeholder = f"{{{{{field}}}}}"
                            if placeholder in value:
                                data[key] = value.replace(placeholder, str(field_value))

                return {
                    "success": True,
                    "action_type": "api_call",
                    "request": {
                        "method": action.get("method", "GET"),
                        "url": url,
                        "headers": headers,
                        "data": data
                    }
                }
            except Exception as e:
                return {
                    "success": False,
                    "action_type": "api_call",
                    "error": str(e)
                }

        def _calculate_next_execution(self, schedule: Dict) -> datetime:
            """다음 실행 시간 계산"""
            now = datetime.utcnow()

            if "interval" in schedule:
                interval = schedule["interval"]
                value = int(interval[:-1])
                unit = interval[-1].lower()

                if unit == 'm':
                    return now + timedelta(minutes=value)
                elif unit == 'h':
                    return now + timedelta(hours=value)
                elif unit == 'd':
                    return now + timedelta(days=value)

            elif "cron" in schedule:
                # TODO: Implement cron expression parsing
                return now + timedelta(hours=24)

            return now

    class TestDataGenerator:
        """테스트 데이터 생성기"""

        @staticmethod
        def generate_test_data(schema: Dict) -> Dict:
            """스키마 기반 테스트 데이터 생성"""
            test_data = {}

            for field, config in schema.get("properties", {}).items():
                field_type = config["type"]

                if field_type == "text":
                    test_data[field] = f"테스트 {field}"
                elif field_type == "number":
                    test_data[field] = 42
                elif field_type == "date":
                    test_data[field] = datetime.utcnow().isoformat()
                elif field_type == "select":
                    options = config.get("options", [])
                    test_data[field] = options[0] if options else "기본값"
                elif field_type == "multi_select":
                    options = config.get("options", [])
                    test_data[field] = options[:2] if options else ["태그1", "태그2"]
                elif field_type == "checkbox":
                    test_data[field] = True
                elif field_type == "email":
                    test_data[field] = "test@example.com"
                elif field_type == "url":
                    test_data[field] = "https://example.com"
                elif field_type == "phone":
                    test_data[field] = "010-1234-5678"

            return test_data