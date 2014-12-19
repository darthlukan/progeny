package main

import (
	"bufio"
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

type Project struct {
	AppName     string
	AuthorName  string
	AuthorEmail string
    VCS         string
	GitHubUser  string
	Language    string
	License     string
	ProjectDir  string
}

func (p *Project) PythonHandler(c *cli.Context) error {
    // TODO: Don't forget setup.py!
	return nil
}

func (p *Project) GolangHandler(c *cli.Context) error {
    // TODO
	return nil
}

func (p *Project) ReadmeHandler(c *cli.Context) error {
    // TODO: Copy to projectDir and replace name
	return nil
}

func (p *Project) LicenseHandler(c *cli.Context) error {
    // TODO: Choose License file and copy to projectDir
	return nil
}

func (p *Project) VCSHandler(c *cli.Context) error {
    // TODO: Determine remote via VCS choice
    return nil
}

func (p *Project) CreateProjectDir(dirname string) error {
    return os.MkdirAll(dirname, 0775)
}

func (p *Project) CopyFiles(from, to string) error {
    orig_lines, err := p.readLines(from)
    if err != nil {
        return err
    }
    writeStatus := p.writeLines(orig_lines, to)
	return writeStatus
}

func (p *Project) GoPathHandler() error {
    // TODO: Handle VCS choice!
	appDir := path.Join(goPath, "src", p.VCS, p.GitHubUser, p.AppName)
	os.Stdout.WriteString(appDir)
	return nil
}

func (p *Project) readLines(filePath string) ([]string, error) {
	var lines []string

	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func (p *Project) writeLines(lines []string, destPath string) error {
	file, err := os.Create(destPath)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	for _, line := range lines {
		fmt.Fprintln(writer, line)
	}
	return writer.Flush()
}

func (p *Project) ReplaceReadmeNames(readme []string) error {
	var appName, author, email, license string
	for _, line := range readme {
		if strings.Contains(line, "{{APP_NAME}}") {
			appName = strings.Replace(line, "{{APP_NAME}}", p.AppName, 1)
		}
		if strings.Contains(line, "{{AUTHOR}}") {
			author = strings.Replace(line, "{{AUTHOR}}", p.AuthorName, 1)
		}
		if strings.Contains(line, "{{AUTHOR_EMAIL}}") {
			email = strings.Replace(line, "{{AUTHOR_EMAIL}}", p.AuthorEmail, 1)
		}
		if strings.Contains(line, "{{LICENSE}}") {
			license = strings.Replace(line, "{{LICENSE}}", p.License, 1)
		}
		fmt.Printf("line: %v\n, vars: %v, %v, %v, %v\n", line, appName, author, email, license)
	}
	return nil
}

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
		cli.StringFlag{
			Name:  "github-username, g",
			Value: "github_username",
			Usage: "Your GitHub username",
		},
	}
	app.Action = func(c *cli.Context) {
		CreateProject(c)
	}
	app.Run(os.Args)
}
