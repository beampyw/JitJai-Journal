<<<<<<< HEAD
# JitJai-Journal
=======
# JitJai-Journal

# requirements.txt
pip install streamlit

"streamlit run main.py"


CREATE TABLE account ( id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, name VARCHAR(100), lastname VARCHAR(100) );
CREATE TABLE Diary ( id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255) NOT NULL, heading VARCHAR(255) NOT NULL, diarytext LONGTEXT, FOREIGN KEY (email) REFERENCES account(email) ON DELETE CASCADE );
>>>>>>> 3eb36b6 (อัปเดตโค้ด)
