# backend/app/schemas/database.py
from enum import Enum
from typing import Optional, Dict, List, Union
from pydantic import BaseModel


class PropertyType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    PERSON = "person"
    FILE = "file"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    FORMULA = "formula"
    RELATION = "relation"
    ROLLUP = "rollup"
    CREATED_TIME = "created_time"
    CREATED_BY = "created_by"
    LAST_EDITED_TIME = "last_edited_time"
    LAST_EDITED_BY = "last_edited_by"


class FormulaType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"


class RollupFunction(str, Enum):
    COUNT = "count"
    COUNT_VALUES = "count_values"
    SUM = "sum"
    AVERAGE = "average"
    MIN = "min"
    MAX = "max"
    RANGE = "range"
    SHOW_ORIGINAL = "show_original"


class RelationConfig(BaseModel):
    database_id: str
    single_property: bool = False
    reverse_property: Optional[str] = None


class RollupConfig(BaseModel):
    relation_property_id: str
    relation_property_name: str
    target_property_id: str
    target_property_name: str
    function: RollupFunction


class FormulaConfig(BaseModel):
    expression: str
    output_type: FormulaType


class PropertyConfig(BaseModel):
    type: PropertyType
    name: str
    id: str

    # 선택 옵션 설정
    options: Optional[List[str]] = None

    # 숫자 형식 설정
    number_format: Optional[str] = None

    # 날짜 형식 설정
    date_format: Optional[str] = None

    # 관계형 설정
    relation_config: Optional[RelationConfig] = None

    # 롤업 설정
    rollup_config: Optional[RollupConfig] = None

    # 수식 설정
    formula_config: Optional[FormulaConfig] = None