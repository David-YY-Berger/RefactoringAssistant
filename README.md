# Refactoring Assistant  


A Powerful Automated Refactoring Toolkit - Created for Ex Libris Automation   
   
<img src="https://github.com/David-YY-Berger/RefactoringAssistant/assets/91850832/ead92db1-8a62-416b-a94a-ae525a41f03b" width="50" height="50"> 

## Tools
### 1. Refactor Tests
- **Input:** A group of tests (by list of test names, directory path, excel file)
- **Output:** Sorted lists of ng and non ng tests
  - Ng tests - as a <ins>text file</ins> with testname, and ng phrase/s found
  - Non ng tests - as <ins>xml playlists</ins> for Automation Player, organized by Server
  - Automatically creates new ng test files and directories identical to source (optional)
     
### 2. Test List Compare
- **Input:** 2 groups of tests (by list of test names, directory path, excel or csv file)
- **Output:**  3 Lists of tests - tests found in both sources, only source 1, and only source 2
  - Optional: Tests organized by section (in original excel/csv/directory)
      
### 3. Discrepancy Tracker
- **Input:** A group of tests (by excel file)
- **Output:** (find ng/non ng tests acc to excel file's column 'result' (=passed/passed with no code change)
  - Outputs all tests marked as 'passed' with no discrepancies in a text file
  - Outputs all tests marked as 'passed with no code change' but contain discrepancies in another test file
  - Shows Discrepancies (old and new) between the tests, many text files organized by section
  - (Optional) Overwrites the new 'ng' test files with the content of the regular files, if 'passed without code change'  
<br />
<br />
<br />
  
## Capabilitites
- Maps relations btw test names, path, content, testng files, and servers
- Scans test files for key substrings, analyzes results (on large scale)
- Automatically refactors files and directories without build errors


## Ideas for Expansion
- Directory Organization: Consistency btw project structure and Test Rail Section
- Configuration Covering: Ensure that tests check all configurations
  - See list of tests (organized per section), and login institutions
  - Ensure that every section of test rail runs on each Server
  - Ensure Tests use 'Users' and not Exl Impl
 


