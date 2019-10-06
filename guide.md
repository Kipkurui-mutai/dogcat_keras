# A small workshop

## Introduction

__Scenario__: Your deadline draws near and you just accidentally `rm` some codes in your project. You do keep a back-up, but it dated back one month ago, and you've changed a lot since. Is there anyway you can revert to a more recent version? Or, you work in a team project and your teammates and you just put on new codes without informing each other. How do you know where is your friends' new codes, and whether they conflict with your changes. Such situations are why we need a version control system. Among those, `git` is easily the most popular.

Now you have a glimpse of what it does. In simple words, `git`, or any other VCS, allows you to better track your project development, record changes, revert to bug-free version before, or work on different problems at the same time, or better plan what come next, etc.. `git` also makes your teamwork more efficiently by reducing code combining time, visualizing changes between different versions, etc..

Normally, `git`, as it is a distributed system, is paired up with some git repository hosting service, notably `GitHub`, which allows people working on the same project on different machines with a basic fast setup.

In this small workshop, we'll introduce the most important `git` commands, and demo a scenario where `git` helps you better coordinate your collectif efforts.


__Warning:__ This guide is for complete beginners who have bare knowledge about `git` and version control in general. If you're already accustomed to `git` or you've worked on some projects with it, you can ignore this workshop completely.

## Some prior knowledge

For basic `bash` commands, please consult [link](https://files.fosswire.com/2007/08/fwunixref.pdf). 

## Git installation

Please follow steps [here](https://www.linode.com/docs/development/version-control/how-to-install-git-on-linux-mac-and-windows/) to have  `git` in your machine. (Linux/Mac/Windows).

Next, let's go to [https://github.com](https://github.com) to create your personal account, I'll say, `your_name` for example. Once you finish, move to the next part.

## Step by step

Let's first create a new repository in your Github account:

* Go to https://github.com/your_name
* Click on plus sign, then choose "New repository".


<img src='images/newrepo.png' width='200'/>

* Enter "dogcat_keras" as your repository name.
* Leave other options blank as they are not necessary.

Now copy the URL link of your project: it should be something like: [https://github.com/your_name/dogcat_keras](https://github.com/your_name/dogcat_keras)

Next, let's download this small project to your machine. Though `GitHub` comes along with a graphical user interface that'll let you download by clicking some buttons, we'll do it the traditional `git` way with command lines:

```bash
git clone https://github.com/winlp4ever/dogcat_keras
```
You'll see a new folder named `dogcat_keras` is created. Go to that folder:

```bash
cd dogcat_keras/
```

Here you can see that the folder is not empty. It does contain all the files we'll work on already. 

Now (assume you're inside this folder), we'll replace the remote project link by yours. Type:

```bash
git remote rm origin
git remote add origin https://github.com/your_name/dogcat_keras
```

Then populate your remote project with the local files by typing:

```bash
git push origin master
```

You will be asked to enter your credentials for this action, as GitHub wants to be sure if you're granted rights to do so. 

Once done, you can refresh your project page on Github, it should now show differently as you're able to see your newly uploaded local files.

Now let's make some small changes first to see how `git` works:

Go to `download_utils.py`, modify the line 

```python
if pretrained_checkpoint is not None:
```

by deleting the words `is not None` as they are redundant. Also, in `__init__(...)` function, track the line `Dropout` and change the ratio inside from `0.25` to `0.5`. Now let's type: 

```bash
git status # see if there're files untracked, files updated
```

You would probably see the following:

<img src='images/gitstatus.png' width='600'/>

If you add a new file, namely `test.py` for example, the above command will print out:

<img src='images/gitstatus_.png' width='600'>

, which indicates `test.py` is untracked. To track untracked files or record updates (sometimes both), type:

```bash
git add . # . stands for every changes, change to specified files for better versioning
git commit -m 'your commit message here'
```

Now re-type `git status`, `git`'ll annouce you everything fine, `nothing to commit, working tree clean`.

So `git status` to check for new changes, and `git add .` and `git commit -m 'message'` to commit changes.

### One step back, two steps forward

Now understanding how `git` records changes, you may quite frequently want to visit your old codes. After all, that's the reason why we're doing backups all the time, right? In `git`, that can be easily done with `git log`:

Type `git log` and Enter, you'll see:

<img src='images/gitlog.png' width='500'>

Now you see that every time you commit some changes appears here, with some unique hashcode for each commit. If your commit messages are well written enough,you won't have troubles narrow down where exactly you want to review. But now, how to do that? Though the hashcode seems long, actually you only need its first 5 digits, type, for example:

```bash
git checkout 133ddb
```

All your files will revert back to the old version you want. Don't worry, you can return to the modern day as soon with

```bash
git checkout master
```

So fast, right? But what if you really want to undo some changes you've made, which means return to a specific moment and completely erase the history after that. If you want so, `reset` is for you. Type:

```bash
git reset 133ddb
```

Now if you re-type `git log`, you won't see all the change commits behind the commit you revert back to, everything comes after is erased! So consider this option carefully.

### Git branching

Now `git` is a version control system, so `branching` is inevitable, as it's in fact the core idea behind the whole `versioning`. A branch is a version/state of your project. Along a project's development, different branches may share some initial state, then diverge from a moment, and finally re-merge to become one at some future moment. Such a _multiverse_ structure allows people to work on different directions, problems in parallel, at the meantime not too far from the base. 

<img src='images/gitbranch.png' width='600'>

Type `git branch` to get list of all existing branches. The `master` branch is the principal public branch that should be the project final end. You can switch to a branch with `git checkout <branch-name>`. As there is no other branch except `master` in our project, let's create a new one:

```bash
git checkout -b dev
```

Now type `git branch`, you'll see:

<img src='images/brs.png' width='200' />

So we've switched to the new branch called `dev`. 

(To delete a branch, use `git branch -d <remote name-optional> <branch-name>`)

Test the dowloading with command `python download_utils.py`. As we see here,

<img src='images/down_no_log.png' width='400'/>

, nothing allows us to guess what's happening with the download. For big files, this is uncomfortable.  

So we want to log information about the download process. Let's make some changes in the function `down_fr_url(...)` in `download_utils.py`:

We'll write two new local functions in the scope of `down_fr_url(...)` right at the beginning.

```python
    def indicator(quantity, width=10):
            if quantity > 1024:
                return '{:.0f} MB/s'.format(quantity / 1024).rjust(width)
            return '{:.0f} KB/s'.format(quantity).rjust(width)

    def progress(count, block_size, total_size):
        global start_time
        if count == 0:
            start_time = time.time()
        if count % 100 == 99 or (count + 1) * block_size >= total_size:
            percent = (count * block_size) / total_size
            down_size_in_mb = count * block_size // BYTES_PER_MB
            total_size_in_mb = total_size // BYTES_PER_MB
            pos = int(ceil(percent * 20))
            down_bar = '[' + '=' * max(pos - 1, 0) + '>' + (20 - pos) * '-' + ']'
            if (count + 1) * block_size >= total_size:
                down_bar = '[' + '=' * 20 +']'
                down_size_in_mb = total_size_in_mb

            speed = (count * block_size) / (time.time() - start_time + 1e-3) / 1024
            time_left = int((total_size_in_mb - down_size_in_mb) * 1024 / (speed + 1e-3))
            print('{} {}/{} MB {} {}\testim. time left: {}'.format(down_bar,
                    str(down_size_in_mb).rjust(len(str(total_size_in_mb))),
                    total_size_in_mb, ('(%2.1f%%)'%(percent * 100)).rjust(8),
                    indicator(speed), time_left),
                flush=True, end='\r')
```

Also, add an argument `reporthook=progress` to the `urlretrieve(...)` call inside the `down_fr_url` scope so that we're able to use these trackers when downloading. Let's retry the downloading process:

```bash
python download_utils.py
```

<img src='images/down_log.png' width='800'/>

It does look much better, right?

### Push updates

When a change is committed locally, if that change is important enough, we think about pushing it to the remote repository. You do it with command:

```bash
git push origin dev #or master, depends on which remote branch you want to push to
```
### Conflicts and resolve

Imagine this situation, one of our teammates also sees another unexpected behavior of `down_fr_url(...)`, that is, even if the file already exists, typing the command above will re-force the entire download. Therefore, he, working on `master` branch, decides to add a small piece of code to the function:

```python
if os.path.exists(save_path) and os.path.getsize(save_path)>=retri_file_size   (url):
    print('{} already exists.'.format(save_path))
    continue
```

After done with his works, he proudly push it to the master branch. And we, after feeling satisfied with our changes in branch `dev`, decide that would be a moment to merge it to the `master` branch. Conflicts occur, as we and him both made changes in the same file. 

If you want to merge locally: you have to re-switch to `master` branch:

```bash
git checkout master
git merge dev
```

If ever there is conflicts, you have to go to the conflicted files, and choose for each conflicted part, which branch to apply changes from.

If you want to do such a pull request on `GitHub`, which is the main way how people contribute to a project, click `create pull request`, you will have chance to compare between the current master version with yours _dev_ version, 

<img src='images/pullrequest.png' width='800' />

Then `git` will re-examine the both codes, if there's any conflict, they'll invite you to resolve it (choose which part which branch), otherwise, you'll see:

<img src='images/goodtogo.png' width='800' />

## Some remarks

`git` is a pretty easy, must-use tool to learn. As usual, the best way to learn it is through practices, so you should get along with it in your projects from onwards.

This `git` commands [cheatsheet](https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf) is recommended.