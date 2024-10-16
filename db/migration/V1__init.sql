-- Create schemas for tenants
CREATE SCHEMA IF NOT EXISTS tenant1;
CREATE SCHEMA IF NOT EXISTS tenant2;

-- Create a sample table in tenant1 schema
CREATE TABLE tenant1.items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price INTEGER
);

-- Create the same table in tenant2 schema
CREATE TABLE tenant2.items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price INTEGER
);