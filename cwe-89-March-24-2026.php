<?php
// ============================================================================
// AUTOMATIC FIX BY IPDEFENDER
// This file was automatically corrected. The agent is not allowed to create
// vulnerable code either accidentally or on purpose.
// ============================================================================
//
// CWE-89: Improper Neutralization of Special Elements used in an SQL Command
//         ('SQL Injection')
//
// This file demonstrates the SECURE (remediated) version of CWE-89.
// The original vulnerable pattern uses unsanitized user input directly in an
// SQL query string. The fix below uses prepared statements with parameterized
// queries to prevent SQL injection.
//

// --- Database connection using environment variables (no hard-coded secrets) ---
$servername = getenv('DB_HOST') ?: 'localhost';
$username   = getenv('DB_USER') ?: 'default_user';
$password   = getenv('DB_PASS') ?: '';
$dbname     = getenv('DB_NAME') ?: 'testdb';

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    // Log the error internally; do not expose details to the end user (CWE-200)
    error_log("Database connection failed: " . $conn->connect_error);
    die("An internal error occurred. Please try again later.");
}

// -------------------------------------------------------------------------
// VULNERABLE PATTERN (DO NOT USE — shown only as a comment for reference):
//
//   $user_input = $_GET['id'];
//   $sql = "SELECT * FROM users WHERE id = '$user_input'";
//   $result = $conn->query($sql);
//
// An attacker could supply:  ?id=' OR '1'='1
// which would return all rows, or worse, manipulate / exfiltrate data.
// -------------------------------------------------------------------------

// SECURE PATTERN: Prepared statement with parameterized query
$user_input = $_GET['id'] ?? null;

if ($user_input === null) {
    die("Missing required parameter: id");
}

// Validate that the input is a positive integer (defense in depth)
if (!ctype_digit($user_input)) {
    die("Invalid parameter: id must be a positive integer.");
}

$stmt = $conn->prepare("SELECT id, name FROM users WHERE id = ?");
if ($stmt === false) {
    error_log("Prepare failed: " . $conn->error);
    die("An internal error occurred.");
}

$stmt->bind_param("i", $user_input);  // "i" = integer type
$stmt->execute();

$result = $stmt->get_result();

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        echo "id: " . htmlspecialchars($row["id"], ENT_QUOTES, 'UTF-8')
           . " - Name: " . htmlspecialchars($row["name"], ENT_QUOTES, 'UTF-8')
           . "<br>";
    }
} else {
    echo "0 results";
}

$stmt->close();
$conn->close();
?>
