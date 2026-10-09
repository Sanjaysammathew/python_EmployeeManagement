DROP TABLE IF EXISTS employee;

CREATE TABLE employee (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary NUMERIC NOT NULL,
    experience INT NOT NULL,
    annual_salary NUMERIC,
    bonus NUMERIC,
    tax NUMERIC,
    net_salary NUMERIC
);

INSERT INTO employee (
    name,
    salary,
    experience,
    annual_salary,
    bonus,
    tax,
    net_salary
)
VALUES
    ('Arun',     30000, 4, 360000, 3000, 1500, 361500),
    ('Priya',    25000, 2, 300000,    0,    0, 300000),
    ('Karthik',  40000, 6, 480000, 4000, 2000, 482000),
    ('Divya',    35000, 3, 420000, 3500, 1750, 421750),
    ('Rahul',    20000, 1, 240000,    0,    0, 240000),
    ('Sneha',    45000, 5, 540000, 4500, 2250, 542250),
    ('Vijay',    28000, 2, 336000,    0,    0, 336000),
    ('Anitha',   32000, 4, 384000, 3200, 1600, 385600),
    ('Suresh',   50000, 8, 600000, 5000, 2500, 602500),
    ('Meena',    22000, 1, 264000,    0,    0, 264000),
    ('Prakash',  38000, 3, 456000, 3800, 1900, 457900),
    ('Kavya',    27000, 0, 324000,    0,    0, 324000),
    ('Ramesh',   42000, 7, 504000, 4200, 2100, 506100),
    ('Lakshmi',  33000, 2, 396000,    0,    0, 396000),
    ('Manoj',    26000, 1, 312000,    0,    0, 312000),
    ('Pooja',    48000, 5, 576000, 4800, 2400, 578400),
    ('Ganesh',   36000, 4, 432000, 3600, 1800, 433800),
    ('Nithya',   24000, 2, 288000,    0,    0, 288000),
    ('Deepak',   55000, 9, 660000, 5500, 2750, 662750),
    ('Swathi',   31000, 3, 372000, 3100, 1550, 373550);

-- Display all employees
SELECT * FROM employee ORDER BY id;

