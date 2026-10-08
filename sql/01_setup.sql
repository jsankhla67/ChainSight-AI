-- Agar database pehle se bana hua hai to pehle usko hata do

DROP DATABASE IF EXISTS ecommerce_supply_chain;

-- Ab fresh database create kar rahe hain

CREATE DATABASE ecommerce_supply_chain
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Ab isi database par kaam karenge

USE ecommerce_supply_chain;

-- Saare available databases checking 

SHOW DATABASES;

-- Check kar rahe hain ki abhi kaunsa database selected hai

SELECT DATABASE() AS current_database;

-- MySQL ka version check kar rahe hain

SELECT VERSION() AS mysql_version;
