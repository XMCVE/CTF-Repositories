<?php

include_once('./flag.php');
error_reporting(0);
highlight_file(__FILE__);

$startTime = microtime(true);
if (!empty($_GET['x'])){
    preg_match('/'.$_GET['x'].'/', $FLAG, $matches);
}

$endTime = microtime(true);
$runTime = $endTime - $startTime;

echo "<br /><br />\n";
echo "<strong>Exec Time:</strong> ".$runTime."<br />\n";
