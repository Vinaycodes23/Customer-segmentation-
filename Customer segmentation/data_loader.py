import pandas as pd
from sqlalchemy import create_engine

def load_sample_data(config):
    """
    Load sample data into the database
    """
    engine = create_engine(config['database_uri'])
    
    # Sample customer data
    customers_data = [
        (1, 'Male', 19, 15, 39),
        (2, 'Male', 21, 15, 81),
        (3, 'Female', 20, 16, 6),
        (4, 'Female', 23, 16, 77),
        (5, 'Female', 31, 17, 40)
    ]
    
    customers_df = pd.DataFrame(customers_data, 
                               columns=['customer_id', 'gender', 'age', 
                                        'annual_income_k', 'spending_score'])
    
    # Sample transaction data
    transactions_data = [
        (1, '2024-12-10', 150.75),
        (2, '2024-12-15', 320.50),
        (3, '2024-11-05', 45.20),
        (4, '2024-12-20', 275.00),
        (5, '2024-10-30', 125.35)
    ]
    
    transactions_df = pd.DataFrame(transactions_data,
                                  columns=['customer_id', 'transaction_date', 'amount'])
    
    # Load to database
    customers_df.to_sql('customers', engine, if_exists='append', index=False)
    transactions_df.to_sql('transactions', engine, if_exists='append', index=False)
    
    print("Sample data loaded successfully!")

if __name__ == "__main__":
    config = {
        'database_uri': 'mysql+pymysql://username:password@localhost/mall_customer_segmentation'
    }
    load_sample_data(config)