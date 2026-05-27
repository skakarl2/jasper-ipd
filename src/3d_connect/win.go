package connect3d

// checkWin checks if the given player has won on the board.
func checkWin(b *Board, player int) bool {
	lines := winLines()
	for _, line := range lines {
		win := true
		for _, pos := range line {
			x, y, z := pos[0], pos[1], pos[2]
			if b.Get(x, y, z) != player {
				win = false
				break
			}
		}
		if win {
			return true
		}
	}
	return false
}

// winLines returns all possible winning lines in 3x3x3.
func winLines() [][3][3]int {
	var lines [][3][3]int
	// Rows, columns, pillars
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			// Rows (x varies)
			lines = append(lines, [3][3]int{{0, i, j}, {1, i, j}, {2, i, j}})
			// Columns (y varies)
			lines = append(lines, [3][3]int{{i, 0, j}, {i, 1, j}, {i, 2, j}})
			// Pillars (z varies)
			lines = append(lines, [3][3]int{{i, j, 0}, {i, j, 1}, {i, j, 2}})
		}
	}
	// Diagonals in each plane
	for i := 0; i < 3; i++ {
		// xy planes
		lines = append(lines, [3][3]int{{0, 0, i}, {1, 1, i}, {2, 2, i}})
		lines = append(lines, [3][3]int{{0, 2, i}, {1, 1, i}, {2, 0, i}})
		// xz planes
		lines = append(lines, [3][3]int{{0, i, 0}, {1, i, 1}, {2, i, 2}})
		lines = append(lines, [3][3]int{{0, i, 2}, {1, i, 1}, {2, i, 0}})
		// yz planes
		lines = append(lines, [3][3]int{{i, 0, 0}, {i, 1, 1}, {i, 2, 2}})
		lines = append(lines, [3][3]int{{i, 0, 2}, {i, 1, 1}, {i, 2, 0}})
	}
	// Main space diagonals
	lines = append(lines, [3][3]int{{0, 0, 0}, {1, 1, 1}, {2, 2, 2}})
	lines = append(lines, [3][3]int{{0, 0, 2}, {1, 1, 1}, {2, 2, 0}})
	lines = append(lines, [3][3]int{{0, 2, 0}, {1, 1, 1}, {2, 0, 2}})
	lines = append(lines, [3][3]int{{0, 2, 2}, {1, 1, 1}, {2, 0, 0}})
	return lines
}
