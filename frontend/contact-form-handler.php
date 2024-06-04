<?php
// Define the email settings
$to_email = 'morningdhansen@gmail.com';
$subject = 'Queen of the Yard Contact Form';

// Check if the form has been submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get the form data
    $name = $_POST['name'];
    $email = $_POST['email'];
    $message = $_POST['message'];

    // Validate the form data
    if (!empty($name) && !empty($email) && !empty($message)) {
        // Send the email
        $headers = 'From: ' . $email . "\r\n";
        $headers .= 'Reply-To: ' . $email . "\r\n";
        $headers .= 'Content-Type: text/plain; charset=UTF-8';
        $body = "From: $name\n\n$message";
        mail($to_email, $subject, $body, $headers);

        // Display a success message
        echo 'Thank you for submitting your comment!';
    } else {
        // Display an error message
        echo 'Please fill in all required fields.';
    }
}
