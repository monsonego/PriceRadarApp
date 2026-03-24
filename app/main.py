from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query, Response, status
from sqlmodel import Session

from app.database import create_db_and_tables, get_session
from app.models import TrackedProduct, TrackedProductCreate, TrackedProductRead, TrackedProductUpdate
from app.repositories import ProductRepository
from app.services import ProductService

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    create_db_and_tables()
    yield


app = FastAPI(title="Shopping Price Alert API", version="0.1.0", lifespan=lifespan)


def get_product_service(session: Session = Depends(get_session)) -> ProductService:
    return ProductService(ProductRepository(session))


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products", response_model=list[TrackedProductRead])
def list_products(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
) -> list[TrackedProduct]:
    return service.list_products(offset=offset, limit=limit)


@app.get("/products/{product_id}", response_model=TrackedProductRead)
def get_product(
    product_id: int, service: ProductService = Depends(get_product_service)
) -> TrackedProduct:
    return service.get_product(product_id)


@app.post("/products", response_model=TrackedProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: TrackedProductCreate, service: ProductService = Depends(get_product_service)
) -> TrackedProduct:
    return service.create_product(product_in)


@app.put("/products/{product_id}", response_model=TrackedProductRead)
def update_product(
    product_id: int,
    product_in: TrackedProductUpdate,
    service: ProductService = Depends(get_product_service),
) -> TrackedProduct:
    return service.update_product(product_id, product_in)


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int, service: ProductService = Depends(get_product_service)
) -> Response:
    service.delete_product(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
