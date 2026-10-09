Drop Table Employee;

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
    ('Arun', 30000, 4, 360000, 3000, 1500, 361500),
    ('Priya', 25000, 2, 300000, 0, 0, 300000),
    ('Karthik', 40000, 6, 480000, 4000, 2000, 482000),
    ('Divya', 35000, 3, 420000, 3500, 1750, 421750),
    ('Rahul', 20000, 1, 240000, 0, 0, 240000);

select * from employee;




