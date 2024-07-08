from litestar import Litestar

from app.controllers import CategoryController, ItemController
from app.database import db_plugin


app = Litestar(
    [ItemController, CategoryController],
    debug=True,
    plugins=[db_plugin],
)
