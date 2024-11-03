SELECT BuyingGroup, COUNT(*) AS CustomerCount
FROM dimension_customer
GROUP BY BuyingGroup;