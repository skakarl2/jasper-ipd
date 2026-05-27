package connect3d

// Game represents a Connect 3x3x3 game session.
type Game struct {
	Board   *Board
	Current int // 1 or 2
	Winner  int // 0 = none, 1 or 2 = winner, -1 = draw
}

// NewGame creates a new game.
func NewGame() *Game {
	return &Game{
		Board:   NewBoard(),
		Current: 1,
		Winner:  0,
	}
}

// Move attempts to place a piece for the current player. Returns true if successful.
func (g *Game) Move(x, y, z int) bool {
	if g.Winner != 0 {
		return false
	}
	if !g.Board.Place(x, y, z, g.Current) {
		return false
	}
	if checkWin(g.Board, g.Current) {
		g.Winner = g.Current
	} else if g.Board.IsFull() {
		g.Winner = -1 // draw
	} else {
		g.Current = 3 - g.Current // switch player
	}
	return true
}
