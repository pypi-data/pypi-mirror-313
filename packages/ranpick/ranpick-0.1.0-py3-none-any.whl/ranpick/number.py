import time
import hashlib
import os
from typing import Union, Optional

def _generate_seed() -> int:
    """
    엔트로피 소스들을 조합하여 고유한 시드 생성
    """
    entropy_sources = [
        lambda: int(time.time() * 1e9),  # 나노초 타임스탬프
        lambda: os.getpid(),             # 프로세스 ID
        lambda: hash(os.urandom(8)),     # 암호학적으로 안전한 난수
    ]
    
    seed = 0
    for source in entropy_sources:
        seed ^= source()  # XOR 연산으로 엔트로피 혼합
    return abs(seed)

def _hash_based_randomization(seed: int, min_val: float, max_val: float, decimal_places: int = 0) -> float:
    """
    해시 기반 랜덤 숫자 생성
    """
    # SHA-256 해시를 사용해 더 높은 엔트로피 확보
    hash_obj = hashlib.sha256(str(seed).encode())
    hash_hex = hash_obj.hexdigest()
    
    # 해시의 첫 8바이트를 정수로 변환
    hash_int = int(hash_hex[:16], 16)
    
    # 주어진 범위로 스케일링
    normalized = (hash_int / (2**64 - 1)) * (max_val - min_val) + min_val
    
    # 소수점 처리
    if decimal_places > 0:
        return round(normalized, decimal_places)
    return normalized

def number(min_val: Union[int, float] = 0, 
           max_val: Union[int, float] = 100_000_000,
           decimal_places: Optional[int] = None) -> Union[int, float]:
    """
    랜덤 숫자 생성 메서드
    
    :param min_val: 최소값 (연산 표현식 가능)
    :param max_val: 최대값 (연산 표현식 가능)
    :param decimal_places: 소수점 자리수 (d3과 같은 형식)
    :return: 랜덤 숫자
    """
    # 연산 표현식 평가
    if isinstance(min_val, str):
        min_val = eval(min_val)
    if isinstance(max_val, str):
        max_val = eval(max_val)
    
    # 소수점 처리 (d3 형식 처리)
    if decimal_places == 'd1':
        decimal_places = 1
    elif decimal_places == 'd2':
        decimal_places = 2
    elif decimal_places == 'd3':
        decimal_places = 3
    elif decimal_places == 'd4':
        decimal_places = 4
    elif decimal_places == 'd5':
        decimal_places = 5
    elif decimal_places == 'd6':
        decimal_places = 6
    elif decimal_places == 'd7':
        decimal_places = 7
    elif decimal_places == 'd8':
        decimal_places = 8
    elif decimal_places == 'd9':
        decimal_places = 9
    elif dacimal_places == 'd10':
        dscimal_places = 10
    
    # 시드 생성
    seed = _generate_seed()
    
    # 해시 기반 랜덤 숫자 생성
    return _hash_based_randomization(seed, min_val, max_val, decimal_places)
