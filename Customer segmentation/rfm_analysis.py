import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

def calculate_rfm(config):
    """
    Calculate RFM metrics and scores
    """
    engine = create_engine(config['database_uri'])
    
    # Execute the RFM view creation if it doesn't exist
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE VIEW IF NOT EXISTS rfm_analysis AS
        SELECT 
            c.customer_id,
            c.gender,
            c.age,
            c.annual_income_k,
            c.spending_score,
            DATEDIFF('2025-01-01', MAX(t.transaction_date)) AS recency,
            COUNT(t.transaction_id) AS frequency,
            SUM(t.amount) AS monetary
        FROM
            customers c
        JOIN
            transactions t ON c.customer_id = t.customer_id
        GROUP BY
            c.customer_id, c.gender, c.age, c.annual_income_k, c.spending_score
        """))
        
    # Fetch the RFM data
    query = text("SELECT * FROM rfm_analysis")
    rfm_df = pd.read_sql(query, engine)
    
    # Calculate RFM scores (1-5 scale, 5 being best)
    # For recency, lower is better
    rfm_df['r_score'] = pd.qcut(rfm_df['recency'].rank(method='first'), 5, labels=[5, 4, 3, 2, 1])
    
    # For frequency and monetary, higher is better
    rfm_df['f_score'] = pd.qcut(rfm_df['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm_df['m_score'] = pd.qcut(rfm_df['monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    
    # Calculate combined RFM score
    rfm_df['rfm_score'] = rfm_df['r_score'].astype(int) + rfm_df['f_score'].astype(int) + rfm_df['m_score'].astype(int)
    
    # Create customer segments
    segment_labels = ['Low-Value', 'Mid-Value', 'High-Value', 'Top Customers']
    rfm_df['segment'] = pd.qcut(rfm_df['rfm_score'], 4, labels=segment_labels)
    
    return rfm_df

if __name__ == "__main__":
    config = {
        'database_uri': 'mysql+pymysql://username:password@localhost/mall_customer_segmentation'
    }
    rfm_results = calculate_rfm(config)
    print(f"Analysis complete. Found {len(rfm_results)} customers across {rfm_results['segment'].nunique()} segments.")
    
    # Optional: Save results to CSV
    # rfm_results.to_csv('output/rfm_analysis_results.csv', index=False)