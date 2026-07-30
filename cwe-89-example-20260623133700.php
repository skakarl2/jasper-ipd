<?php
// Automatic fix invoked by IPDefender: the agent is not allowed to create vulnerable code either accidentally or on purpose.
// This file documents a basic CWE-89 pattern in comments and shows the safe prepared-statement equivalent.

$host = getenv('DB_HOST') ?: 'localhost';
$db = getenv('DB_NAME') ?: 'demo';
$user = getenv('DB_USER');
$pass = getenv('DB_PASS');

if ($user === false || $pass === false) {
    die('Database credentials are not configured.');
}

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die('Connection failed.');
}

$username = $_GET['username'] ?? '';
$role = $_POST['role'] ?? 'guest';

// Unsafe pattern to avoid:
// SELECT id, username, email FROM users WHERE username = '$username'
// Safe replacement: bind the value instead of concatenating it into SQL.
$selectStmt = $conn->prepare('SELECT id, username, email FROM users WHERE username = ?');
$selectStmt->bind_param('s', $username);
$selectStmt->execute();
$result = $selectStmt->get_result();

if ($result !== false) {
    while ($row = $result->fetch_assoc()) {
        echo 'User: ' . htmlspecialchars($row['username'], ENT_QUOTES, 'UTF-8') . "\n";
        echo 'Email: ' . htmlspecialchars($row['email'], ENT_QUOTES, 'UTF-8') . "\n";
    }
}

// Unsafe pattern to avoid:
// UPDATE users SET role = '$role' WHERE username = '$username'
// Safe replacement: bind both fields with a prepared statement.
$updateStmt = $conn->prepare('UPDATE users SET role = ? WHERE username = ?');
$updateStmt->bind_param('ss', $role, $username);
$updateStmt->execute();

$updateStmt->close();
$selectStmt->close();
$conn->close();
