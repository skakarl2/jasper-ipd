package connect3d

// Board represents a 3x3x3 Connect game board.
type Board struct {
	cells [3][3][3]int // 0 = empty, 1 = player 1, 2 = player 2
}

// NewBoard creates a new empty board.
func NewBoard() *Board {
	return &Board{}
}

// Place places a player's piece at (x, y, z). Returns false if invalid.
func (b *Board) Place(x, y, z, player int) bool {
	if x < 0 || x > 2 || y < 0 || y > 2 || z < 0 || z > 2 {
		return false
	}
	if b.cells[x][y][z] != 0 {
		return false
	}
	b.cells[x][y][z] = player
	return true
}

// Get returns the value at (x, y, z).
func (b *Board) Get(x, y, z int) int {
	if x < 0 || x > 2 || y < 0 || y > 2 || z < 0 || z > 2 {
		return -1
	}
	return b.cells[x][y][z]
}

// IsFull returns true if the board is full.
func (b *Board) IsFull() bool {
	for x := 0; x < 3; x++ {
		for y := 0; y < 3; y++ {
			for z := 0; z < 3; z++ {
				if b.cells[x][y][z] == 0 {
					return false
				}
			}
		}
	}
	return true
}
