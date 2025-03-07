import java.util.Scanner;

public class VulnerableClass {

    String[] usernames = {"admin", "user"};
    String[] passwords = {"password", "12345"};

    public void login() {
        Scanner input = new Scanner(System.in);
        
        System.out.println("Enter username: ");
        String username = input.nextLine();
        
        System.out.println("Enter password: ");
        String password = input.nextLine();
        
        if (validateUser(username, password)) {
            System.out.println("Login successful!");
        } else {
            System.out.println("Login failed. Please try again.");
        }
    }

    public boolean validateUser(String username, String password) {
        for (int i = 0; i < usernames.length; i++) {
            if (username.equals(usernames[i]) && password.equals(passwords[i])) {
                return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        VulnerableClass vulnerable = new VulnerableClass();
        vulnerable.login();
    }
    
}
