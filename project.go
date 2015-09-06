package main

import (
	"github.com/codegangsta/cli"
	"os"
)

type Project struct {
	AppName     string
	AuthorName  string
	AuthorEmail string
	Description string
	Language    string
	License     string
	ProjectDir  string
	Type        string
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

func (p *Project) CreateProjectDir() error {
	return os.MkdirAll(p.ProjectDir, 0775)
}

func (p *Project) GoPathHandler() error {
	// TODO: Handle VCS choice!
	return nil
}
