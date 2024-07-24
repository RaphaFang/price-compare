# from django.dispatch import receiver
# from myapp.signals import startup_signal, shutdown_signal
# from myapp.db.sql import build_async_sql_pool, close_async_sql_pool
# import asyncio

# @receiver(startup_signal)
# async def on_startup(sender, **kwargs):
#     print("App has started.")

#     app_state = kwargs['app_state']
#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(build_async_sql_pool(app_state))
#     await build_async_sql_pool(app_state)


# @receiver(shutdown_signal)
# async def on_shutdown(sender, **kwargs):
#     print("App is shutting down.")

#     app_state = kwargs['app_state']
#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(close_async_sql_pool(app_state))
#     await close_async_sql_pool(app_state)


# # async def this_lifespan(app): # 學到yield 第一次發現可以用在這裡
# #     app.async_sql_pool = await build_async_sql_pool()
# #     logger.info("start")
# #     yield
# #     await close_async_sql_pool(app.async_sql_pool)