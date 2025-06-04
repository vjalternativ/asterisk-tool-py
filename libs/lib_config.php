<?php

class lib_config
{

    private static $instance = null;

    private static $configpath;

    private $config;

    public static function setConfigPath($path)
    {
        self::$configpath = $path;
    }

    function __construct()
    {
        $configPath = self::$configpath;
        $dir = __DIR__;
        $fwbasepath = str_replace("libs", "", $dir);
        if (isset($_SERVER['argv'])) {
            if (substr($_SERVER['SCRIPT_FILENAME'], 0, 1) == "/") {
                $dir = substr($_SERVER['SCRIPT_FILENAME'], 0, strrpos($_SERVER['SCRIPT_FILENAME'], "/")) . '/';
            } else {
                $path = $_SERVER['PWD'] . '/' . $_SERVER['SCRIPT_FILENAME'];
                $dir = substr($path, 0, strrpos($path, "/")) . '/';
            }
        } else if (isset($_SERVER['SCRIPT_FILENAME'])) {
            $dir = substr($_SERVER['SCRIPT_FILENAME'], 0, strrpos($_SERVER['SCRIPT_FILENAME'], "/")) . '/';
        }

        if ($configPath) {
            $dir = $configPath . '/';
        }
        $this->config['fwbasepath'] = $fwbasepath;
        $this->config['basepath'] = $dir;
        if (isset($_SERVER['DOCUMENT_ROOT']) && $_SERVER['DOCUMENT_ROOT']) {

            $httpProtocol = "http";
            if (isset($_SERVER['HTTPS'])) {
                $httpProtocol = "https";
            }
            $prefix = $httpProtocol . "://" . $_SERVER["HTTP_HOST"];
            if (! ($_SERVER['SERVER_PORT'] == "80" || $_SERVER['SERVER_PORT'] == "443")) {
                // $prefix .= ":" . $_SERVER['SERVER_PORT'];
            }
            $docRoot = $_SERVER['DOCUMENT_ROOT'];
            $dir = $dir;
            $projectpath = str_replace($docRoot, "", $dir);
            $this->config['urlbasepath'] = $projectpath;
            $this->config['baseurl'] = $prefix . $this->config['urlbasepath'];

            if (substr($this->config['fwbasepath'], 0, strlen($docRoot)) == $docRoot) {
                $projectpath = str_replace($docRoot, "", $this->config['fwbasepath']);
            } else {
                $projectpath .= "spider-php/";
            }

            $this->config['fwurlbasepath'] = $projectpath;
            $this->config['fwbaseurl'] = $prefix . $this->config['fwurlbasepath'];
        }

        global $config;
        if (file_exists($dir . 'config.php')) {
            if (! isset($_GET['module']) && isset($_SERVER['argv']) && file_exists($dir . "cliconfig.php")) {
                global $cliconfig;
                require_once $dir . 'cliconfig.php';
                $clipath = substr($dir, 0, - 1);
                $_SERVER['HTTP_HOST'] = isset($cliconfig[$clipath]['host']) ? $cliconfig[$clipath]['host'] : "localhost";
            }
            require_once $dir . 'config.php';
            unset($config['fwbasepath']);
            unset($config['basepath']);
            unset($config['urlbasepath']);
            unset($config['fwurlbasepath']);

            if (isset($_SERVER['DOCUMENT_ROOT']) && $_SERVER['DOCUMENT_ROOT']) {
                unset($config['baseurl']);
                unset($config['fwbaseurl']);
            }
            $this->config = array_merge($this->config, $config);
            $this->config['display_errors'] = isset($this->config['display_errors']) ? $this->config['display_errors'] : false;
            ini_set("display_errors", $this->config['display_errors']);
            $this->config['resource_alias']['backend'] = isset($this->config['resource_alias']['backend']) ? $this->config['resource_alias']['backend'] : 'backend';
            $this->config['defaultlang'] = isset($config['defaultlang']) ? $config['defaultlang'] : "en_us";
            $this->config['init_default_modules'] = isset($config['init_default_modules']) ? $config['init_default_modules'] : "true";
        } else {
            // echo $dir . "config.php file not exist" . PHP_EOL;
            // throw new \ErrorException($dir . " config.php not exist");
        }
    }

    static function getInstance()
    {
        if (self::$instance == null) {
            self::$instance = new lib_config();
        }
        return self::$instance;
    }

    function get($key)
    {
        return isset($this->config[$key]) ? $this->config[$key] : false;
    }

    function getConfig()
    {
        return $this->config;
    }
}
?>