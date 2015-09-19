package main

import (
	"bufio"
	"os"
)

func OpenFile(path string) (*bufio.Scanner, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	return scanner, nil
}
