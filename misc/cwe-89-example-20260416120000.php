// WARNING: IP Defender detected 7 security issue(s)
// but could not automatically remediate them (reprompt LLM unreachable).
// Issues found:
//   - Hard-coded secret
//   - SQL Injection
//   - SQL Injection
//   - SQL Injection
//   - SQL Injection
//   - SQL Injection
//   - SQL Injection
//
// Please review and fix these issues manually before using this code.

<?php
/**
 * CWE-89: Improper Neutralization of Special Elements used in an SQL Command
 * ('SQL Injection') — Annotated Examples for Security Research
 *
 * This file demonstrates common SQL injection vulnerability patterns.
 * FOR EDUCATIONAL / SECURITY RESEARCH PURPOSES ONLY.
 * Do NOT deploy any of this code in a production environment.
 *
 * Reference: https://cwe.mitre.org/data/definitions/89.html
 * Generated: 2026-04-16 12:00:00
 */

// ---------------------------------------------------------------------------
// EXAMPLE 1: Classic String Concatenation in a SELECT Query
// CWE-89 Pattern: User input is directly concatenated into SQL without sanitization.
// ---------------------------------------------------------------------------

// Simulated database connection (mysqli)
$conn = new mysqli("localhost", "db_user", "db_pass", "app_db");

// VULNERABLE: $_GET['username'] is never validated or escaped.
// Attacker input: ' OR '1'='1 -- 
// Resulting query: SELECT * FROM users WHERE username = '' OR '1'='1' --'
$username = $_GET['username'];                         // [CWE-89] Untrusted source
$query = "SELECT * FROM users WHERE username = '" . $username . "'"; // [CWE-89] Direct concatenation
$result = $conn->query($query);                        // [CWE-89] Executed with injected SQL


// ---------------------------------------------------------------------------
// EXAMPLE 2: Injection via POST Body in a Login Form
// CWE-89 Pattern: Credentials passed directly into query, enabling auth bypass.
// ---------------------------------------------------------------------------

// VULNERABLE: Classic login bypass via SQL injection.
// Attacker input — username: admin'-- , password: anything
// Resulting query: SELECT * FROM users WHERE user='admin'--' AND pass='...'
$user = $_POST['user'];                                // [CWE-89] Untrusted source
$pass = $_POST['pass'];                                // [CWE-89] Untrusted source
$login_query = "SELECT * FROM users WHERE user='" . $user . "' AND pass='" . $pass . "'";
$login_result = $conn->query($login_query);            // [CWE-89] Auth bypass possible


// ---------------------------------------------------------------------------
// EXAMPLE 3: Second-Order SQL Injection
// CWE-89 Pattern: Malicious data stored safely, then unsafely reused later.
// ---------------------------------------------------------------------------

// Step A — data is stored (appears safe at this point)
$safe_insert = $conn->prepare("INSERT INTO profiles (bio) VALUES (?)");
$safe_insert->bind_param("s", $_POST['bio']);
$safe_insert->execute();

// Step B — [CWE-89] The stored value is later retrieved and re-injected unsafely.
$stored_bio_result = $conn->query("SELECT bio FROM profiles WHERE id=1");
$row = $stored_bio_result->fetch_assoc();
$bio = $row['bio'];                                    // Trusted incorrectly — came from user originally
$second_order_query = "UPDATE reports SET summary='" . $bio . "' WHERE id=1"; // [CWE-89] Second-order injection
$conn->query($second_order_query);


// ---------------------------------------------------------------------------
// EXAMPLE 4: Injection in ORDER BY Clause
// CWE-89 Pattern: Parameterized queries cannot bind column names/ORDER BY,
//                 so developers often fall back to concatenation here.
// ---------------------------------------------------------------------------

// VULNERABLE: ORDER BY clause built from unsanitized user input.
// Attacker input: id DESC; DROP TABLE users--
$order_col = $_GET['sort'];                            // [CWE-89] Untrusted source
$order_query = "SELECT id, name FROM products ORDER BY " . $order_col; // [CWE-89] No whitelist check
$conn->query($order_query);


// ---------------------------------------------------------------------------
// EXAMPLE 5: Injection via Cookie Value
// CWE-89 Pattern: HTTP cookies treated as trusted input.
// ---------------------------------------------------------------------------

// VULNERABLE: Session/cookie value used directly in query.
// Attacker can forge the cookie: ' UNION SELECT username,password FROM users--
$session_id = $_COOKIE['session_id'];                  // [CWE-89] Untrusted source (cookie)
$session_query = "SELECT user_id FROM sessions WHERE token='" . $session_id . "'";
$conn->query($session_query);                          // [CWE-89] UNION-based injection possible


// ---------------------------------------------------------------------------
// EXAMPLE 6: Integer Injection (Type Confusion)
// CWE-89 Pattern: Assuming numeric input is safe without explicit casting.
// ---------------------------------------------------------------------------

// VULNERABLE: Even "numeric" GET params can carry injections if not cast.
// Attacker input: 1 OR 1=1
$product_id = $_GET['id'];                             // [CWE-89] No intval() or (int) cast
$product_query = "SELECT * FROM products WHERE id=" . $product_id; // [CWE-89] No type enforcement
$conn->query($product_query);


// ---------------------------------------------------------------------------
// EXAMPLE 7: Stored Procedure with Dynamic SQL (Inside Procedure)
// CWE-89 Pattern: Even stored procedures can be vulnerable when they
//                 build dynamic SQL strings internally.
// ---------------------------------------------------------------------------

// VULNERABLE: Stored proc called safely, but internally does EXEC/sp_executesql
// on concatenated input — the vulnerability lives inside the DB procedure.
// Shown here as the PHP call that passes unsanitized data to the proc.
$search_term = $_POST['search'];                       // [CWE-89] Untrusted source
$proc_query = "CALL search_products('" . $search_term . "')"; // [CWE-89] Injection into proc args
$conn->query($proc_query);


// ---------------------------------------------------------------------------
// REMEDIATION NOTES (what secure code looks like — for contrast)
// ---------------------------------------------------------------------------

/*
 * SECURE PATTERN — Parameterized prepared statement (mysqli):
 *
 *   $stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
 *   $stmt->bind_param("s", $_GET['username']);   // Input bound safely
 *   $stmt->execute();
 *
 * SECURE PATTERN — PDO with named placeholder:
 *
 *   $pdo = new PDO("mysql:host=localhost;dbname=app_db", "user", "pass");
 *   $stmt = $pdo->prepare("SELECT * FROM users WHERE username = :username");
 *   $stmt->execute([':username' => $_GET['username']]);
 *
 * SECURE PATTERN — ORDER BY with allowlist:
 *
 *   $allowed = ['id', 'name', 'created_at'];
 *   $col = in_array($_GET['sort'], $allowed) ? $_GET['sort'] : 'id';
 *   $query = "SELECT * FROM products ORDER BY " . $col;
 *
 * KEY PRINCIPLES:
 *   1. Never concatenate untrusted data into SQL strings.
 *   2. Use prepared statements / parameterized queries exclusively.
 *   3. Apply allowlists for values that cannot be parameterized (column names).
 *   4. Cast numeric inputs explicitly: (int)$_GET['id']
 *   5. Treat ALL external sources as untrusted: GET, POST, COOKIE, SERVER, headers.
 */
