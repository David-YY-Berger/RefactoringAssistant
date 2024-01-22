# Refactoring Assistant

A Powerful Automated Refactoring Toolkit - Created by Ex Libris Automation

## Tools
### Refactor Tests
- **Input:** A group of tests (by list of test names, directory path, excel file)
- **Output:** Sorted lists of ng and non ng tests
  - Ng tests - as a <ins>text file</ins> with testname, and ng phrase/s found
  - Non ng tests - as <ins>xml playlists</ins> for Automation Player, organized by Server
  - Automatically creates new ng test files and directories identical to source (optional)
     
### Test List Compare
- **Input:** 2 groups of tests (by list of test names, directory path, excel or csv file)
- **Output:**  3 Lists of tests - tests found in both sources, only source 1, and only source 2
      
### Discrepancy Tracker
- **Input:** A group of tests (by list of test names, directory path, excel file)
- **Output:** Discrepancies between regular and new ng files copies of the tests (if they exist)
  - In <ins>text file</ins>, organized by old and new discrepancies  
<br />
<br />
<br />
## Capabilitites
- Maps relations btw test names, path, testng files, and servers
- Scans test files for key substrings, organizes accordingly
- Automatically creates refactored files and directories without build errors


## Ideas for Expansion
- Directory Organization: Consistency btw project structure and Test Rail Section
- Configuration Covering: Ensure that tests check all configurations
  - See list of tests (organized per section), and login institutions
  - Ensure that every section of test rail runs on each Server
  - Ensure Tests use 'Users' and not Exl Impl
 


