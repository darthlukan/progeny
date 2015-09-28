# Progeny

[![Build Status](https://travis-ci.org/darthlukan/progeny.svg)](https://travis-ci.org/darthlukan/progeny)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/darthlukan/progeny?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

> Author: Brian Tomlinson <darthlukan@gmail.com>


## Description

> A project generation tool inspired by tools like [Yeoman](http://yeoman.io/) written in Python.


## Why?

> I became unhappy with the current state of project generation tools.  There are a plethora of them in the JavaScript
> ecosystem, but they tend to have a few problems:

* They are slow (more on this later)
* They require a lot of dependencies
* They try to do too many things at once, bordering on practically replacing your package manager (Stop auto-installing
  things that I don't want on my system and don't need in my project!)
* Their templates are a pain to write and require a language not already present in most UNIX-like distributions
* They are very specific to "web projects"
* They require the user to further interact with them during execution


## How does Progeny solve those problems?

> Progeny does not aim to do anything more than get you from "idea to code" in as few steps as possible. Here's how:

* Progeny is faster than Yeoman. Yeoman is a great tool, but it's very slow, partially because it tries to do so much
  and partially due to the fact that it's yet another node-based tool. Python isn't the fastest programming language,
  but executing Progeny with a footprint arg is much faster than executing Yeoman with a basic static site template.

* Progeny requires only what is contained in the Python Standard Library, no external dependencies to install!
* Progeny only does one thing: Generate a directory and file hierarchy. Dependencies for the desired project are up to
  the user to install using the best tool for the job: their system's package manager.
* Progeny uses "footprints" to define a project type's directory and file hierarchy. These are plain-text files that
  contain the project layout.  An example of a simple footprint for a Python CLI project is:

```
  
    __init__.py
    main.py
    README.md
    LICENSE
```

* Because the definition of a project is entirely up to the footprint and because Progeny is just creating file and
  directory hierarchies, Progeny is not language, framework, or type dependent.  Want to start a C project? Load up the
  appropriate footprint (or write one), pass it to Progeny and you're ready to go. In reality, it's not even limited to
  "software projects". Maybe your working language is "english" and your type is "book", there's nothing stopping you
  from supplying such a footprint and then generating the project with Progeny.
* Progeny is designed to require no more interaction from the user after it's been executed. No asking the user during
  execution if they want to add a plugin, or install yet another dependency, or worse: finishing execution but returning
  them to some arbitrary menu just so they can manually exit the program before doing what it is they want to do, which
  is implement their idea.


## Footprints

> Progeny uses footprint files to create projects. Currently, it looks for these files in a small handful of places
> (Where it looks for files could change before v1.0! You've been warned.):

* Via command line argument
* In a directory specified by the user via their config file
* $HOME/.config/progeny/footprints
* /usr/share/progeny/footprints

> As mentioned in the previous section, footprints are just simple text files.  Here are some examples of footprints
> that will work with Progeny:

* Simple Python CLI:


```

    __init__.py
    main.py
    README.md
    LICENSE
```

* A Flask app:

```

    __init__.py
    app.py
    README.md
    LICENSE
    html/
    html/index.html
    js/
    js/main.js
    css/
    css/main.css
```

* A Go web project:


```

    main.go
    routers.go
    models.go
    templates/
    templates/base.html
    templates/index.html
    js/
    js/main.js
    styles/
    styles/main.css
    README.md
    LICENSE
```

> Here are some important notes on writing footprints:

* Filenames should not have spaces, use 'dashes' or 'underscores' instead
* Directories should be listed before any files or subdirectories that rely on them. e.g: js/ before js/main.js
* Directories need to have a trailing slash '/' or Progeny won't know that they are directories (this may change later)


## Usage

> Okay, so you've read all of the above and now you want to actually use this amazing tool. Great! Let's create a simple
> Python CLI project! assuming you have Progeny installed in $HOME/projects/progeny and you only want to supply a
> footprint and a name (because you don't know which license you want to use yet):

```
    $ progeny -f $HOME/projects/progeny/python/cli -n my_app -p ~/projects
```

> In the above example, I'm assuming you don't have a progenyrc file defined in $HOME/.progenyrc or
> $HOME/.config/progeny/progenyrc, so I've supplied the 'parent' argument (-p). This tells Progeny in which parent it
> should place the project.  You should now be able to change to "~/projects/my_app" and have a few files in there.
> Progeny has auto-generated a README.md with some very basic info.  If we were to provide Progeny with a bit more info,
> we could get a pre-populated LICENSE file as well:

```
    $ progeny -f $HOME/projects/progeny/python/cli -n my_app2 -p ~/projects -l gpl2
```

> Now you can "cd" into ~/projects/my_app2 and see that the README.md includes license information, and the LICENSE file
> has been populated with the text of the GPL2.

> At a minimum, Progeny requires a footprint, name, and parent directory in order to successfully execute.  If a
> footprint is omitted, then a language and type are also needed. For example:

```
    $ progeny -n my_app3 -lang python -t cli -p ~/projects
```

> The above command will define a project named "my_app3", search for a cli footprint in the python directory under one
> of the available footprint paths and place all of this under the ~/projects directory.

> For even simpler usage, please see the [progenyrc](https://github.com/darthlukan/progeny/blob/master/progenyrc) file which contains some options that can be set as defaults for
> Progeny. As of today (27-09-2015) Progeny's "defaulting" functionality is not yet fully implemented, you may
> experience a few error messages if you fail to provide some options via the command line without a footprint (such as
> type).


## Support

> For now, Progeny will fail to run on Windows simply because I haven't gotten around to it yet.  It is known to work on
> Linux systems under Python 2 (it should also work in Python 3, though this is untested currently) and it might run on
> OS X, but if so, purely by accident because I never tested it on OS X.


## Contributing

> The great thing about Progeny is that you don't need to know how to write software in order to contribute (though, it
> helps). The easiest way to contribute is to write footprint files and send pull requests to the [Progeny Footprints](https://github.com/darthlukan/progeny-footprints)
> repository so that others can benefit from not having to write footprint files themselves. You can also test Progeny
> and submit bug reports.

> For those that are able to contribute code:

* Progeny aims to be compatible with Python 3 despite being written on a machine with only Python 2 installed
* The author has made an attempt to stick with PEP-8 styling where it makes sense, if you're unsure, turn on pyflakes in
  your Vim or Emacs configs, that's what I did.
* Please make every possible attempt to stick to using only the standard library where it makes sense to do so. The
  fewer external dependencies, the better.


## License
> GPLv3
