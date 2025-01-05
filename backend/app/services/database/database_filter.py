# backend/app/services/database_filter.py
from typing import List, Dict, Any
from datetime import datetime
from enum import Enum


class FilterOperator(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "does_not_contain"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_THAN_EQUAL = "greater_than_equal"
    LESS_THAN_EQUAL = "less_than_equal"
    BETWEEN = "between"
    IS_EMPTY = "is_empty"
    IS_NOT_EMPTY = "is_not_empty"
    IN = "in"
    NOT_IN = "not_in"


class FilterGroup(str, Enum):
    AND = "and"
    OR = "or"


class DatabaseFilter:
    def __init__(self):
        self.operators = {
            FilterOperator.EQUALS: lambda x, y: x == y,
            FilterOperator.NOT_EQUALS: lambda x, y: x != y,
            FilterOperator.CONTAINS: lambda x, y: str(y).lower() in str(x).lower(),
            FilterOperator.DOES_NOT_CONTAIN: lambda x, y: str(y).lower() not in str(x).lower(),
            FilterOperator.STARTS_WITH: lambda x, y: str(x).lower().startswith(str(y).lower()),
            FilterOperator.ENDS_WITH: lambda x, y: str(x).lower().endswith(str(y).lower()),
            FilterOperator.GREATER_THAN: lambda x, y: x > y,
            FilterOperator.LESS_THAN: lambda x, y: x < y,
            FilterOperator.GREATER_THAN_EQUAL: lambda x, y: x >= y,
            FilterOperator.LESS_THAN_EQUAL: lambda x, y: x <= y,
            FilterOperator.BETWEEN: lambda x, y: y[0] <= x <= y[1],
            FilterOperator.IS_EMPTY: lambda x, y: x is None or x == "",
            FilterOperator.IS_NOT_EMPTY: lambda x, y: x is not None and x != "",
            FilterOperator.IN: lambda x, y: x in y,
            FilterOperator.NOT_IN: lambda x, y: x not in y,
        }

    def apply_filters(self, records: List[Dict], filters: Dict) -> List[Dict]:
        """필터 조건을 레코드에 적용"""
        if not filters:
            return records

        filtered_records = []
        for record in records:
            if self._evaluate_filter_group(record, filters):
                filtered_records.append(record)

        return filtered_records

    def _evaluate_filter_group(self, record: Dict, filter_group: Dict) -> bool:
        """필터 그룹 평가"""
        group_type = filter_group.get("type", FilterGroup.AND)
        conditions = filter_group.get("conditions", [])

        if group_type == FilterGroup.AND:
            return all(self._evaluate_condition(record, condition)
                       for condition in conditions)
        else:  # OR
            return any(self._evaluate_condition(record, condition)
                       for condition in conditions)

    def _evaluate_condition(self, record: Dict, condition: Dict) -> bool:
        """개별 필터 조건 평가"""
        if "conditions" in condition:  # Nested group
            return self._evaluate_filter_group(record, condition)

        property_name = condition["property"]
        operator = condition["operator"]
        value = condition["value"]

        record_value = record.get(property_name)

        # 날짜 값 처리
        if isinstance(value, str) and "date" in property_name.lower():
            try:
                value = datetime.fromisoformat(value)
                if isinstance(record_value, str):
                    record_value = datetime.fromisoformat(record_value)
            except ValueError:
                pass

        # 필터 연산자 적용
        try:
            return self.operators[operator](record_value, value)
        except Exception:
            return False


class FilterBuilder:
    """필터 생성 도우미"""

    @staticmethod
    def create_filter_group(type: FilterGroup = FilterGroup.AND) -> Dict:
        return {
            "type": type,
            "conditions": []
        }

    @staticmethod
    def add_condition(group: Dict, property: str, operator: FilterOperator, value: Any):
        group["conditions"].append({
            "property": property,
            "operator": operator,
            "value": value
        })

    @staticmethod
    def add_group(parent_group: Dict, child_group: Dict):
        parent_group["conditions"].append(child_group)


# 사용 예시:
"""
# 단순 필터
filter_builder = FilterBuilder()
filter_group = filter_builder.create_filter_group()
filter_builder.add_condition(filter_group, "status", FilterOperator.EQUALS, "완료")
filter_builder.add_condition(filter_group, "priority", FilterOperator.GREATER_THAN, 3)

# 복합 필터
main_group = filter_builder.create_filter_group(FilterGroup.OR)
sub_group1 = filter_builder.create_filter_group()
filter_builder.add_condition(sub_group1, "status", FilterOperator.EQUALS, "진행중")
filter_builder.add_condition(sub_group1, "priority", FilterOperator.GREATER_THAN, 4)

sub_group2 = filter_builder.create_filter_group()
filter_builder.add_condition(sub_group2, "status", FilterOperator.EQUALS, "완료")
filter_builder.add_condition(sub_group2, "date", FilterOperator.LESS_THAN, "2024-01-01")

filter_builder.add_group(main_group, sub_group1)
filter_builder.add_group(main_group, sub_group2)
"""