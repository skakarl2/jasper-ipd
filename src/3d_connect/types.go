package main

const BoardSize = 3

const (
	Empty   rune = '.'
	PlayerX rune = 'X'
	PlayerO rune = 'O'
)

type Coord struct {
	X int
	Y int
	Z int
}
