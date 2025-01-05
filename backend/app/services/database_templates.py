
from typing import Dict, List, Optional
from enum import Enum


class TemplateCategory(str, Enum):
    PROJECT_MANAGEMENT = "project_management"
    TASK_TRACKING = "task_tracking"
    CONTENT_CALENDAR = "content_calendar"
    CRM = "crm"
    INVENTORY = "inventory"
    HUMAN_RESOURCES = "human_resources"


class DatabaseTemplate:
    """데이터베이스 템플릿 정의"""

    @staticmethod
    def get_template(category: TemplateCategory, template_name: str) -> Dict:
        templates = {
            TemplateCategory.PROJECT_MANAGEMENT: {
                "project_tracker": {
                    "name": "프로젝트 트래커",
                    "schema": {
                        "properties": {
                            "project_name": {
                                "type": "text",
                                "name": "프로젝트명"
                            },
                            "status": {
                                "type": "select",
                                "name": "상태",
                                "options": ["계획", "진행중", "완료", "보류"]
                            },
                            "priority": {
                                "type": "select",
                                "name": "우선순위",
                                "options": ["높음", "중간", "낮음"]
                            },
                            "deadline": {
                                "type": "date",
                                "name": "마감일"
                            },
                            "assignee": {
                                "type": "person",
                                "name": "담당자"
                            },
                            "progress": {
                                "type": "number",
                                "name": "진행률",
                                "number_format": "percentage"
                            },
                            "description": {
                                "type": "text",
                                "name": "설명",
                                "long_text": true
                            }
                        },
                        "views": {
                            "default": {
                                "type": "table",
                                "sorts": [
                                    {
                                        "property": "priority",
                                        "direction": "ascending"
                                    },
                                    {
                                        "property": "deadline",
                                        "direction": "ascending"
                                    }
                                ]
                            },
                            "board": {
                                "type": "board",
                                "group_by": "status"
                            },
                            "calendar": {
                                "type": "calendar",
                                "date_property": "deadline"
                            }
                        }
                    }
                },
                "task_list": {
                    "name": "작업 목록",
                    "schema": {
                        "properties": {
                            "task": {
                                "type": "text",
                                "name": "작업"
                            },
                            "status": {
                                "type": "select",
                                "name": "상태",
                                "options": ["대기", "진행중", "검토", "완료"]
                            },
                            "due_date": {
                                "type": "date",
                                "name": "기한"
                            },
                            "assignee": {
                                "type": "person",
                                "name": "담당자"
                            },
                            "tags": {
                                "type": "multi_select",
                                "name": "태그",
                                "options": ["버그", "기능", "디자인", "문서"]
                            }
                        }
                    }
                }
            },

            TemplateCategory.CONTENT_CALENDAR: {
                "blog_posts": {
                    "name": "블로그 포스트 캘린더",
                    "schema": {
                        "properties": {
                            "title": {
                                "type": "text",
                                "name": "제목"
                            },
                            "status": {
                                "type": "select",
                                "name": "상태",
                                "options": ["아이디어", "초안", "검토중", "발행"]
                            },
                            "publish_date": {
                                "type": "date",
                                "name": "발행일"
                            },
                            "author": {
                                "type": "person",
                                "name": "작성자"
                            },
                            "category": {
                                "type": "select",
                                "name": "카테고리",
                                "options": ["기술", "디자인", "마케팅", "뉴스"]
                            },
                            "tags": {
                                "type": "multi_select",
                                "name": "태그"
                            },
                            "content": {
                                "type": "text",
                                "name": "내용",
                                "long_text": true
                            }
                        },
                        "views": {
                            "calendar": {
                                "type": "calendar",
                                "date_property": "publish_date"
                            },
                            "kanban": {
                                "type": "board",
                                "group_by": "status"
                            }
                        }
                    }
                }
            },

            TemplateCategory.CRM: {
                "customer_contacts": {
                    "name": "고객 연락처",
                    "schema": {
                        "properties": {
                            "name": {
                                "type": "text",
                                "name": "이름"
                            },
                            "company": {
                                "type": "text",
                                "name": "회사"
                            },
                            "email": {
                                "type": "email",
                                "name": "이메일"
                            },
                            "phone": {
                                "type": "phone_number",
                                "name": "전화번호"
                            },
                            "status": {
                                "type": "select",
                                "name": "상태",
                                "options": ["잠재고객", "상담중", "계약완료", "휴면"]
                            },
                            "last_contact": {
                                "type": "date",
                                "name": "최근연락일"
                            },
                            "notes": {
                                "type": "text",
                                "name": "메모",
                                "long_text": true
                            }
                        }
                    }
                }
            },

            TemplateCategory.INVENTORY: {
                "product_inventory": {
                    "name": "제품 재고 관리",
                    "schema": {
                        "properties": {
                            "product_name": {
                                "type": "text",
                                "name": "제품명"
                            },
                            "sku": {
                                "type": "text",
                                "name": "SKU"
                            },
                            "category": {
                                "type": "select",
                                "name": "카테고리"
                            },
                            "quantity": {
                                "type": "number",
                                "name": "수량"
                            },
                            "price": {
                                "type": "number",
                                "name": "가격",
                                "number_format": "currency"
                            },
                            "reorder_point": {
                                "type": "number",
                                "name": "재주문점"
                            },
                            "supplier": {
                                "type": "text",
                                "name": "공급업체"
                            }
                        },
                        "views": {
                            "inventory": {
                                "type": "table",
                                "filters": [
                                    {
                                        "property": "quantity",
                                        "operator": "less_than",
                                        "value": "reorder_point"
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }

        return templates.get(category, {}).get(template_name, None)

    @staticmethod
    def list_templates() -> Dict[str, List[Dict]]:
        """사용 가능한 모든 템플릿 목록 반환"""
        return {
            TemplateCategory.PROJECT_MANAGEMENT: [
                {"id": "project_tracker", "name": "프로젝트 트래커"},
                {"id": "task_list", "name": "작업 목록"}
            ],
            TemplateCategory.CONTENT_CALENDAR: [
                {"id": "blog_posts", "name": "블로그 포스트 캘린더"}
            ],
            TemplateCategory.CRM: [
                {"id": "customer_contacts", "name": "고객 연락처"}
            ],
            TemplateCategory.INVENTORY: [
                {"id": "product_inventory", "name": "제품 재고 관리"}
            ]
        }

    @staticmethod
    def create_from_template(category: TemplateCategory, template_name: str) -> Dict:
        """템플릿으로부터 새 데이터베이스 생성"""
        template = DatabaseTemplate.get_template(category, template_name)
        if not template:
            raise ValueError(f"Template not found: {category}/{template_name}")

        return {
            "name": template["name"],
            "schema": template["schema"],
            "records": []
        }

    @staticmethod
    def validate_template(template: Dict) -> bool:
        """템플릿 유효성 검사"""
        required_fields = ["name", "schema"]
        if not all(field in template for field in required_fields):
            return False

        if "properties" not in template["schema"]:
            return False

        return True