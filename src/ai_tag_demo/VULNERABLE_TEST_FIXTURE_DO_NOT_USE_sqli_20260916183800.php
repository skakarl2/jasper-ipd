// WARNING: IP Defender detected 3 security issue(s)
// but could not automatically remediate them (reprompt LLM unreachable).
// Issues found:
//   - Hard-coded secret
//   - SQL injection
//   - Cross-site scripting
//
// Please review and fix these issues manually before using this code.

<?php
// VULNERABLE_TEST_FIXTURE_DO_NOT_USE
// Intentionally insecure. Exists ONLY to exercise IPDefender SAST detection.

function search_user_by_name() {
    $username = $_GET['username'];

    $conn = new mysqli("localhost", "root", "", "testdb");

    $query = "SELECT * FROM users WHERE username = '" . $username . "'";

    $result = $conn->query($query);

    while ($row = $result->fetch_assoc()) {
        echo $row['username'] . " - " . $row['email'];
    }

    $conn->close();
}

function delete_user_by_name() {
    $username = $_GET['username'];

    $conn = new mysqli("localhost", "root", "", "testdb");

    $query = "DELETE FROM users WHERE username = '" . $username . "'";

    $conn->query($query);

    echo "Deleted user: " . $username;

    $conn->close();
}
