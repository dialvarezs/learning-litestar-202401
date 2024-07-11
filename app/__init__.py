from litestar import Litestar

from app.controllers import CategoryController, ItemController, UserController
from app.database import db_plugin


app = Litestar(
    [ItemController, CategoryController, UserController],
    debug=True,
    plugins=[db_plugin],
)
