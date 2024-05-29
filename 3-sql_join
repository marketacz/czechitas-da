CREATE OR REPLACE TABLE "shops-select-reviews" AS
SELECT 
    r.*,
    s."totalScore",
    s."address",
    s."categoryName",
    s."website",
    s."reviews_0_text",
    s."reviews_1_text",
    s."reviews_2_text",
    s."reviews_3_text",
    s."reviews_4_text",
    s."reviews_5_text",
    s."reviews_6_text",
    s."reviews_7_text",
    s."reviews_8_text",
    s."reviews_9_text",
    s."reviews_10_text",
    s."reviews_11_text",
    s."reviews_12_text",
    s."reviews_13_text",
    s."reviews_14_text",
    s."reviews_15_text",
    s."reviews_16_text",
    s."reviews_17_text",
    s."reviews_18_text",
    s."reviews_19_text",
    s."location_lat",
    s."location_lng",
    s."openingHours_0_day",
    s."openingHours_0_hours",
    s."openingHours_1_day",
    s."openingHours_1_hours",
    s."openingHours_2_day",
    s."openingHours_2_hours",
    s."openingHours_3_day",
    s."openingHours_3_hours",
    s."openingHours_4_day",
    s."openingHours_4_hours",
    s."openingHours_5_day",
    s."openingHours_5_hours",
    s."openingHours_6_day",
    s."openingHours_6_hours"
FROM 
    "shops-reviews2" r
LEFT JOIN 
    "shops-select2" s
ON 
    r."url" = s."url";
