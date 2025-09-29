from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers import auth
from app import crud, schemas


# импортируем все роутеры
from app.routers import user_router, purchase_router, feeding_router, web

app = FastAPI(title="Cat Food Manager API")

# подключаем роутеры
app.include_router(user_router.router)
app.include_router(purchase_router.router)
app.include_router(feeding_router.router)
app.include_router(web.router)
app.include_router(auth.router)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="web")


@app.get("/users/html", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    users = crud.crud_user.get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.post("/purchases/add", response_class=HTMLResponse)
def add_purchase(
    request: Request,
    amount: int = Form(...),
    db: Session = Depends(get_db)
):
    purchase = schemas.PurchaseCreate(amount=amount)
    crud.crud_purchase.create_purchase(db, purchase)
    purchases = crud.crud_purchase.get_purchases(db)
    return templates.TemplateResponse("purchases.html", {"request": request, "purchases": purchases})

@app.get("/feedings/html", response_class=HTMLResponse)
def list_feedings(request: Request, db: Session = Depends(get_db)):
    feedings = crud.crud_feeding.get_feedings(db)
    return templates.TemplateResponse("feedings.html", {"request": request, "feedings": feedings})


@app.get("/feedings/add", response_class=HTMLResponse)
def add_feeding_form(request: Request):
    return templates.TemplateResponse("feeding_form.html", {"request": request})


@app.post("/feedings/add", response_class=HTMLResponse)
def add_feeding(
    request: Request,
    amount: int = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    feeding = schemas.FeedingCreate(amount=amount)
    crud.crud_feeding.create_feeding(db, feeding, user_id=user_id)
    feedings = crud.crud_feeding.get_feedings(db)
    return templates.TemplateResponse("feedings.html", {"request": request, "feedings": feedings})
