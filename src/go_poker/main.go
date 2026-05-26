package main

import (
	"fmt"
	"math/rand"
	"sort"
	"time"
)

var suits = []string{"♠", "♥", "♦", "♣"}
var ranks = []string{"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"}

// Card represents a playing card
type Card struct {
	Suit string
	Rank string
}

func (c Card) String() string {
	return fmt.Sprintf("%s%s", c.Rank, c.Suit)
}

// Deck represents a deck of cards
type Deck []Card

func NewDeck() Deck {
	deck := make(Deck, 0, 52)
	for _, suit := range suits {
		for _, rank := range ranks {
			deck = append(deck, Card{Suit: suit, Rank: rank})
		}
	}
	return deck
}

func (d Deck) Shuffle() {
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(d), func(i, j int) {
		d[i], d[j] = d[j], d[i]
	})
}

func (d *Deck) Deal(n int) []Card {
	cards := (*d)[:n]
	*d = (*d)[n:]
	return cards
}

// Player represents a poker player
type Player struct {
	Name string
	Hand []Card
}

// PokerGame represents a simple poker game
// (5-card draw, no betting, winner by best hand)
type PokerGame struct {
	Players []Player
	Deck    Deck
}

func NewPokerGame(playerNames []string) *PokerGame {
	deck := NewDeck()
	deck.Shuffle()
	players := make([]Player, len(playerNames))
	for i, name := range playerNames {
		players[i] = Player{Name: name}
	}
	return &PokerGame{Players: players, Deck: deck}
}

func (g *PokerGame) DealHands() {
	for i := range g.Players {
		g.Players[i].Hand = g.Deck.Deal(5)
	}
}

func (g *PokerGame) ShowHands() {
	for _, p := range g.Players {
		fmt.Printf("%s: %v\n", p.Name, p.Hand)
	}
}

// EvaluateHand returns a simple score for a hand (for demo: by highest card)
func EvaluateHand(hand []Card) int {
	// Map rank to value
	rankValue := make(map[string]int)
	for i, r := range ranks {
		rankValue[r] = i
	}
	max := 0
	for _, c := range hand {
		if rankValue[c.Rank] > max {
			max = rankValue[c.Rank]
		}
	}
	return max
}

func (g *PokerGame) Winner() *Player {
	best := -1
	var winner *Player
	for i := range g.Players {
		score := EvaluateHand(g.Players[i].Hand)
		if score > best {
			best = score
			winner = &g.Players[i]
		}
	}
	return winner
}

func main() {
	playerNames := []string{"Alice", "Bob", "Carol", "Dave"}
	game := NewPokerGame(playerNames)
	game.DealHands()
	fmt.Println("Hands:")
	game.ShowHands()
	w := game.Winner()
	fmt.Printf("\nWinner: %s\n", w.Name)
}
