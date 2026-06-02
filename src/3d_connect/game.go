package main

import (
	"errors"
	"math/rand"
	"time"
)

type Game struct {
	Board        Board
	Current      rune
	Winner       rune
	IsOver       bool
	AIEnabled    bool
	AIPlayer     rune
	randSource   *rand.Rand
	QuitByPlayer bool
}

func NewGame(aiEnabled bool, aiPlayer rune) *Game {
	return &Game{
		Board:      NewBoard(),
		Current:    PlayerX,
		Winner:     Empty,
		IsOver:     false,
		AIEnabled:  aiEnabled,
		AIPlayer:   aiPlayer,
		randSource: rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

func (g *Game) OtherPlayer(player rune) rune {
	if player == PlayerX {
		return PlayerO
	}
	return PlayerX
}

func (g *Game) PlayTurn(x, y int) (Coord, error) {
	if g.IsOver {
		return Coord{}, errors.New("game is already over")
	}

	z, err := g.Board.DropDisc(x, y, g.Current)
	if err != nil {
		return Coord{}, err
	}

	move := Coord{X: x, Y: y, Z: z}
	winner := CheckWinner(&g.Board)
	if winner != Empty {
		g.Winner = winner
		g.IsOver = true
		return move, nil
	}

	if g.Board.IsFull() {
		g.IsOver = true
		return move, nil
	}

	g.Current = g.OtherPlayer(g.Current)
	return move, nil
}

func (g *Game) AISelectMove() (Coord, error) {
	if !g.AIEnabled {
		return Coord{}, errors.New("ai is disabled")
	}

	moves := g.Board.ValidMoves()
	if len(moves) == 0 {
		return Coord{}, errors.New("no valid moves")
	}

	for _, m := range moves {
		clone := g.Board.Clone()
		_, _ = clone.DropDisc(m.X, m.Y, g.AIPlayer)
		if CheckWinner(&clone) == g.AIPlayer {
			return m, nil
		}
	}

	opponent := g.OtherPlayer(g.AIPlayer)
	for _, m := range moves {
		clone := g.Board.Clone()
		_, _ = clone.DropDisc(m.X, m.Y, opponent)
		if CheckWinner(&clone) == opponent {
			return m, nil
		}
	}

	for _, m := range moves {
		if m.X == 1 && m.Y == 1 {
			return m, nil
		}
	}

	return moves[g.randSource.Intn(len(moves))], nil
}
