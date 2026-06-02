package main

import "fmt"

func main() {
	fmt.Println("Connect 4x4x4")
	fmt.Println("--------------")
	fmt.Println("Two players alternate dropping pieces into a 4x4 board of columns.")
	fmt.Println("Columns are addressed by x y where x,y are 1..4.")
	fmt.Println("A piece falls to the lowest free z in that column.")
	fmt.Println("First player to align 4 pieces in any 3D straight line wins.")
	fmt.Println()

	game := NewGame()
	game.Play()
}
