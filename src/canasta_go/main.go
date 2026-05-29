package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Card represents a single playing card
// Rank: 2-10, J, Q, K, A, Joker
// Suit: H, D, C, S, Joker
// Jokers are represented as Rank="Joker", Suit="Joker"
type Card struct {
	Rank string
	Suit string
}

// Deck returns a shuffled deck of 108 cards (2 decks + 4 jokers)
func NewDeck() []Card {
	ranks := []string{"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"}
	suits := []string{"H", "D", "C", "S"}
	deck := make([]Card, 0, 108)
	for d := 0; d < 2; d++ {
		for _, suit := range suits {
			for _, rank := range ranks {
				deck = append(deck, Card{Rank: rank, Suit: suit})
			}
		}
	}
	// Add 4 Jokers
	for i := 0; i < 4; i++ {
		deck = append(deck, Card{Rank: "Joker", Suit: "Joker"})
	}
	return deck
}

func Shuffle(deck []Card) {
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(deck), func(i, j int) {
		deck[i], deck[j] = deck[j], deck[i]
	})
}

// Player represents a player in the game
// Hand: cards in hand
// Melds: list of melds (each meld is a slice of cards)
type Player struct {
	Name  string
	Hand  []Card
	Melds [][]Card
}

// Game state
// DiscardPile: top card is last
// Stock: draw pile
// Players: 2 for this simple version
// Current: index of current player
// Canasta: true if a player has a canasta
// Winner: index of winner, -1 if none

type Game struct {
	Players    [2]Player
	Stock      []Card
	DiscardPile []Card
	Current    int
	Canasta    [2]bool
	Winner     int
}

func NewGame(p1, p2 string) *Game {
	deck := NewDeck()
	Shuffle(deck)
	players := [2]Player{{Name: p1}, {Name: p2}}
	for i := 0; i < 2; i++ {
		players[i].Hand = deck[:11]
		deck = deck[11:]
	}
	// Start discard pile with one card
	discard := []Card{deck[0]}
	deck = deck[1:]
	return &Game{
		Players: players,
		Stock: deck,
		DiscardPile: discard,
		Current: 0,
		Canasta: [2]bool{false, false},
		Winner: -1,
	}
}

func (g *Game) Draw(playerIdx int) {
	if len(g.Stock) == 0 {
		fmt.Println("Stock is empty!")
		return
	}
	card := g.Stock[0]
	g.Stock = g.Stock[1:]
	g.Players[playerIdx].Hand = append(g.Players[playerIdx].Hand, card)
	fmt.Printf("%s draws %s%s\n", g.Players[playerIdx].Name, card.Rank, card.Suit)
}

func (g *Game) Discard(playerIdx int, cardIdx int) {
	card := g.Players[playerIdx].Hand[cardIdx]
	g.Players[playerIdx].Hand = append(g.Players[playerIdx].Hand[:cardIdx], g.Players[playerIdx].Hand[cardIdx+1:]...)
	g.DiscardPile = append(g.DiscardPile, card)
	fmt.Printf("%s discards %s%s\n", g.Players[playerIdx].Name, card.Rank, card.Suit)
}

// Try to meld a set of cards (must be 3+ of same rank, wilds allowed)
func (g *Game) Meld(playerIdx int, cardIndices []int) bool {
	if len(cardIndices) < 3 {
		fmt.Println("Need at least 3 cards to meld.")
		return false
	}
	hand := g.Players[playerIdx].Hand
	meld := make([]Card, 0, len(cardIndices))
	rank := ""
	wilds := 0
	for _, idx := range cardIndices {
		c := hand[idx]
		if c.Rank == "2" || c.Rank == "Joker" {
			wilds++
		} else if rank == "" {
			rank = c.Rank
		} else if c.Rank != rank {
			fmt.Println("All non-wild cards must match rank.")
			return false
		}
		meld = append(meld, c)
	}
	if wilds > len(meld)/2 {
		fmt.Println("Too many wilds in meld.")
		return false
	}
	// Remove cards from hand
	newHand := make([]Card, 0, len(hand)-len(cardIndices))
	used := make(map[int]bool)
	for _, idx := range cardIndices {
		used[idx] = true
	}
	for i, c := range hand {
		if !used[i] {
			newHand = append(newHand, c)
		}
	}
	g.Players[playerIdx].Hand = newHand
	g.Players[playerIdx].Melds = append(g.Players[playerIdx].Melds, meld)
	fmt.Printf("%s melds: ", g.Players[playerIdx].Name)
	for _, c := range meld {
		fmt.Printf("%s%s ", c.Rank, c.Suit)
	}
	fmt.Println()
	// Check for canasta (7+ cards in meld)
	if len(meld) >= 7 {
		g.Canasta[playerIdx] = true
		fmt.Printf("%s has a canasta!\n", g.Players[playerIdx].Name)
	}
	return true
}

func (g *Game) CheckWinner() {
	for i, p := range g.Players {
		if len(p.Hand) == 0 && g.Canasta[i] {
			g.Winner = i
		}
	}
}

func (g *Game) PrintState() {
	fmt.Println("\n--- Game State ---")
	for i, p := range g.Players {
		fmt.Printf("%s's hand: ", p.Name)
		for _, c := range p.Hand {
			fmt.Printf("%s%s ", c.Rank, c.Suit)
		}
		fmt.Println()
		fmt.Printf("Melds: ")
		for _, meld := range p.Melds {
			fmt.Print("[")
			for _, c := range meld {
				fmt.Printf("%s%s ", c.Rank, c.Suit)
			}
			fmt.Print("] ")
		}
		fmt.Println()
	}
	fmt.Printf("Discard pile: ")
	for _, c := range g.DiscardPile {
		fmt.Printf("%s%s ", c.Rank, c.Suit)
	}
	fmt.Println()
	fmt.Printf("Stock: %d cards\n", len(g.Stock))
	fmt.Println("-------------------\n")
}

func main() {
	g := NewGame("Alice", "Bob")
	for g.Winner == -1 {
		g.PrintState()
		cur := g.Current
		fmt.Printf("%s's turn.\n", g.Players[cur].Name)
		g.Draw(cur)
		// For demo, try to meld first 3 cards if possible
		if len(g.Players[cur].Hand) >= 3 {
			g.Meld(cur, []int{0, 1, 2})
		}
		// Discard last card
		if len(g.Players[cur].Hand) > 0 {
			g.Discard(cur, len(g.Players[cur].Hand)-1)
		}
		g.CheckWinner()
		g.Current = 1 - g.Current
	}
	fmt.Printf("Game over! Winner: %s\n", g.Players[g.Winner].Name)
}
