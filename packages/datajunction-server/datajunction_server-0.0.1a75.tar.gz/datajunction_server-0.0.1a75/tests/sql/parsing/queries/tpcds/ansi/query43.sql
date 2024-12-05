-- start query 43 in stream 0 using template query43.tpl
SELECT s_store_name,
               s_store_id,
               Sum(CASE
                     WHEN ( d_day_name = 'Sunday' ) THEN ss_sales_price
                     ELSE NULL
                   END) sun_sales,
               Sum(CASE
                     WHEN ( d_day_name = 'Monday' ) THEN ss_sales_price
                     ELSE NULL
                   END) mon_sales,
               Sum(CASE
                     WHEN ( d_day_name = 'Tuesday' ) THEN ss_sales_price
                     ELSE NULL
                   END) tue_sales,
               Sum(CASE
                     WHEN ( d_day_name = 'Wednesday' ) THEN ss_sales_price
                     ELSE NULL
                   END) wed_sales,
               Sum(CASE
                     WHEN ( d_day_name = 'Thursday' ) THEN ss_sales_price
                     ELSE NULL
                   END) thu_sales,
               Sum(CASE
                     WHEN ( d_day_name = 'Friday' ) THEN ss_sales_price
                     ELSE NULL
                   END) fri_sales,
               Sum(CASE
                     WHEN ( d_day_name = 'Saturday' ) THEN ss_sales_price
                     ELSE NULL
                   END) sat_sales
FROM   date_dim,
       store_sales,
       store
WHERE  d_date_sk = ss_sold_date_sk
       AND s_store_sk = ss_store_sk
       AND s_gmt_offset = -5
       AND d_year = 2002
GROUP  BY s_store_name,
          s_store_id
ORDER  BY s_store_name,
          s_store_id,
          sun_sales,
          mon_sales,
          tue_sales,
          wed_sales,
          thu_sales,
          fri_sales,
          sat_sales
LIMIT 100;
