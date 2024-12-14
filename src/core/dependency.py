from fastapi import Header


async def get_wanted_language(
    x_wanted_language: str = Header("ko", description="다국어 정보")
) -> str:
    return x_wanted_language or "ko"
