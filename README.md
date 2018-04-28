 DM18T8

Data Mining 2018 for team 8

# Git tutorial

## Configure Git Bash  
### Authentication
**git config --global user.email** "\[username\]"  *why type it in every time?*  
**git config credential.helper store** *if you want password remembered:*  

### Editor for commits  
#### to use notepad:   
**git config --global core.editor** notepad  *change default editor -- useful when commiting with message body, not just title:*   
#### to use notepad++:  
*(x86):* **git config --global core.editor** "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"    
*(x64):* **git config --global core.editor** "'C:/Program Files (x86)/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"  
*obviously use the actual path, if it is different and other editors can be used as well*  

## Basic commands 
**git init** *Initializes current folder to be ready for gir repo related commands, such as pull*  
**git pull** https://github.com/RobertKajnak/DM18T8.git  
**git add** \[filename\] *( **git add .** adds all files, ignoring only some python specific chached files etc)*   
**git commit -m** "\[description of the changes\]"  *quick and dirty -- if you only need a couple of words to desribe the change*  
**git commit**  *Launches editor (preferably notepad++, the other can be a pain. Use two newlines to separate commit title and body*  
**git push** https://github.com/RobertKajnak/DM18T8.git **master**  

## Other useful commands  
**git diff --cached --name-status** \[check added files (e.g. after git add . (A=added,M=modified,D=deleted)\]  
**git diff --cached**  *check differences as well*  
**git reset** *undo add files*  
