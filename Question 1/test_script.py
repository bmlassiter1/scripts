from github import Github
from datetime import datetime
import collections
from collections import OrderedDict
import pylab as py
import pylab as py1
import numpy 

git = Github()
repo = git.get_repo('JuanitoFatas/fast-ruby')

#Repository name
print "Repository name: " + repo.name + "\n"

#Date of first/most recent commit
latest = []
first = []

branches = repo.get_branches()

for branch in branches:
    commits = repo.get_commits(sha=branch.name)
    latest.append(commits[0].commit.committer.date)
    first.append(commits[len(list(commits)) - 1].commit.committer.date)

print "Latest commit: " + str(max(latest))
print "First commit: " + str(min(first)) + "\n"

#List the branches
recents = []
max_branch_count = 0

print "Branches: "
for branch in branches:
    print branch.name
    commits = repo.get_commits(sha=branch.name)
    first = (branch.name, commits[0].commit.committer.date, commits[0].stats.additions, commits[0].stats.deletions)
    recents.append(first)
    if len(list(commits)) > max_branch_count:
        count = len(list(commits))
        max_branch = branch.name

#How many issues against repo
issues_closed = repo.get_issues(state='closed')
issues_open = repo.get_issues(state='open')
issues_all = repo.get_issues(state='all')

print "\nIssues: "
print "Closed issues: " + str(len(list(issues_closed)))
print "Open issues: " + str(len(list(issues_open)))
print "All issues: " + str(len(list(issues_all)))

#Opened/closed the most issues
names = []
names_closed = []  

for issue in issues_closed:
    if issue.closed_by <> None:
        names.append(issue.closed_by.name)
        if issue.user <> None:
            names_closed.append(issue.user.name)
                
for issue in issues_open:
    if issue.user <> None:
        names_closed.append(issue.user.name)
        
count = collections.Counter(names_closed).most_common(1)
tup = count[0]
print "\nMost Opened Issues: " + str(tup[0])

count = collections.Counter(names).most_common(1)
tup = count[0]
print "Most Closed Issues: " + str(tup[0])

#Open pull requests
i = 1
print "\nAll open pull requests: "
pulls = repo.get_pulls(state='open')
if len(list(pulls)) == 0:
    print "No open pull requests"
else:
    for pull in pulls:
        print str(i) + ". " + str(pull.title)
        i = i + 1

#Top 5 Contributors
print "\nTop 5 Contributors: "
contrib =  repo.get_contributors()
count = len(list(contrib))
i = 0
upper = 5
if count < 5:
    upper = count
while i < upper:
    number = i + 1
    print str(number) + ". " + contrib[i].name
    i = i + 1

#Diff on master branch
master = repo.get_commits(sha='master')

print "\nMost recent commit in Master branch: "
master_date = master[0].commit.committer.date
print "Date: " + str(master_date)
print "Diff from today: " + str(datetime.now() - master_date)
print "Additions: " + str(master[0].stats.additions)
print "Deletions: " + str(master[0].stats.deletions)

#Diff on non-master branch    
most_recent = max(recents, key=lambda x:x[1])
print "\nMost recent commit other than the Master branch:"
if most_recent[0] == 'master':
    print "The most recent commit is in the Master branch"
else:
    print "Branch: " + most_recent[0]
    print "Date: " + str(most_recent[1])
    print "Diff from today: " + str(datetime.now() - most_recent[1])
    print "Additions: " + str(most_recent[2])
    print "Deletions: " + str(most_recent[3])

#Histograms
histogram_dates = []
months = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0}
days = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
for commit in repo.get_commits(sha=max_branch):
    histogram_dates.append(commit.commit.committer.date)
    month = commit.commit.committer.date.month
    day = commit.commit.committer.date.weekday()
    months[str(month)] = months[str(month)] + 1
    days[str(day + 1)] = days[str(day + 1)] + 1

months = OrderedDict(sorted(months.items(), key=lambda x:int(x[0])))
days = OrderedDict(sorted(days.items(), key=lambda x:int(x[0])))

X = numpy.arange(len(months))
py.bar(X, months.values(), align='center')
py.xticks(X, months.keys())
xmax = max(months.values()) + 1
py.ylim(0, xmax)
py.xlabel('Month by number (January-December)')
py.ylabel('Commit Frequency')
py.title('Commits by Month of the Year for ' + max_branch + ' Branch')
py.ion()
py.show()

#Y = numpy.arange(len(days))
#py1.bar(Y, days.values(), align='center')
#py1.xticks(Y, days.keys())
#ymax = max(days.values()) + 1
#py1.ylim(0, ymax)
#py1.xlabel('Day by number (Sunday-Saturday)')
#py1.ylabel('Commit Frequency')
#py1.title('Commits by Day of the Week for ' + max_branch + ' Branch')
#py1.show()