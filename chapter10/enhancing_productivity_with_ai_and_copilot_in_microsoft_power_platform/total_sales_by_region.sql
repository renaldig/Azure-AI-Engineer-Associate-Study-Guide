-- Find the total sales by region
SELECT Region, SUM(SalesAmount) AS TotalSales
FROM SalesData
GROUP BY Region;
