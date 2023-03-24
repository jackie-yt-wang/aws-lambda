-- SELECT * FROM superstore.orders;

select c.customerID,sum(Sales) from superstore.customers c
left join superstore.orders o on c.customerID = o.customerID
group by c.customerID
order by sum(Sales) desc
limit 10