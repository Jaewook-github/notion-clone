# backend/app/services/database_compute.py
from typing import Any, List, Dict
from datetime import datetime
from statistics import mean
from app.schemas.database import RollupFunction, FormulaType
import re
import operator
from typing import Callable


class FormulaEvaluator:
    def __init__(self):
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne,
        }

        self.functions = {
            'now': lambda: datetime.now(),
            'today': lambda: datetime.now().date(),
            'if': lambda condition, true_val, false_val: true_val if condition else false_val,
            'concat': lambda *args: ''.join(str(arg) for arg in args),
            'length': len,
            'round': round,
            'abs': abs,
        }

    def evaluate(self, formula: str, record_data: Dict[str, Any]) -> Any:
        # 프로퍼티 참조 처리 (예: prop("필드명"))
        formula = self._replace_property_references(formula, record_data)

        try:
            # 파이썬 eval로 수식 계산 (보안상 제한된 환경에서 실행)
            return eval(formula, {"__builtins__": {}}, {
                **self.operators,
                **self.functions
            })
        except Exception as e:
            print(f"Formula evaluation error: {e}")
            return None

    def _replace_property_references(self, formula: str, record_data: Dict[str, Any]) -> str:
        """프로퍼티 참조를 실제 값으로 대체"""
        pattern = r'prop\("([^"]*)"\)'

        def replacer(match):
            field_name = match.group(1)
            return repr(record_data.get(field_name))

        return re.sub(pattern, replacer, formula)


class RollupCalculator:
    @staticmethod
    def calculate(values: List[Any], function: RollupFunction) -> Any:
        if not values:
            return None

        try:
            if function == RollupFunction.COUNT:
                return len(values)
            elif function == RollupFunction.COUNT_VALUES:
                return len([v for v in values if v is not None])
            elif function == RollupFunction.SUM:
                return sum(float(v) for v in values if v is not None)
            elif function == RollupFunction.AVERAGE:
                valid_values = [float(v) for v in values if v is not None]
                return mean(valid_values) if valid_values else None
            elif function == RollupFunction.MIN:
                return min(v for v in values if v is not None)
            elif function == RollupFunction.MAX:
                return max(v for v in values if v is not None)
            elif function == RollupFunction.RANGE:
                valid_values = [v for v in values if v is not None]
                if valid_values:
                    return max(valid_values) - min(valid_values)
                return None
            elif function == RollupFunction.SHOW_ORIGINAL:
                return values[0] if values else None
        except Exception as e:
            print(f"Rollup calculation error: {e}")
            return None


class DatabaseCompute:
    def __init__(self):
        self.formula_evaluator = FormulaEvaluator()
        self.rollup_calculator = RollupCalculator()

    async def compute_formula(self, formula_config: Dict, record_data: Dict) -> Any:
        """수식 프로퍼티 계산"""
        result = self.formula_evaluator.evaluate(
            formula_config["expression"],
            record_data
        )
        return self._convert_formula_result(result, formula_config["output_type"])

    async def compute_rollup(self,
                             rollup_config: Dict,
                             related_records: List[Dict],
                             target_property: str) -> Any:
        """롤업 프로퍼티 계산"""
        values = [record.get(target_property) for record in related_records]
        return self.rollup_calculator.calculate(values, rollup_config["function"])

    def _convert_formula_result(self, result: Any, output_type: FormulaType) -> Any:
        """수식 결과를 지정된 출력 타입으로 변환"""
        try:
            if output_type == FormulaType.TEXT:
                return str(result)
            elif output_type == FormulaType.NUMBER:
                return float(result)
            elif output_type == FormulaType.BOOLEAN:
                return bool(result)
            elif output_type == FormulaType.DATE:
                if isinstance(result, datetime):
                    return result
                return datetime.fromisoformat(str(result))
        except Exception:
            return None
        return result