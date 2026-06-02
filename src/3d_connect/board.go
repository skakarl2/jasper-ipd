package main

import (
	"errors"
	"fmt"
	"strings"
)

type Board struct {
	cells [BoardSize][BoardSize][BoardSize]rune
}

func NewBoard() Board {
	b := Board{}
	for z := 0; z < BoardSize; z++ {
		for y := 0; y < BoardSize; y++ {
			for x := 0; x < BoardSize; x++ {
				b.cells[z][y][x] = Empty
			}
		}
	}
	return b
}

func (b *Board) DropDisc(x, y int, player rune) (int, error) {
	if x < 0 || x >= BoardSize || y < 0 || y >= BoardSize {
		return -1, errors.New("coordinates out of bounds")
	}

	for z := 0; z < BoardSize; z++ {
		if b.cells[z][y][x] == Empty {
			b.cells[z][y][x] = player
			return z, nil
		}
	}

	return -1, errors.New("column is full")
}

func (b *Board) Cell(x, y, z int) rune {
	return b.cells[z][y][x]
}

func (b *Board) IsFull() bool {
	for z := 0; z < BoardSize; z++ {
		for y := 0; y < BoardSize; y++ {
			for x := 0; x < BoardSize; x++ {
				if b.cells[z][y][x] == Empty {
					return false
				}
			}
		}
	}
	return true
}

func (b *Board) IsColumnFull(x, y int) bool {
	return b.cells[BoardSize-1][y][x] != Empty
}

func (b *Board) String() string {
	var sb strings.Builder
	sb.WriteString("Coordinates: x y are 1..3, discs fall on z-axis\n")

	for z := BoardSize - 1; z >= 0; z-- {
		sb.WriteString(fmt.Sprintf("\nLayer z=%d\n", z+1))
		sb.WriteString("   1 2 3\n")
		for y := 0; y < BoardSize; y++ {
			sb.WriteString(fmt.Sprintf("%d  ", y+1))
			for x := 0; x < BoardSize; x++ {
				sb.WriteRune(b.cells[z][y][x])
				if x < BoardSize-1 {
					sb.WriteRune(' ')
				}
			}
			sb.WriteRune('\n')
		}
	}

	return sb.String()
}

func (b *Board) Clone() Board {
	copyBoard := NewBoard()
	copyBoard.cells = b.cells
	return copyBoard
}

func (b *Board) ValidMoves() []Coord {
	moves := make([]Coord, 0, BoardSize*BoardSize)
	for y := 0; y < BoardSize; y++ {
		for x := 0; x < BoardSize; x++ {
			if b.IsColumnFull(x, y) {
				continue
			}
			for z := 0; z < BoardSize; z++ {
				if b.cells[z][y][x] == Empty {
					moves = append(moves, Coord{X: x, Y: y, Z: z})
					break
				}
			}
		}
	}
	return moves
}
