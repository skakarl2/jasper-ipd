package src;

import java.util.*;

public class CanastaPlayer {
    public final String name;
    public final List<Card> hand = new ArrayList<>();
    public final List<List<Card>> melds = new ArrayList<>();
    public int score = 0;
    public CanastaPlayer(String name) {
        this.name = name;
    }
    public void draw(Card card) {
        hand.add(card);
    }
    public void discard(Card card) {
        hand.remove(card);
    }
    public boolean hasCanasta() {
        for (List<Card> meld : melds) {
            if (meld.size() >= 7) return true;
        }
        return false;
    }
}
