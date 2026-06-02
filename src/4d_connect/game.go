package main

import "fmt"

type Game struct {
	board   *Board
	players [2]Player
	turn    int
	input   *InputReader
}

func NewGame() *Game {
	return &Game{
		board: NewBoard(),
		players: [2]Player{
			{Name: "Player 1", Symbol: 'X'},
			{Name: "Player 2", Symbol: 'O'},
		},
		turn:  0,
		input: NewInputReader(),
	}
}

func (g *Game) currentPlayer() Player {
	return g.players[g.turn%2]
}

func (g *Game) switchTurn() {
	g.turn++
}

func (g *Game) Play() {
	for {
		fmt.Println(g.board.Render())

		p := g.currentPlayer()
		x, y, err := g.input.ReadMove(p)
		if err != nil {
			fmt.Println("Input error:", err)
			fmt.Println()
			continue
		}

		z, err := g.board.Drop(x, y, p.Symbol)
		if err != nil {
			fmt.Println("Move error:", err)
			fmt.Println()
			continue
		}

		if g.board.HasConnect4From(x, y, z, p.Symbol) {
			fmt.Println(g.board.Render())
			fmt.Printf("%s wins!\n", p.Name)
			return
		}

		if g.board.IsFull() {
			fmt.Println(g.board.Render())
			fmt.Println("Draw: board is full.")
			return
		}

		g.switchTurn()
	}
}
