<?php
// Secure code example with no sensitive data leaks
if (isset($_GET['id'])) {
    $id = filter_var($_GET['id'], FILTER_SANITIZE_NUMBER_INT);

    // Include database credentials securely
    include 'config.php'; // Ensure this file is protected and not accessible publicly

    $conn = new mysqli($db_host, $db_username, $db_password, $db_name);

    if ($conn->connect_error) {
        // Log the error securely instead of exposing sensitive details to the user
        error_log("Database connection failed: " . $conn->connect_error);
        die("An error occurred. Please try again later.");
    }

    // Using prepared statements to prevent SQL Injection
    $sql = "SELECT * FROM users WHERE id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            echo "User: " . htmlspecialchars($row["username"]) . "<br>";
        }
    } else {
        echo "No results found.";
    }

    $stmt->close();
    $conn->close();
}
?>