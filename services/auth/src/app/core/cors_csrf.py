from fastapi import Request, HTTPException, status

CSRf_HEADER = "X-CSRF-Token"
CSRf_COOKIE = "csrftoken"

async def csrf_protect(request: Request):
    if request.method in {"GET", "HEAD", "OPTIONS"}:
        return
    token_hdr = request.headers.get(CSRf_HEADER)
    token_ck = request.cookies.get(CSRf_COOKIE)
    if not token_hdr or not token_ck or token_hdr != token_ck:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF validation failed"
        )
