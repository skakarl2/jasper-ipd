package connect3d

import "testing"

func TestBoardPlaceAndGet(t *testing.T) {
	b := NewBoard()
	if !b.Place(1, 1, 1, 1) {
		t.Fatal("Should allow placing at (1,1,1)")
	}
	if b.Get(1, 1, 1) != 1 {
		t.Fatal("Get should return player 1 at (1,1,1)")
	}
	if b.Place(1, 1, 1, 2) {
		t.Fatal("Should not allow placing on occupied cell")
	}
	if b.Get(0, 0, 0) != 0 {
		t.Fatal("Empty cell should be 0")
	}
}

func TestBoardIsFull(t *testing.T) {
	b := NewBoard()
	count := 0
	for x := 0; x < 3; x++ {
		for y := 0; y < 3; y++ {
			for z := 0; z < 3; z++ {
				b.Place(x, y, z, 1)
				count++
			}
		}
	}
	if !b.IsFull() {
		t.Fatal("Board should be full after 27 moves")
	}
}
