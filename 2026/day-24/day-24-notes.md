## git merge
# What is a fast forward merge?
A git merge that occurs ina direct,linear path and; leaves no merge commit and it's automatic when a linear path is available.

# When does Git create merge commit?
WHen git needs to combine two different histories commit histories.

# What is a merge conflict? 
When users on different branch try to change the same file, conflict occurs.

## git rebase
# What does git rebase actually do to your commits?
It creates a linear commit history.

# How is the history different from a merge?
It doesn't show where a new branch is merged.

# Why should you never rebase commits that have been pushed and shared with others?
Because it will change commit history and without branching others will not be able to locate the branch which have been changed and their local version of history doesn't matches the server's version.

# When would you rebase vs merge?
Use rebase to sync your private branch with main and clean up pending commits.
Use merge to sync your shared branch with main and after finishing a feature to move it to main.

## git squash
# What does squash merging do?
It combines all commits into one and puts it in staging area to be committed.

# When would you use squash merge vs regular merge?
When you have many small query or appending commits , use squash merge.
Use regular merge when your commit contains important and distinct architectural steps.

# What is the trade-off of squashing?
Clutter::	Very Low as there is only commit per feature)	
Debugging::	Harder as all the Changes are bundled.

## git stash 
# What is the difference between "git stash pop" and "git stash apply"?
While using git stash pop it removes your work from stash, and deletes the stash entry immediately.
While in the case of git stash apply, it gives copy of a file meaning keeping the original in stash list.

# When would you stash in a real-world workflow?
Only when my file/work isn't ready to be committed.

## cherry Picking
# What does cherry-pick do?
It can pick a single commit to merge instead of merging whole commmit history. 

# When would you cherry-pick in a reak project?
If only some commits are good to be merged into main.

# What can go wrong with cheer-picking?
If you merge two branches, same commit can appear two times.

