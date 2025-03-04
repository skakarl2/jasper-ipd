import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

public class VulnerableDatabase {
    public static void main(String[] args) throws Exception {
        String username = "username";
        String password = "password";
        Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb", username, password);
        try (PreparedStatement statement = connection.prepareStatement("SELECT * FROM users WHERE name = ?")) {
            // This is where the vulnerability occurs
            String userInput = new java.util.Scanner(System.in).nextLine();
            statement.setString(1, userInput);
            try (java.sql.ResultSet results = statement.executeQuery()) {
                while (results.next()) {
                    System.out.println(results.getString("name"));
                }
            }
        } finally {
            connection.close();
        }
    }
}
