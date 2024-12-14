class DefaultExceptions(Exception):
    """
    Default Exception
    """

    http_code = 500


class BadRequest(DefaultExceptions):
    """
    잘못 된 요청: 400
    """

    http_code = 400


class Unauthorized(DefaultExceptions):
    """
    권한 없음: 401
    """

    http_code = 401


class Forbidden(DefaultExceptions):
    """
    허용된 권한이 아님: 403
    """

    http_code = 403


class PageNotFound(DefaultExceptions):
    """
    찾을 수 없음: 404
    """

    http_code = 404
