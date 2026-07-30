<?php
/*
 * IPDefender automatic fix: The agent is not allowed to create vulnerable code,
 * either accidentally or on purpose. This file contains a safe CWE-89 mitigation example.
 */

declare(strict_types=1);

/**
 * Secure SQL usage examples (CWE-89 mitigation) using mysqli prepared statements.
 *
 * Notes:
 * - Uses environment variables for DB credentials (no hard-coded secrets).
 * - Uses parameterized queries for user-controlled values.
 * - Uses allowlist validation for ORDER BY column selection.
 */

$dbHost = getenv('DB_HOST') ?: 'localhost';
$dbUser = getenv('DB_USER') ?: '';
$dbPass = getenv('DB_PASS') ?: '';
$dbName = getenv('DB_NAME') ?: '';

$mysqli = @new mysqli($dbHost, $dbUser, $dbPass, $dbName);
if ($mysqli->connect_error) {
    error_log('Database connection failed.');
    http_response_code(500);
    exit('Internal server error.');
}

$username = (string) (filter_input(INPUT_GET, 'username', FILTER_UNSAFE_RAW) ?? '');
$password = (string) (filter_input(INPUT_GET, 'password', FILTER_UNSAFE_RAW) ?? '');
$userId = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);
$sort = (string) (filter_input(INPUT_GET, 'sort', FILTER_UNSAFE_RAW) ?? 'created_at');

// 1) Safe SELECT with bound string parameter
$stmt1 = $mysqli->prepare('SELECT id, username FROM users WHERE username = ?');
if ($stmt1) {
    $stmt1->bind_param('s', $username);
    $stmt1->execute();
    $result1 = $stmt1->get_result();
    $stmt1->close();
}

// 2) Safe authentication query with bound parameters
$stmt2 = $mysqli->prepare('SELECT id FROM users WHERE username = ? AND password = ?');
if ($stmt2) {
    $stmt2->bind_param('ss', $username, $password);
    $stmt2->execute();
    $result2 = $stmt2->get_result();
    $stmt2->close();
}

// 3) Safe numeric lookup (validated int + bound parameter)
if ($userId !== false && $userId !== null) {
    $stmt3 = $mysqli->prepare('SELECT id, account_name, status FROM accounts WHERE id = ?');
    if ($stmt3) {
        $stmt3->bind_param('i', $userId);
        $stmt3->execute();
        $result3 = $stmt3->get_result();
        $stmt3->close();
    }
}

// 4) Safe ORDER BY using strict allowlist for identifiers
$allowedSortColumns = ['created_at', 'title', 'id'];
if (!in_array($sort, $allowedSortColumns, true)) {
    $sort = 'created_at';
}
$sql4 = "SELECT id, title, created_at FROM posts ORDER BY {$sort}";
$result4 = $mysqli->query($sql4);

// 5) Safe UPDATE with bound parameter
$stmt5 = $mysqli->prepare('UPDATE profiles SET last_seen = NOW() WHERE username = ?');
if ($stmt5) {
    $stmt5->bind_param('s', $username);
    $stmt5->execute();
    $stmt5->close();
}

$mysqli->close();
