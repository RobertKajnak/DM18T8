# DM18T8

Data Mining 2018 for team 8

#Git tutorial

[config git]  
git config --global user.email "[username]"  
[if you want password remembered]  
git config credential.helper store  
[change default editor -- useful when commiting with message body, not just title]  
to use notepad: git config --global core.editor notepad  
to use notepad++  
(x86): git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"  
(x64): git config --global core.editor "'C:/Program Files (x86)/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"  
obviously use the actual path, if it is different and other editors can be used as well

git init  
git pull https://github.com/RobertKajnak/IloveCI_2017_T90.git   
git add [filename] ( . adds all files, ignoring only some python specific chached files etc)   
[quick and dirty]  git commit -m "[description of the changes]"  
[with editor]  git commit  [use two newlines to separate commit title and body]  
git push https://github.com/RobertKajnak/IloveCI_2017_T90 master  

git diff --chached --name-status  [check added files (e.g. after git add . (A=added,M=modified,D=deleted)]
git diff --chached  {check differences as well}
git reset [undo add files]
