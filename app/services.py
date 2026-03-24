from fastapi import HTTPException, status

from app.models import TrackedProduct, TrackedProductCreate, TrackedProductUpdate
from app.repositories import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def list_products(self, *, offset: int = 0, limit: int = 100) -> list[TrackedProduct]:
        return self.repository.list(offset=offset, limit=limit)

    def get_product(self, product_id: int) -> TrackedProduct:
        product = self.repository.get(product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    def create_product(self, product_in: TrackedProductCreate) -> TrackedProduct:
        return self.repository.create(product_in)

    def update_product(self, product_id: int, product_in: TrackedProductUpdate) -> TrackedProduct:
        product = self.get_product(product_id)
        return self.repository.update(product, product_in)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        self.repository.delete(product)
