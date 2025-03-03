-- Database creation and tables setup SQL
CREATE DATABASE mall_customer_segmentation;
USE mall_customer_segmentation;

-- Create customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    gender VARCHAR(10),
    age INT,
    annual_income_k INT,
    spending_score INT
);

-- Create transactions table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    transaction_date DATE,
    amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create an index on customer_id for faster joins
CREATE INDEX idx_customer_id ON transactions(customer_id);