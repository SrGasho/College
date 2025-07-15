CREATE DATABASE amazon;

-- Crear tablas independientes primero
CREATE TABLE IF NOT EXISTS Category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS Seller (
    seller_id SERIAL PRIMARY KEY,
    seller_name VARCHAR(255) NOT NULL,
    seller_type VARCHAR(50),
    seller_rating DECIMAL(3, 2)
);

CREATE TABLE IF NOT EXISTS Customer (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    shipping_address VARCHAR(500) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    registration_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Payment_Method (
    payment_method_id SERIAL PRIMARY KEY,
    payment_type VARCHAR(50) NOT NULL,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE IF NOT EXISTS Shipping (
    shipping_id SERIAL PRIMARY KEY,
    shipping_company VARCHAR(255) NOT NULL,
    shipping_date DATE,
    estimated_delivery DATE,
    shipping_cost DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Coupons (
    coupons_id SERIAL PRIMARY KEY,
    discount_code VARCHAR(50) NOT NULL,
    discount_value DECIMAL(10, 2) NOT NULL,
    expiration_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Offer (
    offer_id SERIAL PRIMARY KEY,
    discount DECIMAL(10, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

-- Crear tablas que dependen de las anteriores
CREATE TABLE IF NOT EXISTS Product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity_available INT NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    seller_id INT,
    FOREIGN KEY (seller_id) REFERENCES Seller(seller_id)
);

CREATE TABLE IF NOT EXISTS Orders (
    orders_id SERIAL PRIMARY KEY,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_status VARCHAR(50) NOT NULL,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    payment_method_id INT,
    FOREIGN KEY (payment_method_id) REFERENCES Payment_Method(payment_method_id),
    shipping_id INT,
    FOREIGN KEY (shipping_id) REFERENCES Shipping(shipping_id)
);

CREATE TABLE IF NOT EXISTS Order_Items (
    order_item_id SERIAL PRIMARY KEY,
    orders_id INT,
    FOREIGN KEY (orders_id) REFERENCES Orders(orders_id),
    product_id INT,
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    coupon_id INT,  -- FK a Coupons
    FOREIGN KEY (coupon_id) REFERENCES Coupons(coupons_id),
    offer_id INT,  -- FK a Offer
    FOREIGN KEY (offer_id) REFERENCES Offer(offer_id)
);

CREATE TABLE IF NOT EXISTS Shopping_Cart (
    shopping_cart_id SERIAL PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE IF NOT EXISTS Shopping_Cart_Product (
    cart_id INT,
    FOREIGN KEY (cart_id) REFERENCES Shopping_Cart(shopping_cart_id),
    product_id INT,
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    quantity INT NOT NULL,
    PRIMARY KEY (cart_id, product_id)
);

CREATE TABLE IF NOT EXISTS Review (
    review_id SERIAL PRIMARY KEY,
    rating INT NOT NULL,
    comment TEXT,
    review_date DATE NOT NULL,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    product_id INT,
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

CREATE TABLE IF NOT EXISTS Returns (
    returns_id SERIAL PRIMARY KEY,
    return_date DATE NOT NULL,
    return_reason VARCHAR(255),
    return_status VARCHAR(50),
    order_item_id INT, -- Relacionado con Order_Items
    FOREIGN KEY (order_item_id) REFERENCES Order_Items(order_item_id)
);

CREATE TABLE IF NOT EXISTS Product_Recommendations (
    product_Recommendation_id SERIAL PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    recommended_product_id INT,
    FOREIGN KEY (recommended_product_id) REFERENCES Product(product_id),
    recommendation_date DATE -- Fecha de recomendación
);

CREATE TABLE IF NOT EXISTS Search_History (
    search_History_id SERIAL PRIMARY KEY,
    search_term VARCHAR(255) NOT NULL,
    search_date DATE NOT NULL,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);