<?php
error_reporting(0);
ini_set('open_basedir', __DIR__.":/tmp");
define("FUNC_LIST", get_defined_functions());

class fumo_backdoor {
    public $path = null;
    public $argv = null;
    public $func = null;
    public $class = null;
    
    public function __sleep() {
        if (
            file_exists($this->path) && 
            preg_match_all('/[flag]/m', $this->path) === 0
        ) {
            readfile($this->path);
        }
    }

    public function __wakeup() {
        $func = $this->func;
        if (
            is_string($func) && 
            in_array($func, FUNC_LIST["internal"])
        ) {
            call_user_func($func);
        } else {
            $argv = $this->argv;
            $class = $this->class;
            
            new $class($argv);
        }
    }
}

$cmd = $_REQUEST['cmd'];
$data = $_REQUEST['data'];

switch ($cmd) {
    case 'unserialze':
        unserialize($data);
        break;
    
    case 'rm':
        system("rm -rf /tmp 2>/dev/null");
        break;
    
    default:
        highlight_file(__FILE__);
        break;
}
