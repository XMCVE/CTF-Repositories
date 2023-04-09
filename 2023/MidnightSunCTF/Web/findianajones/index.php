<?php
    ini_set("allow_url_fopen", 0);
    ini_set("allow_url_include", 0);
    session_start();

    if(isset($_GET['cmd'])){
        $_GET['cmd'](strval($_GET['path'])); # One argument for babies
        echo "Still no shell? ".$_SESSION['attempts']." tries and counting :-)<br>\n";
        $_SESSION['attempts'] = (isset($_SESSION['attempts']) ? $_SESSION['attempts']+1 : $_SESSION['attempts']=1);

        if(isset($_GET['hiddenschmidden'])){
            $descriptorspec = array(
                0 => array("pipe", "r"),
                1 => array("pipe", "w")
             );
            $proc = proc_open(['timeout','0.5','chmod','+x',strval($_GET['path'])], $descriptorspec, $pipes);
            proc_close($proc);
            $proc = proc_open(['timeout','0.5',strval($_GET['path'])], $descriptorspec, $pipes2); #No argument for haxors
            echo @stream_get_contents($pipes2[1]);
            proc_close($proc);
        }
        die();
    }

?>