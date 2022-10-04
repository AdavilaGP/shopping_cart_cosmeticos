from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient

class DataBase:
    client: AsyncIOMotorClient = None
    database_uri = config("DATABASE_URI")
    users_db = None
    addresses_db = None
    products_db = None
    orders_db = None
    order_itens_db = None

db = DataBase()

async def connect_db():
    try:
        db.client = AsyncIOMotorClient(
        db.database_uri,
        minPoolSize = 10,
        maxPoolSize = 10,
        tls = True,
        tlsAllowInvalidCertificates = True
        )
        db.users_db = db.client.shopping_cart.users
        db.addresses_db = db.client.shopping_cart.addresses
        db.products_db = db.client.shopping_cart.products
        db.orders_db = db.client.shopping_cart.orders
        db.order_itens_db = db.client.shopping_cart.order_itens

        print(await db.client.server_info())

    except Exception:
        print("Unable to connect to the server.")

async def disconnect_db():
    db.client.close()