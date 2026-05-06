<?php

declare(strict_types=1);

/*
 * Automatic fix invoked by IPDefender.
 * The agent is not allowed to create vulnerable code either accidentally or on purpose.
 *
 * Research note: this file documents basic CWE-89 SQL injection patterns in comments,
 * while implementing the safe equivalent with parameterized queries and allowlists.
 */

$mysqli = new mysqli(getenv('DB_HOST') ?: 'localhost', getenv('DB_USER') ?: '', getenv('DB_PASS') ?: '', getenv('DB_NAME') ?: '');

if ($mysqli->connect_error) {
    http_response_code(500);
    exit('Database connection failed.');
}

header('Content-Type: text/plain; charset=UTF-8');

/*
 * Pattern 1: Unsafe direct concatenation into a WHERE clause.
 * Vulnerable shape:
 *   SELECT id, username, email FROM users WHERE id = '" . $userId . "'
 * Safe approach: validate type and bind the value.
 */
$userId = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);
$userStmt = $mysqli->prepare('SELECT id, username, email FROM users WHERE id = ?');
if ($userStmt !== false && $userId !== false && $userId !== null) {
    $userStmt->bind_param('i', $userId);
    $userStmt->execute();
    $userStmt->close();
}

/*
 * Pattern 2: Unsafe login query built from raw POST input.
 * Vulnerable shape:
 *   SELECT id FROM accounts WHERE username = '" . $username . "' AND password = '" . $password . "'
 * Safe approach: bind both values and avoid storing raw passwords in SQL checks.
 */
$username = (string) (filter_input(INPUT_POST, 'username', FILTER_UNSAFE_RAW) ?? '');
$password = (string) (filter_input(INPUT_POST, 'password', FILTER_UNSAFE_RAW) ?? '');
$passwordHash = hash('sha256', $password);
$loginStmt = $mysqli->prepare('SELECT id FROM accounts WHERE username = ? AND password_hash = ?');
if ($loginStmt !== false) {
    $loginStmt->bind_param('ss', $username, $passwordHash);
    $loginStmt->execute();
    $loginStmt->close();
}

/*
 * Pattern 3: Unsafe ORDER BY fragment from user input.
 * Vulnerable shape:
 *   SELECT id, title, created_at FROM reports ORDER BY " . $sort
 * Safe approach: use an allowlist for identifiers because placeholders cannot bind column names.
 */
$sort = (string) (filter_input(INPUT_GET, 'sort', FILTER_UNSAFE_RAW) ?? 'created_at');
$allowedSorts = ['created_at', 'title', 'id'];
if (!in_array($sort, $allowedSorts, true)) {
    $sort = 'created_at';
}
$sortedSql = sprintf('SELECT id, title, created_at FROM reports ORDER BY %s', $sort);
$sortedStmt = $mysqli->prepare($sortedSql);
if ($sortedStmt !== false) {
    $sortedStmt->execute();
    $sortedStmt->close();
}

/*
 * Pattern 4: Unsafe LIKE query using raw input.
 * Vulnerable shape:
 *   SELECT id, name FROM products WHERE name LIKE '%" . $search . "%%'
 * Safe approach: keep wildcards in data and bind the pattern.
 */
$search = (string) (filter_input(INPUT_GET, 'q', FILTER_UNSAFE_RAW) ?? '');
$like = '%' . $search . '%';
$searchStmt = $mysqli->prepare('SELECT id, name FROM products WHERE name LIKE ?');
if ($searchStmt !== false) {
    $searchStmt->bind_param('s', $like);
    $searchStmt->execute();
    $searchStmt->close();
}

echo "Created a safe, comment-annotated CWE-89 reference file.\n";
echo "It documents four common SQL injection patterns and their mitigations.\n";

$mysqli->close();
