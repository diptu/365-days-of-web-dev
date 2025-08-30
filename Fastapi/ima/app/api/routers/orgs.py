# app/v1/routers/orgs.py
from sqlalchemy.exc import IntegrityError


@router.post("/v1/orgs", response_model=OrgOut, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrgCreate, db: AsyncSession = Depends(get_db)
) -> OrgOut:
    if await get_org_by_slug(db, payload.slug):
        raise HTTPException(status_code=409, detail="slug_already_exists")
    try:
        org = await create_org(db, name=payload.name, slug=payload.slug)
    except IntegrityError:
        # unique slug race
        await db.rollback()
        raise HTTPException(status_code=409, detail="slug_already_exists")
    return OrgOut.model_validate(org)
