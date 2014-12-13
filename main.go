package main

import (
	"fmt"
	"github.com/codegangsta/cli"
	"os"
)

func main() {
	fmt.Printf("Hello, World!\n")
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
	}
	app.Run(os.Args)
}
