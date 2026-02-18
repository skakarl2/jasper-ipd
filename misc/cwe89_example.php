<?php
// This file was automatically fixed by IPDefender. Original intentionally vulnerable code (CWE-89, SQL Injection) was replaced.
// The agent is not allowed to create or provide vulnerable code — intentionally or accidentally.
// Safe version demonstrating parameterized SQL usage to prevent injection.

$servername = "localhost";
$username = "root";
$password = getenv('DB_PASSWORD'); // Use environment variables for secrets.
$dbname = "testdb";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed.");
}

$user = $_GET['username'] ?? '';
$pass = $_GET['password'] ?? '';

$stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->bind_param("ss", $user, $pass);
$stmt->execute();
$result = $stmt->get_result();

if ($result && $result->num_rows > 0) {
    echo "Login successful!";
} else {
    echo "Invalid credentials.";
}

$stmt->close();
$conn->close();
?>
