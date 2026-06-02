package main

// All unique line directions in a 3D grid, folded to avoid duplicates.
var directions = [][3]int{
	{1, 0, 0},
	{0, 1, 0},
	{0, 0, 1},
	{1, 1, 0},
	{1, -1, 0},
	{1, 0, 1},
	{1, 0, -1},
	{0, 1, 1},
	{0, 1, -1},
	{1, 1, 1},
	{1, 1, -1},
	{1, -1, 1},
	{1, -1, -1},
}

func (b *Board) HasConnect4From(x, y, z int, symbol rune) bool {
	for _, d := range directions {
		count := 1
		count += b.countDirection(x, y, z, d[0], d[1], d[2], symbol)
		count += b.countDirection(x, y, z, -d[0], -d[1], -d[2], symbol)
		if count >= 4 {
			return true
		}
	}
	return false
}

func (b *Board) countDirection(x, y, z, dx, dy, dz int, symbol rune) int {
	count := 0
	cx, cy, cz := x+dx, y+dy, z+dz

	for b.IsInBounds(cx, cy, cz) && b.Get(cx, cy, cz) == symbol {
		count++
		cx += dx
		cy += dy
		cz += dz
	}

	return count
}
