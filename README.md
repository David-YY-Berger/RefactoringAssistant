# Refactoring Assistant  


A Powerful Automated Refactoring Toolkit - Created for Ex Libris Automation   
   
<img src="https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/ead92db1-8a62-416b-a94a-ae525a41f03b" width="50" height="50"> 
     
**Short Summary:** Utulizing knowledge of Compilers, Operating Systems, and Databases, this toolkit enables my team to refactor thousands of test files easily and responsibly. The selenium based tests must be adapted to the product's new Frontend (Angular - 'ng'), we must create and maintain old test files to check the old product, and new 'ng' test files to check the new frontend. This Readme describes some parts of the toolkit.
<br />
    
<ins>Screenshots below </ins>
   
   ![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/38ac64fd-c429-4f5f-a73a-6fae34ee9a36)
  
        
## Tools
### 1. Refactor Tests
- **Input:** A group of tests (by list of test names, directory path, excel file or csv file)
- **Output:** Sorted lists of ng and non ng tests
  - Ng tests - as a <ins>text file</ins> with testname, testng, server and ng phrase/s found
  - Non ng tests - as <ins>xml playlists</ins> for Automation Player, organized by Server
  - Automatically creates new ng test files and directories parallel to the src (optional) at new path with new class names
     
### 2. Test List Compare
- **Input:** 2 groups of tests (by list of test names, directory path, excel or csv file)
- **Output:**  3 Lists of tests - tests found in both sources, only source 1, and only source 2. Organized by section found in directory/Excel/CSV
      
### 3. Discrepancy Tracker
- **Input:** A group of tests (by excel file)
- **Output:** For all tests marked as 'passed', saves each discrepancy between the ng and non ng test file (every month)
  - Outputs (.txt) new discrepancies discovered in test files, organized by section, and by function in test file
  - Outputs (.txt) all tests with path or name inconsistent with our coding scheme
<br />
<br />
<br />
  
## Capabilitites
- Maps relations btw test names, path, content, testng files, and servers
- Scans test files for key substrings, analyzes results (on large scale)
- Automatically refactors files and directories without build errors
- Saves history efficiently, compares current verions, parses Java files by function


## Ideas for Expansion
- Directory Organization: Consistency btw project structure and Test Rail Section
- Configuration Covering: Ensure that tests check all configurations
  - See list of tests (organized per section), and login institutions
  - Ensure that every section of test rail runs on each Server
  - Ensure Tests use 'Users' and not Exl Impl
 

## Screenshots
   
The app:  
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/f4776a76-2ea7-41e2-b281-059a5f4c0263)
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/e2052b61-1557-4ee6-ad2d-53d1553cb18a)
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/d1e65480-5a52-4092-aa63-ca76fb6d0707)
    
### Output Files - Refactor Tests:
    
Finding phrases that must be refactored (txt):       
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/b443863c-2144-41d9-aba9-7e9fa853ca63)
   
Discovering incorrect file paths for ng files (txt):
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/e6abcb66-60e4-4795-812a-fd1038439f89)
    
Playlist to Run Tests Automatically acc to server (xml):
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/f05e0b13-4745-455f-9336-82c1c187ead4)

   
### List Compare:

![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/40ae6c47-a1d8-4c11-ae4d-8ba194e16a3a)
    
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/8a3d9c73-d317-4d94-b0c4-f41a947206a0)
   
    
### Output Files - Discrepancy Tracker:
File containing discrepancies (csv):
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/3a556358-b94b-4cfb-acd5-b30c8edfae1c)
   
Discrepancies printed by section:
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/826b45a5-6b54-4fc2-b4cf-ee0991ca8862)
   
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/badf4c41-75dd-43f7-a31f-90e1d07844bb)

### Metric Collection:
    
![image](https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/994c7a6d-11d6-496a-ae28-cfdde8363d66)
   





 


