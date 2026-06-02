package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Println("3D Connect 3x3x3")
	fmt.Println("=================")
	fmt.Println("Created with love by ChatGPT")
	fmt.Println("Choose mode:")
	fmt.Println("1) Player vs Player")
	fmt.Println("2) Player vs Computer")

	mode := askMode(reader)
	aiEnabled := mode == 2
	aiPlayer := PlayerO

	if aiEnabled {
		aiPlayer = askAIOrder(reader)
	}

	game := NewGame(aiEnabled, aiPlayer)

	for !game.IsOver {
		fmt.Println()
		fmt.Print(game.Board.String())
		fmt.Println()

		if game.AIEnabled && game.Current == game.AIPlayer {
			move, err := game.AISelectMove()
			if err != nil {
				fmt.Printf("Game AI error: %v\n", err)
				return
			}
			played, err := game.PlayTurn(move.X, move.Y)
			if err != nil {
				fmt.Printf("AI move failed: %v\n", err)
				return
			}
			fmt.Printf("Computer played x=%d y=%d (z=%d)\n", played.X+1, played.Y+1, played.Z+1)
			continue
		}

		fmt.Printf("Player %c turn. Enter move as 'x y' (1..3), or 'q' to quit: ", game.Current)
		line, err := reader.ReadString('\n')
		if err != nil {
			fmt.Printf("input error: %v\n", err)
			return
		}
		line = strings.TrimSpace(line)

		if strings.EqualFold(line, "q") || strings.EqualFold(line, "quit") {
			game.IsOver = true
			game.QuitByPlayer = true
			break
		}

		x, y, parseErr := parseMove(line)
		if parseErr != nil {
			fmt.Printf("invalid input: %v\n", parseErr)
			continue
		}

		_, err = game.PlayTurn(x, y)
		if err != nil {
			fmt.Printf("cannot play move: %v\n", err)
			continue
		}
	}

	fmt.Println()
	fmt.Print(game.Board.String())
	fmt.Println()

	switch {
	case game.QuitByPlayer:
		fmt.Println("Game ended by player.")
	case game.Winner != Empty:
		fmt.Printf("Player %c wins!\n", game.Winner)
	default:
		fmt.Println("Draw.")
	}
}

func askMode(reader *bufio.Reader) int {
	for {
		fmt.Print("Select 1 or 2: ")
		line, err := reader.ReadString('\n')
		if err != nil {
			fmt.Printf("input error: %v\n", err)
			continue
		}
		line = strings.TrimSpace(line)
		if line == "1" {
			return 1
		}
		if line == "2" {
			return 2
		}
		fmt.Println("Please type 1 or 2.")
	}
}

func askAIOrder(reader *bufio.Reader) rune {
	for {
		fmt.Println("Who starts?")
		fmt.Println("1) You (X)")
		fmt.Println("2) Computer (X)")
		fmt.Print("Select 1 or 2: ")
		line, err := reader.ReadString('\n')
		if err != nil {
			fmt.Printf("input error: %v\n", err)
			continue
		}
		line = strings.TrimSpace(line)
		if line == "1" {
			return PlayerO
		}
		if line == "2" {
			return PlayerX
		}
		fmt.Println("Please type 1 or 2.")
	}
}

func parseMove(input string) (int, int, error) {
	parts := strings.Fields(input)
	if len(parts) != 2 {
		return 0, 0, fmt.Errorf("expected exactly two integers")
	}

	x, err := strconv.Atoi(parts[0])
	if err != nil {
		return 0, 0, fmt.Errorf("x is not an integer")
	}
	y, err := strconv.Atoi(parts[1])
	if err != nil {
		return 0, 0, fmt.Errorf("y is not an integer")
	}

	x--
	y--
	if x < 0 || x >= BoardSize || y < 0 || y >= BoardSize {
		return 0, 0, fmt.Errorf("x and y must be between 1 and 3")
	}

	return x, y, nil
}
