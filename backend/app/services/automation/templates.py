# backend/app/services/automation/templates.py

class AutomationTemplates:
    @staticmethod
    def get_templates() -> Dict[str, List[Dict]]:
        return {
            "PROJECT_MANAGEMENT": [
                {
                    "id": "agile_sprint",
                    "name": "애자일 스프린트 관리",
                    "description": "스프린트 시작/종료 자동화 및 보고서 생성",
                    "template": {
                        "trigger": {"type": "scheduled", "schedule": "0 9 * * 1"},  # 매주 월요일
                        "actions": [
                            {"type": "create_record", "database": "sprints"},
                            {"type": "send_notification", "channel": "team"},
                            {"type": "sync_calendar", "calendar": "team"},
                            {"type": "create_github_issue", "label": "sprint-planning"}
                        ]
                    }
                },
                {
                    "id": "milestone_tracking",
                    "name": "마일스톤 트래킹",
                    "description": "프로젝트 마일스톤 모니터링 및 보고",
                    "template": {
                        "trigger": {"type": "on_update", "database": "milestones"},
                        "actions": [
                            {"type": "update_dashboard"},
                            {"type": "generate_report"},
                            {"type": "post_to_slack"}
                        ]
                    }
                }
            ],

            "DOCUMENT_MANAGEMENT": [
                {
                    "id": "document_approval",
                    "name": "문서 승인 워크플로우",
                    "description": "문서 검토 및 승인 프로세스 자동화",
                    "template": {
                        "trigger": {"type": "on_create", "database": "documents"},
                        "actions": [
                            {"type": "send_notification", "to": "approvers"},
                            {"type": "create_record", "database": "approvals"},
                            {"type": "export_to_pdf", "backup": true}
                        ]
                    }
                },
                {
                    "id": "document_archiving",
                    "name": "문서 자동 아카이브",
                    "description": "오래된 문서 자동 아카이브 및 백업",
                    "template": {
                        "trigger": {"type": "scheduled", "schedule": "0 0 1 * *"},  # 매월 1일
                        "actions": [
                            {"type": "archive_records"},
                            {"type": "create_backup"},
                            {"type": "clean_old_records"}
                        ]
                    }
                }
            ],

            "DATA_ANALYSIS": [
                {
                    "id": "sales_metrics",
                    "name": "매출 메트릭스 분석",
                    "description": "주간/월간 매출 데이터 분석 및 보고서 생성",
                    "template": {
                        "trigger": {"type": "scheduled", "schedule": "0 7 * * 1"},  # 매주 월요일
                        "actions": [
                            {"type": "calculate_metrics"},
                            {"type": "generate_report"},
                            {"type": "export_to_excel"},
                            {"type": "send_notification", "channel": "executives"}
                        ]
                    }
                },
                {
                    "id": "performance_tracking",
                    "name": "성과 추적",
                    "description": "KPI 및 성과 지표 자동 추적",
                    "template": {
                        "trigger": {"type": "scheduled", "schedule": "0 9 * * *"},  # 매일
                        "actions": [
                            {"type": "run_data_analysis"},
                            {"type": "update_dashboard"},
                            {"type": "post_to_slack"}
                        ]
                    }
                }
            ],

            "SOCIAL_MEDIA": [
                {
                    "id": "content_scheduler",
                    "name": "컨텐츠 스케줄러",
                    "description": "소셜 미디어 포스팅 자동화",
                    "template": {
                        "trigger": {"type": "condition_met", "database": "content"},
                        "actions": [
                            {"type": "post_to_social"},
                            {"type": "send_telegram"},
                            {"type": "update_record"}
                        ]
                    }
                }
            ],

            "CUSTOMER_SERVICE": [
                {
                    "id": "ticket_escalation",
                    "name": "티켓 에스컬레이션",
                    "description": "고객 문의 자동 에스컬레이션",
                    "template": {
                        "trigger": {"type": "condition_met", "database": "tickets"},
                        "actions": [
                            {"type": "send_sms", "to": "manager"},
                            {"type": "create_trello_card"},
                            {"type": "post_to_slack", "channel": "urgent"}
                        ]
                    }
                }
            ],

            "INVENTORY_MANAGEMENT": [
                {
                    "id": "stock_alerts",
                    "name": "재고 알림",
                    "description": "재고 부족 시 자동 알림",
                    "template": {
                        "trigger": {"type": "condition_met", "database": "inventory"},
                        "actions": [
                            {"type": "send_notification"},
                            {"type": "create_record", "database": "orders"},
                            {"type": "post_to_slack"}
                        ]
                    }
                }
            ]
        }