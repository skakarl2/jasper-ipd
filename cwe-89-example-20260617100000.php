<?php
/*
 * Automatic fix invoked by IPDefender: the agent is not allowed to create vulnerable code
 * either accidentally or on purpose.
 */

/**
 * CWE-89 educational reference (non-exploitable).
 *
 * This file annotates common SQL injection anti-patterns as comments only,
 * and demonstrates secure equivalents with prepared statements.
 *
 * NOTE: The vulnerable examples are intentionally non-executable comments.
 */

mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$host = getenv('DB_HOST') ?: '127.0.0.1';
$user = getenv('DB_USER') ?: '';
$pass = getenv('DB_PASS') ?: '';
$name = getenv('DB_NAME') ?: '';

$db = new mysqli($host, $user, $pass, $name);
$db->set_charset('utf8mb4');

// -------------------------------------------------------------
// Pattern A: String concatenation in WHERE clauses (CWE-89)
// Vulnerable shape (comment only):
//   $sql = "SELECT * FROM users WHERE username = '" . $_GET['u'] . "'";
// Secure shape below: prepared statement with bound parameter.
// -------------------------------------------------------------
$username = isset($_GET['u']) ? (string)$_GET['u'] : '';
$stmtA = $db->prepare('SELECT id, username FROM users WHERE username = ?');
$stmtA->bind_param('s', $username);
$stmtA->execute();
$resA = $stmtA->get_result();

// -------------------------------------------------------------
// Pattern B: Authentication query interpolation (CWE-89)
// Vulnerable shape (comment only):
//   $sql = "SELECT id FROM accounts WHERE email='" . $e . "' AND pass='" . $p . "'";
// Secure shape below: parameterized query.
// -------------------------------------------------------------
$email = isset($_POST['email']) ? (string)$_POST['email'] : '';
$passInput = isset($_POST['password']) ? (string)$_POST['password'] : '';
$stmtB = $db->prepare('SELECT id FROM accounts WHERE email = ? AND password = ?');
$stmtB->bind_param('ss', $email, $passInput);
$stmtB->execute();
$resB = $stmtB->get_result();

// -------------------------------------------------------------
// Pattern C: Numeric parameter interpolation (CWE-89)
// Vulnerable shape (comment only):
//   $sql = "SELECT * FROM orders WHERE id = " . $_GET['id'];
// Secure shape below: cast + bind integer parameter.
// -------------------------------------------------------------
$orderId = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$stmtC = $db->prepare('SELECT id, amount FROM orders WHERE id = ?');
$stmtC->bind_param('i', $orderId);
$stmtC->execute();
$resC = $stmtC->get_result();

// -------------------------------------------------------------
// Pattern D: Dynamic ORDER BY input (CWE-89-like misuse)
// Vulnerable shape (comment only):
//   $sql = "SELECT id, amount FROM payments ORDER BY " . $_GET['sort'];
// Secure shape below: fixed query variants selected via strict allow-list.
// -------------------------------------------------------------
$sortInput = isset($_GET['sort']) ? (string)$_GET['sort'] : 'id';
switch ($sortInput) {
    case 'amount':
        $sqlD = 'SELECT id, amount FROM payments ORDER BY amount';
        break;
    case 'created_at':
        $sqlD = 'SELECT id, amount FROM payments ORDER BY created_at';
        break;
    default:
        $sqlD = 'SELECT id, amount FROM payments ORDER BY id';
        break;
}
$resD = $db->query($sqlD);

// -------------------------------------------------------------
// Pattern E: LIKE filter interpolation (CWE-89)
// Vulnerable shape (comment only):
//   $sql = "SELECT * FROM docs WHERE title LIKE '%" . $_GET['q'] . "%'";
// Secure shape below: bind the wildcard value.
// -------------------------------------------------------------
$q = isset($_GET['q']) ? (string)$_GET['q'] : '';
$needle = '%' . $q . '%';
$stmtE = $db->prepare('SELECT id, title FROM documents WHERE title LIKE ?');
$stmtE->bind_param('s', $needle);
$stmtE->execute();
$resE = $stmtE->get_result();

echo 'CWE-89 annotation file generated with safe executable examples only.';

$stmtA->close();
$stmtB->close();
$stmtC->close();
$stmtE->close();
$db->close();
