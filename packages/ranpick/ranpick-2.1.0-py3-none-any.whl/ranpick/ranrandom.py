# 파일 경로: ranpick/__init__.py
import time
import hashlib
import inspect
from typing import List, Tuple, Union

class RanpickError(Exception):
    """ranpick 모듈의 커스텀 에러 클래스"""
    def __init__(self, message: str, code: str):
        frame = inspect.currentframe().f_back
        line_number = frame.f_lineno
        self.message = f"ranpickError: (Line {line_number}) {message}: {code}"
        super().__init__(self.message)

def _generate_seed() -> int:
    """
    현재 시간을 기반으로 해시값을 생성하여 난수 시드를 반환하는 내부 함수.
    """
    current_time = time.time_ns()  # 나노초 단위 현재 시간
    time_hash = hashlib.sha256(str(current_time).encode()).hexdigest()
    seed = int(time_hash, 16)  # 16진수를 정수로 변환
    return seed

def ranrandom(*options: Union[str, Tuple[str, int]]) -> str:
    """
    리스트에서 랜덤으로 항목을 선택하는 함수.
    
    - 항목을 단순 문자열로 제공하거나, 확률을 지정 가능.
    - 확률 합이 100이 아니거나 항목이 2개 미만이면 에러 발생.
    - 확률을 지정하지 않은 항목은 자동으로 균등 분배.
    """
    if len(options) < 2:
        raise RanpickError(
            "At least two options must be provided",
            code=str(options)
        )

    items = []
    probabilities = []
    fixed_probability_sum = 0  # 명시적으로 지정된 확률 합
    unspecified_count = 0     # 확률이 명시되지 않은 항목 수

    for option in options:
        if isinstance(option, tuple):
            item, probability = option
            if not isinstance(probability, int) or probability < 0:
                raise RanpickError(
                    "Invalid probability value",
                    code=str(option)
                )
            items.append(item)
            probabilities.append(probability)
            fixed_probability_sum += probability
        elif isinstance(option, str):
            items.append(option)
            probabilities.append(None)  # 확률 미지정 상태로 추가
            unspecified_count += 1
        else:
            raise RanpickError(
                "Invalid option format",
                code=str(option)
            )

    # 확률 분배 로직
    if unspecified_count > 0:
        # 미지정 확률 값 계산
        remaining_probability = 100 - fixed_probability_sum
        if remaining_probability < 0:
            raise RanpickError(
                "The sum of specified probabilities exceeds 100",
                code=str(options)
            )
        equal_share = remaining_probability // unspecified_count
        for i in range(len(probabilities)):
            if probabilities[i] is None:
                probabilities[i] = equal_share

        # 남은 확률이 정확히 나누어떨어지지 않는 경우 보정
        remaining_mod = remaining_probability % unspecified_count
        for i in range(remaining_mod):
            probabilities[i] += 1

    # 최종 확률 합 검증
    if sum(probabilities) != 100:
        raise RanpickError(
            "The sum of each probability does not add up to 100",
            code=str(options)
        )

    # 누적 가중치 계산
    cumulative_weights = []
    cumulative_sum = 0
    for p in probabilities:
        cumulative_sum += p
        cumulative_weights.append(cumulative_sum)

    # 난수 생성 및 결과 선택
    random_seed = _generate_seed() % 100
    for idx, weight in enumerate(cumulative_weights):
        if random_seed < weight:
            return items[idx]
