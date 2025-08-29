from fastapi import APIRouter, Request, HTTPException, status

router = APIRouter()


@router.get("/whoami")
async def whoami(request: Request):
    org_id = getattr(request.state, "org_id", None)
    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing X-Org-ID"
        )
    return {"org_id": org_id}
