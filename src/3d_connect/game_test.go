package connect3d

import "testing"

func TestGameMoveAndWin(t *testing.T) {
	g := NewGame()
	moves := [][3]int{
		{0, 0, 0}, // P1
		{0, 1, 0}, // P2
		{1, 1, 1}, // P1
		{0, 2, 0}, // P2
		{2, 2, 2}, // P1 (diagonal win)
	}
	for _, m := range moves {
		if !g.Move(m[0], m[1], m[2]) {
			t.Fatalf("Move %v should be valid", m)
		}
		if g.Winner != 0 {
			break
		}
	}
	if g.Winner != 1 {
		t.Fatalf("Player 1 should win, got %d", g.Winner)
	}
}

func TestGameDraw(t *testing.T) {
	g := NewGame()
	// Fill the board with no winner
	p := 1
	for x := 0; x < 3; x++ {
		for y := 0; y < 3; y++ {
			for z := 0; z < 3; z++ {
				g.Board.Place(x, y, z, p)
				p = 3 - p
			}
		}
	}
	if !g.Board.IsFull() {
		t.Fatal("Board should be full")
	}
	if checkWin(g.Board, 1) || checkWin(g.Board, 2) {
		t.Fatal("No player should win")
	}
}
