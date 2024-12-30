<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Gallery</title>
    <style>
        body {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        .card {
            width: calc(20% - 10px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
            background-color: #fff;
        }
        .card img {
            width: 100%;
            height: auto;
        }
    </style>
</head>
<body>

    <?php
    for ($i = 1; $i <= 50; $i++) {
        echo "<div class='card'>";
        echo "<img src='images/card{$i}.jpg' alt='Card {$i}'>";
        echo "</div>";
    }
    ?>

</body>
</html>
