USE company;

SET FOREIGN_KEY_CHECKS = 0;

INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES 
(1, 'Research', '123456789', '2022-01-15'),
(2, 'Administration', '987654321', '2021-06-01'),
(3, 'Development', '456789123', '2023-03-10');

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES 
('123456789', 'Alice', 'Smith', '1985-04-12', '123 El-Geish St, Alexandria', 'F', 85000.00, 1),
('987654321', 'Bob', 'Johnson', '1979-11-23', '45 Sidi Gaber, Alexandria', 'M', 95000.00, 2),
('456789123', 'Charlie', 'Brown', '1990-07-30', '78 Smouha, Alexandria', 'M', 72000.00, 3);

INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES 
(101, 'AI Document Processing', 'Alexandria', 1),
(102, 'Database Migration', 'Cairo', 2),
(103, 'Cloud Infrastructure', 'Alexandria', 3);

SET FOREIGN_KEY_CHECKS = 1;