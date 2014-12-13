package main

import (
	"github.com/codegangsta/cli"
	"os"
	"path"
)

var (
	projectRoot string
	goPath      = os.Getenv("GOPATH")
)

func init() {
	if goPath == "" {
		projectRoot = "."
	} else {
		projectRoot = path.Join(goPath, "src", "github.com", "darthlukan", "progeny")
	}
}

func main() {
	app := cli.NewApp()
	app.Name = "Progeny"
	app.Author = "Brian Tomlinson"
	app.Email = "darthlukan@gmail.com"
	app.Usage = "Generate project files automagically!"
	app.Version = "0.0.1"
	app.Flags = []cli.Flag{
		cli.StringFlag{
			Name:  "lang, l",
			Value: "go",
			Usage: "Project language",
		},
		cli.StringFlag{
			Name:  "name, n",
			Value: "my_app",
			Usage: "The name of your project",
		},
		cli.StringFlag{
			Name:  "license, L",
			Value: "gpl3",
			Usage: "Project license",
		},
		cli.StringFlag{
			Name:  "dir, d",
			Value: "$GOPATH",
			Usage: "Project directory",
		},
		cli.StringFlag{
			Name:  "authorname, a",
			Value: "Your name here",
			Usage: "Your name",
		},
		cli.StringFlag{
			Name:  "email, e",
			Value: "you@youremail.com",
			Usage: "Your email address",
		},
	}
	app.Run(os.Args)
}
