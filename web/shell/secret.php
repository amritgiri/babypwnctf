<?php
// Web Shell Challenge - Restrict Commands to /var/www/html/secret Only
// Set working directory to /var/www/html/secret
$base_dir = '/var/www/html/secret';
chdir($base_dir);

// Logging function for executed commands
function log_command($cmd) {
    $logfile = $base_dir . '/command_log.txt';
    $log_entry = date('Y-m-d H:i:s') . " - Command executed: " . $cmd . PHP_EOL;
    file_put_contents($logfile, $log_entry, FILE_APPEND);
}

// Initialize output variable
$output = "";

// Handle command execution
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['cmd'])) {
    $cmd = $_POST['cmd'];

    // Base commands allowed
    $allowed_commands = ['ls', 'pwd', 'date', 'uname', 'ices8yz3r08y73'];

    // Check if the command starts with an allowed base command
    $is_allowed = false;
    foreach ($allowed_commands as $allowed) {
        if (strpos($cmd, $allowed) === 0) {
            $is_allowed = true;
            break;
        }
    }

    // Reject if command is not in the allowed list
    if (!$is_allowed) {
        $output = "Command not allowed.";
        goto display_form;
    }

    // Prevent access to directories outside $base_dir
    if (preg_match('/(\.\.|\/var|\/etc|~|\/root|\/bin|\/usr|\/home|\/)/i', $cmd)) {
        $output = "Access to the specified path is not allowed.";
        goto display_form;
    }

    if (strpos($cmd, 'ices8yz3r08y73') === 0) {
        $cmd = str_replace('ices8yz3r08y73', 'cat', $cmd);
    }

    // Log and execute the command
    log_command($cmd);
    $output = "<pre>" . shell_exec($cmd) . "</pre>";
}

display_form:
// Display the form and output
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Shell Challenge</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f9;
        }
        .container {
            max-width: 600px;
            margin: auto;
            padding: 20px;
            background: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        input[type="text"] {
            width: 80%;
            padding: 10px;
            margin-right: 10px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .output {
            margin-top: 20px;
            padding: 10px;
            background: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Web Shell Challenge</h2>
        <form method="post">
            <input type="text" name="cmd" placeholder="Enter your command" required>
            <input type="submit" value="Execute">
        </form>
        <?php if ($output): ?>
        <div class="output">
            <h3>Command Output:</h3>
            <?php echo $output; ?>
        </div>
        <?php endif; ?>
    </div>
</body>
</html>
