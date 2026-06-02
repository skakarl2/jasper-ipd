package main

import (
	"errors"
	"fmt"
	"strings"
)

type Board struct {
	cells [BoardSize][BoardSize][BoardSize]rune
}

func NewBoard() *Board {
	b := &Board{}
	for x := 0; x < BoardSize; x++ {
		for y := 0; y < BoardSize; y++ {
			for z := 0; z < BoardSize; z++ {
				b.cells[x][y][z] = EmptyCell
			}
		}
	}
	return b
}

func (b *Board) IsInBounds(x, y, z int) bool {
	return x >= 0 && x < BoardSize && y >= 0 && y < BoardSize && z >= 0 && z < BoardSize
}

func (b *Board) Get(x, y, z int) rune {
	if !b.IsInBounds(x, y, z) {
		return EmptyCell
	}
	return b.cells[x][y][z]
}

func (b *Board) Drop(x, y int, symbol rune) (int, error) {
	if x < 0 || x >= BoardSize || y < 0 || y >= BoardSize {
		return -1, errors.New("column out of range; use x,y in 1..4")
	}

	for z := 0; z < BoardSize; z++ {
		if b.cells[x][y][z] == EmptyCell {
			b.cells[x][y][z] = symbol
			return z, nil
		}
	}

	return -1, errors.New("column is full")
}

func (b *Board) IsFull() bool {
	for x := 0; x < BoardSize; x++ {
		for y := 0; y < BoardSize; y++ {
			if b.cells[x][y][BoardSize-1] == EmptyCell {
				return false
			}
		}
	}
	return true
}

func (b *Board) Render() string {
	var sb strings.Builder

	for z := BoardSize - 1; z >= 0; z-- {
		sb.WriteString(fmt.Sprintf("Level z=%d\n", z+1))
		sb.WriteString("   y: 1 2 3 4\n")
		for x := 0; x < BoardSize; x++ {
			sb.WriteString(fmt.Sprintf("x=%d   ", x+1))
			for y := 0; y < BoardSize; y++ {
				sb.WriteRune(b.cells[x][y][z])
				if y != BoardSize-1 {
					sb.WriteRune(' ')
				}
			}
			sb.WriteRune('\n')
		}
		sb.WriteRune('\n')
	}

	return sb.String()
}
