import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books, sellers



# Тест на ручку создающую продавца

@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {"first_name":"Anna", "last_name":"Vashukova", "email":"ann_vash@gmail.com", "password":"16748"}
    response = await async_client.post("/api/v1/sellers/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == {
        "first_name": "Anna",
        "last_name": "Vashukova",
        "email": "ann_vash@gmail.com",
        "id": result_data["id"]
    }



# Тест на ручку получения списка продавцов

@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):

    seller = sellers.Seller(first_name="Anna", last_name="Vashukova", email="ann_vash@gmail.com", password="16748")
    seller_2 = sellers.Seller(first_name="Den", last_name="Andreev", email="dandreev@gmail.com", password="00000")

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2

    result_data = response.json()

    assert result_data == {
        "sellers": [
            {"first_name": "Anna", "last_name": "Vashukova", "email": "ann_vash@gmail.com", "id": seller.id},
            {"first_name": "Den", "last_name": "Andreev", "email": "dandreev@gmail.com", "id": seller_2.id},
        ]
    }




# Тест на ручку получения одного продавца

@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):

    seller = sellers.Seller(first_name="Anna", last_name="Vashukova", email="ann_vash@gmail.com", password="16748")

    db_session.add_all([seller])
    await db_session.flush()


    book = books.Book(author="Leo Tolstoy", title="War and Peace", year=1868, count_pages=1300, seller_id=seller.id)

    db_session.add(book)
    await db_session.flush()


    response = await async_client.get(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_200_OK


    assert response.json() == {
        "first_name": "Anna",
        "last_name": "Vashukova",
        "email": "ann_vash@gmail.com",
        "books": [{"author": "Leo Tolstoy", "title": "War and Peace", "year": 1868, "count_pages": 1300, "id": book.id, }]
    }





# Тест на ручку удаления продавца
    
@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    
    seller = sellers.Seller(first_name="Anna", last_name="Vashukova", email="ann_vash@gmail.com", password="16748")

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.Seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0




# Тест на ручку обновления данных о продавце

@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    
    seller = sellers.Seller(first_name="Anna", last_name="Vashukova", email="ann_vash@gmail.com", password="16748")

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/sellers/{seller.id}",
        json={"id": seller.id, "first_name": "Den", "last_name": "Andreev", "email": "dandreev@gmail.com", "password": "00000"},
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(sellers.Seller, seller.id)
    assert res.id == seller.id
    assert res.first_name == "Den"
    assert res.last_name == "Andreev"
    assert res.email == "dandreev@gmail.com"