package main

import (
	"fmt"
	"math/rand"
	"time"
)

const (
	NumPlayers = 2
	HandSize   = 11
)

type Suit string
type Rank string

type Card struct {
	Suit Suit
	Rank Rank
}

type Player struct {
	Name  string
	Hand  []Card
	Score int
	Melds [][]Card
}

type Game struct {
	Players    [NumPlayers]Player
	Deck       []Card
	Discard    []Card
	Current    int
	GameOver   bool
}

var Suits = []Suit{"Hearts", "Diamonds", "Clubs", "Spades"}
var Ranks = []Rank{"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}

func NewDeck() []Card {
	deck := make([]Card, 0, 108)
	for d := 0; d < 2; d++ {
		for _, s := range Suits {
			for _, r := range Ranks {
				deck = append(deck, Card{Suit: s, Rank: r})
			}
		}
		// Add Jokers (2 per deck)
		deck = append(deck, Card{Suit: "Joker", Rank: "Joker"})
		deck = append(deck, Card{Suit: "Joker", Rank: "Joker"})
	}
	return deck
}

func Shuffle(deck []Card) {
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(deck), func(i, j int) {
		deck[i], deck[j] = deck[j], deck[i]
	})
}

func Deal(g *Game) {
	for i := 0; i < NumPlayers; i++ {
		g.Players[i].Hand = g.Deck[:HandSize]
		g.Deck = g.Deck[HandSize:]
	}
	g.Discard = append(g.Discard, g.Deck[0])
	g.Deck = g.Deck[1:]
}

func (g *Game) Draw(playerIdx int) Card {
	if len(g.Deck) == 0 {
		fmt.Println("Deck is empty!")
		return Card{}
	}
	card := g.Deck[0]
	g.Deck = g.Deck[1:]
	g.Players[playerIdx].Hand = append(g.Players[playerIdx].Hand, card)
	return card
}

func (g *Game) DiscardCard(playerIdx int, cardIdx int) {
	card := g.Players[playerIdx].Hand[cardIdx]
	g.Players[playerIdx].Hand = append(g.Players[playerIdx].Hand[:cardIdx], g.Players[playerIdx].Hand[cardIdx+1:]...)
	g.Discard = append(g.Discard, card)
}

func (g *Game) ShowHands() {
	for i, p := range g.Players {
		fmt.Printf("Player %d (%s): ", i+1, p.Name)
		for _, c := range p.Hand {
			fmt.Printf("%s-%s ", c.Rank, c.Suit)
		}
		fmt.Println()
	}
}

func main() {
	g := Game{}
	g.Players[0].Name = "Alice"
	g.Players[1].Name = "Bob"
	g.Deck = NewDeck()
	Shuffle(g.Deck)
	Deal(&g)
	fmt.Println("Initial hands:")
	g.ShowHands()

	for !g.GameOver {
		player := &g.Players[g.Current]
		fmt.Printf("\n%s's turn\n", player.Name)
		fmt.Println("Drawing a card...")
		g.Draw(g.Current)
		g.ShowHands()
		fmt.Println("Choose a card to discard (0-indexed):")
		var idx int
		fmt.Scan(&idx)
		if idx < 0 || idx >= len(player.Hand) {
			fmt.Println("Invalid index, discarding last card.")
			idx = len(player.Hand) - 1
		}
		g.DiscardCard(g.Current, idx)
		fmt.Printf("%s discarded.\n", player.Name)
		g.ShowHands()
		// End condition: if a player has no cards
		if len(player.Hand) == 0 {
			fmt.Printf("%s has gone out!\n", player.Name)
			g.GameOver = true
		}
		g.Current = (g.Current + 1) % NumPlayers
	}
	fmt.Println("Game over!")
}
