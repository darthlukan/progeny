package main

import (
	"bufio"
	"fmt"
	"os"
)

var readmeBase = `
# %s

> Author: %s <%s>

## Description

> %s

## LICENSE

> %s, see LICENSE file.
`

func writeReadme(data string, destPath string) error {
	file, err := os.Create(destPath)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	i, err := writer.WriteString(data)
	fmt.Printf("Wrote %v bytes\n", i)
	if err != nil {
		return err
	}
	return writer.Flush()
}

func GenerateReadme(p *Project) error {
	var readme = fmt.Sprintf(readmeBase, p.AppName, p.AuthorName, p.AuthorEmail, p.Description, p.License)
	destination := fmt.Sprintf("%s/README.md", p.ProjectDir)

	return writeReadme(readme, destination)
}
