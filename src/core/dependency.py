from fastapi import Header


async def get_wanted_language(
    x_wanted_language: str = Header("ko", description="다국어 정보")
) -> str:
    """헤더 x_wanted_language 에서 언어정보를 가져옴"""

    return x_wanted_language or "ko"
