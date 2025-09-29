# импортируем зависимости для работы с БД и схемами
from app.database import SessionLocal
from app.schemas.user import UserCreate
from app.schemas.purchase import PurchaseCreate
from app.schemas.feedings import FeedingCreate

# импортируем CRUD-модули напрямую вместо runpy
from app.crud import crud_user, crud_purchase, crud_feeding


def run():
    # создаём сессию с БД
    db = SessionLocal()

    print("=== Создание пользователя ===")
    user = crud_user.create_user(
        db, UserCreate(username="cat2", email="cat2@example.com", password="12345")
    )
    print(f"Создан пользователь: id={user.id}, username={user.username}")

    print("\n=== Поиск пользователя по email ===")
    found = crud_user.get_user_by_email(db, "cat2@example.com")
    print(f"Найден пользователь: id={found.id}, username={found.username}")

    print("\n=== Создание покупки ===")
    purchase = crud_purchase.create_purchase(
        db, PurchaseCreate(amount=3.0), user_id=user.id
    )
    print(f"Создана покупка: id={purchase.id}, amount={purchase.amount}")

    print("\n=== Создание кормления ===")
    feeding = crud_feeding.create_feeding(
        db, FeedingCreate(amount=40.0), user_id=user.id
    )
    print(f"Создано кормление: id={feeding.id}, amount={feeding.amount}")

    print("\n=== Все пользователи ===")
    for u in crud_user.get_users(db):
        print(f"- id={u.id}, username={u.username}")

    print("\n=== Все покупки ===")
    for p in crud_purchase.get_purchases(db):
        print(f"- id={p.id}, amount={p.amount}, user_id={p.user_id}")

    print("\n=== Все кормления ===")
    for f in crud_feeding.get_feedings(db):
        print(f"- id={f.id}, amount={f.amount}, user_id={f.user_id}")

    print("\n=== Удаление пользователя ===")
    deleted = crud_user.delete_user_by_id(db, user.id)
    if deleted:
        print(f"Удалён пользователь: id={deleted.id}, username={deleted.username}")
    else:
        print(f"Пользователь с id={user.id} не найден")

    print("\n=== Все пользователи после удаления ===")
    for u in crud_user.get_users(db):
        print(f"- id={u.id}, username={u.username}")


if __name__ == "__main__":
    run()
