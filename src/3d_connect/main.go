package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

	"jasper-ipd/src/3d_connect"
)

func printBoard(b *connect3d.Board) {
	for z := 0; z < 3; z++ {
		fmt.Printf("Layer %d:\n", z)
		for y := 0; y < 3; y++ {
			for x := 0; x < 3; x++ {
				cell := b.Get(x, y, z)
				ch := '.'
				if cell == 1 {
					ch = 'X'
				} else if cell == 2 {
					ch = 'O'
				}
				fmt.Printf("%c ", ch)
			}
			fmt.Println()
		}
		fmt.Println()
	}
}

func main() {
	game := connect3d.NewGame()
	reader := bufio.NewReader(os.Stdin)
	for game.Winner == 0 {
		printBoard(game.Board)
		fmt.Printf("Player %d's move (x y z): ", game.Current)
		line, _ := reader.ReadString('\n')
		parts := strings.Fields(line)
		if len(parts) != 3 {
			fmt.Println("Invalid input. Enter x y z.")
			continue
		}
		x, err1 := strconv.Atoi(parts[0])
		y, err2 := strconv.Atoi(parts[1])
		z, err3 := strconv.Atoi(parts[2])
		if err1 != nil || err2 != nil || err3 != nil {
			fmt.Println("Invalid numbers.")
			continue
		}
		if !game.Move(x, y, z) {
			fmt.Println("Invalid move.")
		}
	}
	printBoard(game.Board)
	if game.Winner == -1 {
		fmt.Println("It's a draw!")
	} else {
		fmt.Printf("Player %d wins!\n", game.Winner)
	}
}
