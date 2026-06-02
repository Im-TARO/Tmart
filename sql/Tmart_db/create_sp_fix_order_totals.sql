DELIMITER $$

-- Drop the procedure if it exists
DROP PROCEDURE IF EXISTS fix_order_totals $$

-- Create the procedure
CREATE PROCEDURE fix_order_totals()
comment 'Procedure to fix the order total_amount and delivery_cost when items are canceled: CALL fix_order_totals();'
BEGIN
    UPDATE orders o
    JOIN (
        -- CTE: identify all orders that contain at least one canceled item,
        -- and capture whether the customer is a loyalty member    
    with canceled as (select distinct i.order_id, c.loyalty_member from order_items i join orders o on i.order_id = o.order_id join customers c on o.customer_id = c.customer_id where i.item_status = 'Canceled')
			-- For each order that has a cancellation, sum only the non-canceled line totals    
        SELECT
            o.order_id, c.loyalty_member,
            SUM(CASE
                WHEN o.item_status != 'Canceled' THEN line_total
                ELSE 0 -- exclude canceled items from the total
            END) AS new_total
        FROM order_items o  join canceled c on o.order_id = c.order_id -- limit to orders with at least one cancellation
        GROUP BY order_id, loyalty_member
    ) t ON o.order_id = t.order_id
    SET
			-- Round the recalculated total to 2 decimal places
        o.total_amount = ROUND(t.new_total, 2),
        -- Recalculate delivery cost based on the new total and loyalty membership status
        o.delivery_cost =
       CASE
				-- If the entire order is canceled (total = 0), no delivery charge
           WHEN t.new_total = 0 THEN 0  
				-- Loyalty member delivery tiers
           WHEN t.loyalty_member THEN CASE
                                          WHEN t.new_total >= 50 THEN 0
                                          WHEN t.new_total >= 25 THEN 5
                                          ELSE 10
                                      END
				-- Standard (non-loyalty) delivery tiers                                      
           ELSE CASE
                    WHEN t.new_total >= 75 THEN 0
                    WHEN t.new_total >= 50 THEN 5
                    WHEN t.new_total >= 25 THEN 10
                    ELSE 25
                END
       END;

END $$

DELIMITER ;