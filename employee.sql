CREATE TABLE employee (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    experience INT NOT NULL,
    annual_salary NUMERIC(10, 2),
    bonus NUMERIC(10, 2),
    tax NUMERIC(10, 2),
    net_salary NUMERIC(10, 2)
);

INSERT INTO employee (
    id,
    name,
    salary,
    experience,
    annual_salary,
    bonus,
    tax,
    net_salary
)
VALUES
(1, 'Sam', 30000, 2, 360000, 0, 0, 360000),
(2, 'John', 40000, 3, 480000, 4000, 2000, 482000),
(3, 'David', 50000, 5, 600000, 5000, 2500, 602500),
(4, 'Priya', 35000, 4, 420000, 3500, 1750, 421750),
(5, 'Rahul', 45000, 1, 540000, 0, 0, 540000);

select * from employee

