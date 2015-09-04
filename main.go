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

func CreateProject(c *cli.Context) error {
	// TODO
	return nil
}

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
			Name:  "template, t",
			Value: "template",
			Usage: "Your project template.",
		},
	}
	app.Action = func(c *cli.Context) {
		CreateProject(c)
	}
	app.Run(os.Args)
}
