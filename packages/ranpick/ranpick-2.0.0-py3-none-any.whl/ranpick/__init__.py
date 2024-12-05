import time
import hashlib
from typing import Union, Optional

def _generate_seed() -> int:
    """현재 시간을 나노초 단위로 해시하여 시드로 변환"""
    current_time = time.time_ns()  # 현재 시간 (나노초)
    seed_hash = hashlib.sha256(str(current_time).encode()).hexdigest()
    return int(seed_hash[:16], 16)  # 상위 16자리 숫자 변환 (정수)

def _random_from_seed(seed: int, start: float, end: float, decimal_places: int = 0) -> Union[int, float]:
    """지정된 범위에서 랜덤 숫자 생성 (정수 또는 소수)"""
    multiplier = 10 ** decimal_places if decimal_places > 0 else 1
    scaled_start = int(start * multiplier)
    scaled_end = int(end * multiplier)

    random_value = (seed % (scaled_end - scaled_start + 1)) + scaled_start
    return random_value / multiplier if decimal_places > 0 else random_value

def rannumber(
    start: Union[int, float] = 0, 
    end: Union[int, float] = 100000000, 
    decimal_option: Optional[str] = None
) -> Union[int, float]:
    """
    랜덤 숫자를 생성하는 메인 함수.
    
    - 기본적으로 0~100,000,000 사이의 정수를 반환합니다.
    - start와 end를 입력하면 해당 범위 내에서 값을 생성합니다.
    - decimal_option이 "dX" 형태라면 소수 X번째 자리까지 처리합니다.
    """
    if isinstance(start, str):
        start = eval(start)  # 문자열 수식 평가 (예: "1+4")
    if isinstance(end, str):
        end = eval(end)

    # 소수 자릿수 처리
    decimal_places = 0
    if decimal_option and decimal_option.startswith("d"):
        decimal_places = int(decimal_option[1:])

    # 시드 생성 및 랜덤 값 계산
    seed = _generate_seed()
    return _random_from_seed(seed, start, end, decimal_places)
