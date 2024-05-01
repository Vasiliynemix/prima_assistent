from src.bot.routers.start import router as start_router
from src.bot.routers.subscription import router as subscription_router
from src.bot.routers.boost_more import router as boost_more_router
from src.bot.routers.boost_settings import router as boost_settings_router
from src.bot.routers.back_to import router as back_to_router

routers = (
    start_router,
    subscription_router,
    boost_more_router,
    boost_settings_router,

    back_to_router,
)
