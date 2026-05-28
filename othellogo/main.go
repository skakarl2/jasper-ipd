package main

import (
	"fmt"
	"os"
)

const (
	Empty = 0
	Black = 1
	White = 2
	BoardSize = 8
)

type Board [BoardSize][BoardSize]int

type Game struct {
	Board      Board
	Turn       int
	GameOver   bool
}

func NewGame() *Game {
	g := &Game{Turn: Black}
	g.Board[3][3] = White
	g.Board[3][4] = Black
	g.Board[4][3] = Black
	g.Board[4][4] = White
	return g
}

func (g *Game) PrintBoard() {
	fmt.Println("  a b c d e f g h")
	for i := 0; i < BoardSize; i++ {
		fmt.Printf("%d ", i+1)
		for j := 0; j < BoardSize; j++ {
			switch g.Board[i][j] {
			case Black:
				fmt.Print("● ")
			case White:
				fmt.Print("○ ")
			default:
				fmt.Print(". ")
			}
		}
		fmt.Println()
	}
}

var directions = [8][2]int{
	{-1, -1}, {-1, 0}, {-1, 1},
	{0, -1},          {0, 1},
	{1, -1},  {1, 0}, {1, 1},
}

func (g *Game) IsValidMove(row, col, color int) bool {
	if g.Board[row][col] != Empty {
		return false
	}
	opp := Black
	if color == Black {
		opp = White
	}
	for _, d := range directions {
		dr, dc := d[0], d[1]
		r, c := row+dr, col+dc
		found := false
		for r >= 0 && r < BoardSize && c >= 0 && c < BoardSize && g.Board[r][c] == opp {
			r += dr
			c += dc
			found = true
		}
		if found && r >= 0 && r < BoardSize && c >= 0 && c < BoardSize && g.Board[r][c] == color {
			return true
		}
	}
	return false
}

func (g *Game) HasValidMove(color int) bool {
	for i := 0; i < BoardSize; i++ {
		for j := 0; j < BoardSize; j++ {
			if g.IsValidMove(i, j, color) {
				return true
			}
		}
	}
	return false
}

func (g *Game) ApplyMove(row, col, color int) bool {
	if !g.IsValidMove(row, col, color) {
		return false
	}
	g.Board[row][col] = color
	opp := Black
	if color == Black {
		opp = White
	}
	for _, d := range directions {
		dr, dc := d[0], d[1]
		r, c := row+dr, col+dc
		toFlip := [][2]int{}
		for r >= 0 && r < BoardSize && c >= 0 && c < BoardSize && g.Board[r][c] == opp {
			toFlip = append(toFlip, [2]int{r, c})
			r += dr
			c += dc
		}
		if r >= 0 && r < BoardSize && c >= 0 && c < BoardSize && g.Board[r][c] == color {
			for _, pos := range toFlip {
				g.Board[pos[0]][pos[1]] = color
			}
		}
	}
	return true
}

func (g *Game) Count(color int) int {
	count := 0
	for i := 0; i < BoardSize; i++ {
		for j := 0; j < BoardSize; j++ {
			if g.Board[i][j] == color {
				count++
			}
		}
	}
	return count
}

func parseMove(input string) (int, int, bool) {
	if len(input) != 2 {
		return 0, 0, false
	}
	col := int(input[0] - 'a')
	row := int(input[1] - '1')
	if row < 0 || row >= BoardSize || col < 0 || col >= BoardSize {
		return 0, 0, false
	}
	return row, col, true
}

func main() {
	g := NewGame()
	for !g.GameOver {
		g.PrintBoard()
		fmt.Printf("Black: %d, White: %d\n", g.Count(Black), g.Count(White))
		color := g.Turn
		colorName := "Black"
		if color == White {
			colorName = "White"
		}
		if !g.HasValidMove(color) {
			if !g.HasValidMove(3-color) {
				g.GameOver = true
				break
			}
			fmt.Printf("%s has no valid moves. Skipping turn.\n", colorName)
			g.Turn = 3 - color
			continue
		}
		fmt.Printf("%s's move (e.g., d3): ", colorName)
		var move string
		_, err := fmt.Scan(&move)
		if err != nil {
			fmt.Println("Input error.")
			os.Exit(1)
		}
		row, col, ok := parseMove(move)
		if !ok || !g.ApplyMove(row, col, color) {
			fmt.Println("Invalid move. Try again.")
			continue
		}
		g.Turn = 3 - color
	}
	g.PrintBoard()
	fmt.Println("Game over!")
	fmt.Printf("Final Score - Black: %d, White: %d\n", g.Count(Black), g.Count(White))
	if g.Count(Black) > g.Count(White) {
		fmt.Println("Black wins!")
	} else if g.Count(White) > g.Count(Black) {
		fmt.Println("White wins!")
	} else {
		fmt.Println("It's a tie!")
	}
}
