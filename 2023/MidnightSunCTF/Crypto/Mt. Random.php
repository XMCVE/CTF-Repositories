<?php
session_start();

$flag = "";

function flag_to_numbers($flag) {
    $numbers = [];
    foreach (str_split($flag) as $char) {
        $numbers[] = ord($char);
    }
    return $numbers;
}

function non_continuous_sample($min, $max, $gap_start, $gap_end) {
    $rand_num = mt_rand($min, $max - ($gap_end - $gap_start));
    if ($rand_num >= $gap_start) {
        $rand_num += ($gap_end - $gap_start);
    }
    return $rand_num;
}

if(!str_starts_with($flag, "midnight{")){
    echo "Come back later.\n";
    exit();
}

$flag_numbers = flag_to_numbers($flag);

if (isset($_GET['generate_samples'])) {
    header('Content-Type: application/json');

    // Maybe we can recover these constants 
    $min = 0;
    $max = 0;
    $gap_start = 0;
    $gap_end = 0;
    $seed = mt_rand(0, 10000); // Varying seed
    $samples = [];

    foreach ($flag_numbers as $number) {
        mt_srand($seed + $number);
        $samples[] = non_continuous_sample($min, $max, $gap_start, $gap_end);
    }

    echo json_encode(["samples" => $samples]);
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mt. Random</title>
</head>
<body>
    <h1>Hiking Guide</h1>
    <p>This mountain is boring, I'm going to sample alot of seeds!</p>
    <a href="?generate_samples=1">Get a new sample</a>
</body>
</html>
