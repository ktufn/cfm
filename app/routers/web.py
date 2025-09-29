from fastapi import Form, Depends, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.core.auth import create_access_token, decode_access_token

router = APIRouter(prefix="/web", tags=["web"])
templates = Jinja2Templates(directory="app/templates")


# ------------------------
# Главная
# ------------------------
@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    """Главная страница — остаток корма и последние кормления (только для авторизованных)."""
    user_email = request.cookies.get("user_email")
    token = request.cookies.get("access_token")
    payload = decode_access_token(token) if token else None

    if not payload:
        # Если не авторизован → перебрасываем на страницу логина
        return RedirectResponse(url="/web/login", status_code=303)

    # Остаток корма
    total_purchased = sum(p.amount for p in crud.crud_purchase.get_purchases(db))
    total_fed = sum(f.amount for f in crud.crud_feeding.get_feedings(db))
    total_food = total_purchased - total_fed

    # Последние 5 кормлений
    feedings = crud.crud_feeding.get_feedings(db)
    last_feedings = feedings[-5:] if feedings else []

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "user_email": user_email,
            "total_food": total_food,
            "last_feedings": last_feedings
        }
    )

# ------------------------
# Регистрация
# ------------------------
@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    """Страница регистрации"""
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Создание нового пользователя"""
    user = crud.crud_user.get_user_by_email(db, email=email)
    if user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email уже зарегистрирован"})
    crud.crud_user.create_user(db, schemas.UserCreate(email=email, password=password))
    return templates.TemplateResponse("login.html", {"request": request, "msg": "Регистрация успешна, войдите"})


# ------------------------
# Логин
# ------------------------
@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    """Страница входа"""
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Обработка входа — проверка пароля, установка cookie"""
    user = crud.crud_user.authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный логин или пароль"})

    token = create_access_token({"sub": user.email})
    response = RedirectResponse(url="/web/", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)
    response.set_cookie(key="user_email", value=user.email)
    response.set_cookie(key="user_id", value=str(user.id))
    return response


# ------------------------
# Логаут
# ------------------------
@router.get("/logout")
def logout():
    """Выход — удаляем cookie"""
    response = RedirectResponse(url="/web/", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie("user_email")
    response.delete_cookie("user_id")
    return response


# ------------------------
# Покупки
# ------------------------
@router.get("/purchases", response_class=HTMLResponse)
def list_purchases(request: Request, db: Session = Depends(get_db)):
    """Список всех покупок"""
    purchases = crud.crud_purchase.get_purchases(db)
    return templates.TemplateResponse("purchases.html", {"request": request, "purchases": purchases})


@router.get("/purchases/add", response_class=HTMLResponse)
def add_purchase_form(request: Request):
    """Форма добавления покупки (только для авторизованных)"""
    token = request.cookies.get("access_token")
    if not token or not decode_access_token(token):
        return RedirectResponse(url="/web/login", status_code=303)
    return templates.TemplateResponse("purchase_form.html", {"request": request})


@router.post("/purchases/add", response_class=HTMLResponse)
def add_purchase(
    request: Request,
    amount: int = Form(...),
    db: Session = Depends(get_db),
):
    """Добавление покупки (только для авторизованных)"""
    token = request.cookies.get("access_token")
    payload = decode_access_token(token) if token else None
    if not payload:
        return RedirectResponse(url="/web/login", status_code=303)

    # Берём user_id из cookie
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/web/login", status_code=303)

    purchase = schemas.PurchaseCreate(amount=amount)
    crud.crud_purchase.create_purchase(db, purchase, user_id=int(user_id))

    purchases = crud.crud_purchase.get_purchases(db)
    return templates.TemplateResponse("purchases.html", {"request": request, "purchases": purchases})


# ------------------------
# Кормления
# ------------------------
@router.get("/feedings", response_class=HTMLResponse)
def list_feedings(request: Request, db: Session = Depends(get_db)):
    """Список всех кормлений"""
    feedings = crud.crud_feeding.get_feedings(db)
    return templates.TemplateResponse("feedings.html", {"request": request, "feedings": feedings})


@router.get("/feedings/add", response_class=HTMLResponse)
def add_feeding_form(request: Request):
    """Форма добавления кормления (только для авторизованных)"""
    token = request.cookies.get("access_token")
    if not token or not decode_access_token(token):
        return RedirectResponse(url="/web/login", status_code=303)
    return templates.TemplateResponse("feeding_form.html", {"request": request})


@router.post("/feedings/add", response_class=HTMLResponse)
def add_feeding(
    request: Request,
    amount: int = Form(...),
    db: Session = Depends(get_db),
):
    """Добавление кормления (только для авторизованных)"""
    token = request.cookies.get("access_token")
    payload = decode_access_token(token) if token else None
    if not payload:
        return RedirectResponse(url="/web/login", status_code=303)

    # Берём user_id из cookie
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/web/login", status_code=303)

    feeding = schemas.FeedingCreate(amount=amount)
    crud.crud_feeding.create_feeding(db, feeding, user_id=int(user_id))
    feedings = crud.crud_feeding.get_feedings(db)
    return templates.TemplateResponse("feedings.html", {"request": request, "feedings": feedings})
