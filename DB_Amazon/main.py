from fastapi import FastAPI

# Import Routers
from services import (customer, payment_method, product, category, coupons, seller, 
                      offer, orders, product_recommendations, returns, review, search_history,
                      shipping, shopping_cart, shopping_cart_product, order_items)  # Adjust paths if necessary

app = FastAPI(title="My Amazon API")

"""Include Routers"""
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(coupons.router)
app.include_router(seller.router)
app.include_router(offer.router)
app.include_router(orders.router)
app.include_router(payment_method.router)
app.include_router(product_recommendations.router)
app.include_router(returns.router)
app.include_router(review.router)
app.include_router(search_history.router)
app.include_router(shipping.router)
app.include_router(shopping_cart.router)
app.include_router(shopping_cart_product.router)
app.include_router(order_items.router)

@app.get("/")
async def root():
    """Root route"""
    return {"message": "Welcome!"}