Note that this repository is forked by a template of academic website and modified to generate my personal website (yukun093.github.io).

Several matters still should be took action after you forked this repository. And once you have installed the corresponding prerequisites, the installation on a linux system or a virtual vmware workstation would be much smoothly.

# Install packages

Packages to create prerequisites:

```shell
ruby, bundler, nodejs, rbenv, jekyll
```

It can be completed when run the following commands:

```shell
sudo apt install ruby-dev ruby-bundler nodejs
sudo apt install rbenv
sudo apt install jekyll
```

It should be first install these packages, and then run the following corresponding commands. Before running the bundle, it needs to locate the correct absolute path.

```c++
bundle clean // to clean all the gem on the system
bundle clean --force // no need to use "--force", but if you're sure you want to remove every system gem not in this bundle, run `bundle clean --force`. "gem" seems like a file after running the "bundle install"
```

If it fails, it is suggested that first `sudo apt autoremove`. To remove the previous three packages, and first go into correct absolute path to check if the "ruby" is installed correct or not.

```ruby
ruby
print "hello world" // using "ctrl + D" to check the result, if the output is correct and then ruby is installed correctly.
```

If "bundle install" is refused, then running `bundle config set --local path 'vendor/bundle'`

# Run following commands to configure environment

Then to initialize "rbenv" to configure attributes.

```shell
eval "$(rbenv init -)"
rbenv init
rbenv rehash
bundle exec jekyll liveserve
```

If there is one suggestion about missing gem executables, then using following commands to fix it.

```shell
bundle clean
bundle install
bundle exec jekyll liveserve
```

# update personal website

First the new files should be commited to the github repository, then using following command:

```c++
rbenv rehash
bundle exec jekyll liveserve
localhost:4000 // one the browse, load website
```

Then refresh website again.