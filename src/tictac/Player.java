package tictac;

import java.util.Scanner;

public interface Player {
    String getName();

    Mark getMark();

    Move chooseMove(TicTacToeBoard board, Scanner scanner);

    boolean isComputer();
}
