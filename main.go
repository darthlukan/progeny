package main

import (
	"bufio"
	"errors"
	"fmt"
	"github.com/codegangsta/cli"
	"os"
	"path"
	"strings"
)

var (
	projectRoot string
	goPath      = os.Getenv("GOPATH")
)

func CreateProject(p *Project) error {
	// TODO
	return nil
}

func validateTemplate(c *cli.Context) (*Project, error) {
	fmt.Printf("Preparing to validate %v \n", c.Args().First())
	project := new(Project)
	template, err := os.Open(c.Args().First())
	if err != nil {
		return nil, err
	}
	defer template.Close()

	scanner := bufio.NewScanner(template)
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), "=")
		key := strings.TrimSpace(line[0])
		val := strings.TrimSpace(line[1])
		if val != "" {
			switch {
			case strings.Contains(key, "name"):
				project.AppName = val
			case strings.Contains(key, "author"):
				project.AuthorName = val
			case strings.Contains(key, "email"):
				project.AuthorEmail = val
			case strings.Contains(key, "type"):
				project.Type = val
			case strings.Contains(key, "license"):
				project.License = val
			case strings.Contains(key, "path"):
				project.ProjectDir = val
			case strings.Contains(key, "language"):
				project.Language = val
			}
		}
	}

	fmt.Printf("Performing template validation check... \n")

	checks := 0
	if project.AppName != "" {
		checks++
		fmt.Printf("App name check passed!\n")
	}

	if project.AuthorName != "" {
		checks++
		fmt.Printf("Author check passed!\n")
	}

	if project.AuthorEmail != "" {
		checks++
		fmt.Printf("Author contact check passed!\n")
	}

	if project.Type != "" {
		checks++
		fmt.Printf("Type check passed!\n")
	}

	if project.License != "" {
		checks++
		fmt.Printf("License check passed!\n")
	}

	if project.ProjectDir != "" {
		checks++
		fmt.Printf("Project path check passed!\n")
	}

	if project.Language != "" {
		checks++
		fmt.Printf("Project language check passed!\n")
	}

	if checks < 7 {
		e := `Validation Error: This template does not meet the minimum requirements for use. Please make sure your
		template includes the fields: name, author, email, type, license, path, and language.`
		return nil, errors.New(e)
	}

	return project, nil
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
		project, err := validateTemplate(c)
		if err != nil {
			fmt.Printf("%v\n", err)
			return
		}
		CreateProject(project)
	}
	app.Run(os.Args)
}
