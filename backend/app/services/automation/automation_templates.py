
from typing import Dict, List
from enum import Enum


class TemplateCategory(str, Enum):
    PROJECT = "project"
    TASK = "task"
    NOTIFICATION = "notification"
    REMINDER = "reminder"


class AutomationTemplates:
    @staticmethod
    def get_templates() -> Dict[str, List[Dict]]:
        """미리 정의된 자동화 템플릿 반환"""
        return {
            TemplateCategory.PROJECT: [
                {
                    "id": "project_completion",
                    "name": "프로젝트 완료 자동화",
                    "description": "프로젝트가 완료되면 모든 관련 작업을 자동으로 완료 처리하고 팀원들에게 알림",
                    "rule": {
                        "trigger": {
                            "type": "on_update",
                            "database": "projects"
                        },
                        "conditions": {
                            "type": "and",
                            "conditions": [
                                {"property": "status", "operator": "equals", "value": "완료"}
                            ]
                        },
                        "actions": [
                            {
                                "type": "update_record",
                                "target": "tasks",
                                "filter": {"project_id": "{{id}}"},
                                "data": {
                                    "status": "완료",
                                    "completed_at": "{{now}}"
                                }
                            },
                            {
                                "type": "send_notification",
                                "channel": "email",
                                "template": {
                                    "to": "{{team_email}}",
                                    "subject": "프로젝트 완료 알림",
                                    "message": "프로젝트 {{name}}이(가) 완료되었습니다."
                                }
                            }
                        ]
                    }
                }
            ],

            TemplateCategory.TASK: [
                {
                    "id": "task_reminder",
                    "name": "작업 마감일 알림",
                    "description": "작업 마감일이 다가오면 자동으로 알림 발송",
                    "rule": {
                        "trigger": {
                            "type": "scheduled",
                            "schedule": {"interval": "1d"}
                        },
                        "conditions": {
                            "type": "and",
                            "conditions": [
                                {"property": "due_date", "operator": "less_than", "value": "{{today+3d}}"},
                                {"property": "status", "operator": "not_equals", "value": "완료"}
                            ]
                        },
                        "actions": [
                            {
                                "type": "send_notification",
                                "channel": "email",
                                "template": {
                                    "to": "{{assignee_email}}",
                                    "subject": "작업 마감일 알림",
                                    "message": "작업 {{name}}의 마감일이 {{due_date}}까지 입니다."
                                }
                            }
                        ]
                    }
                }
            ],

            TemplateCategory.NOTIFICATION: [
                {
                    "id": "status_change_notification",
                    "name": "상태 변경 알림",
                    "description": "데이터베이스 레코드의 상태가 변경되면 자동으로 알림 발송",
                    "rule": {
                        "trigger": {
                            "type": "on_update"
                        },
                        "conditions": {
                            "type": "and",
                            "conditions": [
                                {"property": "status", "operator": "changed"}
                            ]
                        },
                        "actions": [
                            {
                                "type": "send_notification",
                                "channel": "email",
                                "template": {
                                    "to": "{{assignee_email}}",
                                    "subject": "상태 변경 알림",
                                    "message": "{{name}}의 상태가 {{old_status}}에서 {{new_status}}로 변경되었습니다."
                                }
                            }
                        ]
                    }
                }
            ],

            TemplateCategory.REMINDER: [
                {
                    "id": "daily_summary",
                    "name": "일일 요약 보고서",
                    "description": "매일 지정된 시간에 진행 중인 작업 요약 보고서 발송",
                    "rule": {
                        "trigger": {
                            "type": "scheduled",
                            "schedule": {
                                "cron": "0 9 * * *"  # 매일 오전 9시
                            }
                        },
                        "conditions": {
                            "type": "and",
                            "conditions": [
                                {"property": "status", "operator": "equals", "value": "진행중"}
                            ]
                        },
                        "actions": [
                            {
                                "type": "api_call",
                                "method": "POST",
                                "url": "{{summary_api_url}}",
                                "data": {
                                    "date": "{{today}}",
                                    "status": "진행중"
                                }
                            },
                            {
                                "type": "send_notification",
                                "channel": "email",
                                "template": {
                                    "to": "{{team_email}}",
                                    "subject": "일일 작업 요약 ({{today}})",
                                    "message": "{{summary_report}}"
                                }
                            }
                        ]
                    }
                }
            ]
        }

    @staticmethod
    def get_template(category: str, template_id: str) -> Dict:
        """특정 템플릿 반환"""
        templates = AutomationTemplates.get_templates()
        category_templates = templates.get(category, [])
        return next(
            (template for template in category_templates if template["id"] == template_id),
            None
        )