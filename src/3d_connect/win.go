package main

var winningLines = generateWinningLines()

func generateWinningLines() [][]Coord {
	lines := make([][]Coord, 0)
	dirs := generateUniqueDirections()

	for z := 0; z < BoardSize; z++ {
		for y := 0; y < BoardSize; y++ {
			for x := 0; x < BoardSize; x++ {
				for _, d := range dirs {
					x2 := x + 2*d.X
					y2 := y + 2*d.Y
					z2 := z + 2*d.Z
					if !inBounds(x2, y2, z2) {
						continue
					}

					line := []Coord{
						{X: x, Y: y, Z: z},
						{X: x + d.X, Y: y + d.Y, Z: z + d.Z},
						{X: x2, Y: y2, Z: z2},
					}
					lines = append(lines, line)
				}
			}
		}
	}

	return lines
}

func generateUniqueDirections() []Coord {
	dirs := make([]Coord, 0)
	for dz := -1; dz <= 1; dz++ {
		for dy := -1; dy <= 1; dy++ {
			for dx := -1; dx <= 1; dx++ {
				if dx == 0 && dy == 0 && dz == 0 {
					continue
				}
				if firstNonZeroPositive(dx, dy, dz) {
					dirs = append(dirs, Coord{X: dx, Y: dy, Z: dz})
				}
			}
		}
	}
	return dirs
}

func firstNonZeroPositive(dx, dy, dz int) bool {
	if dx != 0 {
		return dx > 0
	}
	if dy != 0 {
		return dy > 0
	}
	return dz > 0
}

func inBounds(x, y, z int) bool {
	return x >= 0 && x < BoardSize && y >= 0 && y < BoardSize && z >= 0 && z < BoardSize
}

func CheckWinner(b *Board) rune {
	for _, line := range winningLines {
		a := b.Cell(line[0].X, line[0].Y, line[0].Z)
		if a == Empty {
			continue
		}
		b1 := b.Cell(line[1].X, line[1].Y, line[1].Z)
		c := b.Cell(line[2].X, line[2].Y, line[2].Z)
		if a == b1 && b1 == c {
			return a
		}
	}
	return Empty
}
