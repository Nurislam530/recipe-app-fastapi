from pydantic import BaseModel


class RecipeCreate(BaseModel):
    id: int
    name: str
    ingredients: list
    description: str
    owner_id: int
