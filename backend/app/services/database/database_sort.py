# backend/app/services/database_sort.py
from typing import List, Dict, Any, Callable
from datetime import datetime
from enum import Enum


class SortDirection(str, Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


class SortType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    BOOLEAN = "boolean"
    RELATION = "relation"
    ROLLUP = "rollup"
    SELECT = "select"


class DatabaseSort:
    def __init__(self):
        self.type_handlers = {
            SortType.TEXT: self._compare_text,
            SortType.NUMBER: self._compare_number,
            SortType.DATE: self._compare_date,
            SortType.BOOLEAN: self._compare_boolean,
            SortType.RELATION: self._compare_relation,
            SortType.ROLLUP: self._compare_rollup,
            SortType.SELECT: self._compare_select,
        }

    def sort_records(self, records: List[Dict], sort_config: List[Dict]) -> List[Dict]:
        """레코드 정렬"""
        if not sort_config:
            return records

        def compare_records(record1: Dict, record2: Dict) -> int:
            for sort_rule in sort_config:
                property_name = sort_rule["property"]
                direction = sort_rule.get("direction", SortDirection.ASCENDING)
                sort_type = sort_rule.get("type", SortType.TEXT)

                value1 = record1.get(property_name)
                value2 = record2.get(property_name)

                # None 값 처리
                if value1 is None and value2 is None:
                    continue
                if value1 is None:
                    return 1
                if value2 is None:
                    return -1

                # 비교 함수 호출
                compare_result = self.type_handlers[sort_type](value1, value2)

                if compare_result != 0:
                    return compare_result if direction == SortDirection.ASCENDING else -compare_result

            return 0

        return sorted(records, key=functools.cmp_to_key(compare_records))

    def _compare_text(self, value1: str, value2: str) -> int:
        """텍스트 비교"""
        return (str(value1).lower() > str(value2).lower()) - (str(value1).lower() < str(value2).lower())

    def _compare_number(self, value1: Any, value2: Any) -> int:
        """숫자 비교"""
        try:
            num1 = float(value1)
            num2 = float(value2)
            return (num1 > num2) - (num1 < num2)
        except (ValueError, TypeError):
            return 0

    def _compare_date(self, value1: Any, value2: Any) -> int:
        """날짜 비교"""
        try:
            if isinstance(value1, str):
                date1 = datetime.fromisoformat(value1)
            else:
                date1 = value1

            if isinstance(value2, str):
                date2 = datetime.fromisoformat(value2)
            else:
                date2 = value2

            return (date1 > date2) - (date1 < date2)
        except (ValueError, TypeError):
            return 0

    def _compare_boolean(self, value1: bool, value2: bool) -> int:
        """불리언 비교"""
        return (bool(value1) > bool(value2)) - (bool(value1) < bool(value2))

    def _compare_relation(self, value1: List[Dict], value2: List[Dict]) -> int:
        """관계형 필드 비교 (관련 레코드 수 기준)"""
        len1 = len(value1) if isinstance(value1, list) else 0
        len2 = len(value2) if isinstance(value2, list) else 0
        return (len1 > len2) - (len1 < len2)

    def _compare_rollup(self, value1: Any, value2: Any) -> int:
        """롤업 값 비교"""
        # 롤업 타입에 따라 적절한 비교 함수 사용
        if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
            return self._compare_number(value1, value2)
        return self._compare_text(str(value1), str(value2))

    def _compare_select(self, value1: str, value2: str) -> int:
        """선택 옵션 비교"""
        # 옵션의 순서가 정의되어 있다면 그 순서를 사용
        options_order = self.get_options_order()
        if options_order:
            order1 = options_order.get(value1, float('inf'))
            order2 = options_order.get(value2, float('inf'))
            return (order1 > order2) - (order1 < order2)
        return self._compare_text(value1, value2)

    def get_options_order(self) -> Dict[str, int]:
        """선택 옵션의 정렬 순서 반환"""
        # 데이터베이스 스키마에서 정의된 옵션 순서 사용
        return {
            "높음": 0,
            "중간": 1,
            "낮음": 2,
            "완료": 0,
            "진행중": 1,
            "대기중": 2,
            "취소됨": 3,
        }


class SortBuilder:
    """정렬 설정 생성 도우미"""

    @staticmethod
    def create_sort_rule(
            property: str,
            direction: SortDirection = SortDirection.ASCENDING,
            sort_type: SortType = SortType.TEXT
    ) -> Dict:
        return {
            "property": property,
            "direction": direction,
            "type": sort_type
        }

    @staticmethod
    def create_sort_config(*rules: Dict) -> List[Dict]:
        return list(rules)


# 사용 예시:
"""
sort_builder = SortBuilder()
sort_config = sort_builder.create_sort_config(
    sort_builder.create_sort_rule("priority", SortDirection.DESCENDING, SortType.NUMBER),
    sort_builder.create_sort_rule("created_at", SortDirection.ASCENDING, SortType.DATE)
)
"""