package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type InputReader struct {
	scanner *bufio.Scanner
}

func NewInputReader() *InputReader {
	return &InputReader{scanner: bufio.NewScanner(os.Stdin)}
}

func (r *InputReader) ReadMove(p Player) (int, int, error) {
	fmt.Printf("%s (%c), enter move as: x y (1-4 each): ", p.Name, p.Symbol)
	if !r.scanner.Scan() {
		return -1, -1, fmt.Errorf("failed to read input")
	}

	line := strings.TrimSpace(r.scanner.Text())
	parts := strings.Fields(line)
	if len(parts) != 2 {
		return -1, -1, fmt.Errorf("please enter exactly two numbers")
	}

	x, err := strconv.Atoi(parts[0])
	if err != nil {
		return -1, -1, fmt.Errorf("invalid x value")
	}
	y, err := strconv.Atoi(parts[1])
	if err != nil {
		return -1, -1, fmt.Errorf("invalid y value")
	}

	return x - 1, y - 1, nil
}
