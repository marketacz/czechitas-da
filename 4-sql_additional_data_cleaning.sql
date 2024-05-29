UPDATE "shops-select-reviews"
SET "city_output" = CASE
    WHEN "city_output" ILIKE 'brno%' THEN 'Brno'
    WHEN "city_output" ILIKE 'Staré Město' THEN 'Praha'
    WHEN "city_output" ILIKE 'Nové Město' THEN 'Praha'
    WHEN "city_output" ILIKE 'Nové Město' THEN 'Praha'
    WHEN "city_output" ILIKE 'II-Rokycany' THEN 'Rokycany'
    WHEN "city_output" ILIKE 'Plzeň%' THEN 'Plzeň'
    WHEN "city_output" ILIKE 'Pardubice V' THEN 'Pardubice'
    WHEN "city_output" ILIKE '%Ostrava%' THEN 'Ostrava'
    WHEN "address" = '12, Husova 231, Staré Město, 110 00, Czechia' THEN 'Praha'
    WHEN "address" = 'Novosedly nad Nežárkou 202, 37817, 378 17, Czechia' THEN 'Novosedly nad Nežárkou'
    WHEN "city_output" ILIKE '%-%' AND "city_output" NOT ILIKE 'Frýdek-Místek' AND "city_output" NOT ILIKE 'Sedlec-Prčice' THEN SPLIT_PART("city_output", '-', 1)
    ELSE "city_output"
END;

UPDATE "shops-select-reviews"
SET "address" = 'Hlavní 84, 739 11 Frýdlant nad Ostravicí, Frýdlant'
WHERE "title" = 'Lenčiny sladké dobroty'
;

UPDATE "shops-select-reviews"
SET "city_output" = 'Frýdlant nad Ostravicí'
WHERE "title" = 'Lenčiny sladké dobroty'
;

UPDATE "shops-select-reviews"
SET "city_output" = 'Sýkořice'
WHERE "address" = '255 Sýkořice-Zbečno, Czechia'
;

UPDATE "shops-select-reviews"
SET "city_output" = 'Plzeň'
WHERE "address" = 'D5 85.km, obchvat Plzně PS, č.p, 129, Czechia'
;

UPDATE "shops-select-reviews"
SET "city_output" = CASE
    WHEN "city_output" like '% I%' THEN SPLIT_PART("city_output", ' I', 1)
    ELSE "city_output"
END;
