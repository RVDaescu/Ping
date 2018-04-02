<?php
/* Function for copying regression results and returning ps ax | grep hacpy output */
function get_reg_file($host, $path, $name, $user, $pass)
{
    
    $host = $host;
    $port = 22;
    if (!$user)
    {   $username = base64_decode('cm9vdA==');}
    else
    {   $username = $user;}
    if (!$pass)
    {   $password = base64_decode('aGFjI21hbg==');}
    else
    {    $password = $pass;}
 
    $remoteDir = $path;
    $localDir = getcwd();

#    if (!function_exists("ssh2_connect"))
#    {   echo 'Function ssh2_connect not found, you cannot use ssh2 here';
#        return False;}

    if (!$connection = ssh2_connect($host, $port))
    {   echo "Unable to connect to $host <br />";
        return False;}


    if (!ssh2_auth_password($connection, $username, $password))
    {   echo "Unable to authenticate to $host. <br />";
        return False;}

    /*fetching ps ax output */
    $stream = ssh2_exec($connection, "ps ax | grep hacpy");
    #$stream = ssh2_fetch_stream($stream);
    $errorStream = ssh2_fetch_stream($stream, SSH2_STREAM_STDERR);
    
    stream_set_blocking($errorStream, true);
    stream_set_blocking($stream, true);
    $output = [];

    /* this method return every line of the output in a list/array */
    while ($line = fgets($stream)) 
    {   array_push($output, $line);        
    }

#    $output = stream_get_contents($stream);
    $error = stream_get_contents($errorStream);

    fclose($errorStream);
    fclose($stream);

    if (!$stream = ssh2_sftp($connection))
    {   echo 'Unable to create a stream. <br />';
        return False;
    }

    if (!$dir = opendir("ssh2.sftp://{$stream}{$remoteDir}"))
    {   echo 'Could not open the directory <br />';
        return False;
    }
    
    $file = 'RegressionResults.txt';
#    echo "Copying file: $file from $name <br />";
    if (!$remote = @fopen("ssh2.sftp://{$stream}/{$remoteDir}{$file}", 'r'))
    {   #echo "<h3>Unable to open remote file: $file or file not present on $name in $remoteDir<br /></h3>";
        return False;
    }

    if (!$local = @fopen($localDir . "/" . $file . ".$name", 'w'))
    {   echo "Unable to create local file: $file.$name on $name <br />";
        return False;
    }
    $read = 0;
    $filesize = filesize("ssh2.sftp://{$stream}/{$remoteDir}{$file}");
    while ($read < $filesize && ($buffer = fread($remote, $filesize - $read)))
    {
        $read += strlen($buffer);
        if (fwrite($local, $buffer) === FALSE)
        {
            echo "Unable to write to local file: $file on $name<br />";
            return False;
        }
    }
    fclose($local);
    fclose($remote);

    if (!$error) 
    {   return $output;}
    else
    {   echo $error;
        return False;
    }
}
?>
