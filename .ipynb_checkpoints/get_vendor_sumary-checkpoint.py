import pandas as pd
import sqlite3
import logging

from ingestion_db import ingest_db


logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

def create_vendor_sumary(connection):

    '''This function will merge the different tables to get the overall vendar summary and adding new columns in the resulting data'''
    vendor_sales_sumary = pd.read_sql_query('''
WITH FreightSummary AS (
    SELECT 
        VendorNumber, 
        SUM(Freight) AS FreightCost
    FROM vendor_invoice
    GROUP BY VendorNumber
),
PurchaseSummary AS (
    SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description, -- Added this so the final SELECT can find it
        p.PurchasePrice,
        pp.Volume,
        pp.Price AS ActualPrice,
        SUM(p.Quantity) AS TotalPurchaseQuantity,
        SUM(p.Dollars) AS TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Volume,
        pp.Price
),    
SalesSummary AS (
    SELECT
        VendorNo,
        Brand,
        SUM(SalesDollars) AS TotalSalesDollars,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sales
    GROUP BY
        VendorNo,
        Brand
)   
SELECT
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC
''', connection)
    return vendor_sales_sumary


def clean_data(df):
    df['Volume'] = df['Volume'].astype('float64')

    df.fillna(0, inplace=True)

    df['VendorName'] = df['VendorName'].str.strip() 
    df['Description'] = df['Description'].str.strip()

    # replace df with vendor_sales_sumary if not worked

    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']

    return df

if __name__ == '__main__':
    # Creating db connection
    connection = sqlite3.connect('inventory.db')

    logging.info('Creating Vendor Sumary Table...........')
    sumary_df = create_vendor_sumary(connection)
    logging.info(sumary_df.head())

    logging.info('Cleaning data .....')
    clean_df = clean_data(sumary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting data .....')
    ingest_db(clean_df, 'vendor_sales_sumary', connection)
    logging.info(' Completed.....')