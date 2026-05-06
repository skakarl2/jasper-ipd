<?php

declare(strict_types=1);

/*
 * Automatic fix invoked by IPDefender.
 * The agent is not allowed to create vulnerable code either accidentally or on purpose.
 */

/*
 * Safe PHP example corresponding to common CWE-89 scenarios.
 *
 * This file demonstrates secure handling for:
 * - filtering by id
 * - searching with LIKE
 * - filtering by email
 * - sorting with an allowlist
 */

$host = getenv('DB_HOST') ?: '127.0.0.1';
$dbName = getenv('DB_NAME') ?: 'demo_app';
$username = getenv('DB_USER') ?: 'demo_user';
$password = getenv('DB_PASSWORD');

if ($password === false || $password === '') {
    http_response_code(500);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Database password is not configured.'], JSON_PRETTY_PRINT);
    exit;
}

$pdo = new PDO(
    "mysql:host={$host};dbname={$dbName};charset=utf8mb4",
    $username,
    $password,
    [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]
);

$userIdRaw = $_GET['id'] ?? '0';
$searchRaw = $_GET['q'] ?? '';
$emailRaw = $_POST['email'] ?? '';
$sortRaw = $_GET['sort'] ?? 'name';

$userId = filter_var($userIdRaw, FILTER_VALIDATE_INT);
if ($userId === false) {
    $userId = 0;
}

$search = trim((string) $searchRaw);
$email = trim((string) $emailRaw);

$allowedSortColumns = [
    'name' => 'username',
    'created_at' => 'created_at',
    'id' => 'id',
];
$sortColumn = $allowedSortColumns[$sortRaw] ?? $allowedSortColumns['name'];

// Safe pattern 1: parameterized query for numeric lookup.
$stmtById = $pdo->prepare('SELECT id, username, email FROM users WHERE id = :id');
$stmtById->bindValue(':id', $userId, PDO::PARAM_INT);
$stmtById->execute();
$rowsById = $stmtById->fetchAll();

// Safe pattern 2: parameterized LIKE search.
$stmtSearch = $pdo->prepare('SELECT id, title FROM products WHERE title LIKE :search');
$stmtSearch->bindValue(':search', '%' . $search . '%', PDO::PARAM_STR);
$stmtSearch->execute();
$rowsSearch = $stmtSearch->fetchAll();

// Safe pattern 3: parameterized email lookup.
$stmtByEmail = $pdo->prepare('SELECT id, email, role FROM accounts WHERE email = :email');
$stmtByEmail->bindValue(':email', $email, PDO::PARAM_STR);
$stmtByEmail->execute();
$rowsByEmail = $stmtByEmail->fetchAll();

// Safe pattern 4: allowlist-based ORDER BY construction.
$sqlSorted = "SELECT id, username, created_at FROM users ORDER BY {$sortColumn}";
$stmtSorted = $pdo->query($sqlSorted);
$rowsSorted = $stmtSorted->fetchAll();

header('Content-Type: application/json');
echo json_encode(
    [
        'status' => 'secure example',
        'by_id' => $rowsById,
        'search' => $rowsSearch,
        'by_email' => $rowsByEmail,
        'sorted' => $rowsSorted,
    ],
    JSON_PRETTY_PRINT
);
