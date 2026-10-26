USE library_db;

INSERT INTO AUTHOR (author_id, name, country, image) VALUES 
(1, 'Agatha Christie', 'United Kingdom', 'Agatha Christiett.jpg'),
(2, 'J.K. Rowling', 'United Kingdom', 'J.K. Rowling.jpg'),
(3, 'Dan Brown', 'United States', 'Stephen King.jpg');

INSERT INTO BOOK (book_id, title, price, author_id, image) VALUES 
(101, 'Murder on the Orient Express', 15.50, 1, 'Murder on the Orient Express.jpg'),
(102, 'And Then There Were None', 12.00, 1, 'And Then There Were None.jpg'),
(201, 'Harry Potter and the Sorcerer''s Stone', 20.00, 2, 'HP1.jpg'),
(202, 'Harry Potter and the Chamber of Secrets', 22.50, 2, 'Harry Potter and the Chamber of Secrets.jpg'),
(301, 'The Da Vinci Code', 18.00, 3, 'The Da Vinci Code.jpg'),
(302, 'Angels & Demons', 16.50, 3, 'Angels & Demons.jpg');