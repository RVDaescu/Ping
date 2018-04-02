<?php
    include 'ssh.php';
    function create_page($host, $path, $name, $user, $pass)
    {
        $res = get_reg_file($host, $path, $name, $user, $pass);
        
        $found = 0;     #number of times './hacpy -t' is found in 'ps ax | grep hacpy'
        $duts = [];     #list of devices found after './hacpy -t'; used for running test 

        $NAME = strtoupper($name); 

        $filename = "RegressionResults.txt".".$name";
 
        if ($name == 'hac1')
        {   echo "<h3>$NAME- Classic single device - HACPY Regression page <a href=\"#\" class=\"link\" onclick=\"window.open('img/hacauto1.png', 'popUpWindow', 'height=480,width=980')\">[Topology]</a> </h3>";}
        elseif ($name == 'hac2')
        {   echo "<h3> $NAME - HiOS single device - HACPY Regression page <a href=\"#\" class=\"link\" onclick=\"window.open('img/hacauto2.png', 'popUpWindow', 'height=980,width=980')\">[Topology]</a></h3>";}
        elseif ($name == 'hac5')
        {   echo "<h3> $NAME - Classic multi-device - HACPY Regression page <a href=\"#\" class=\"link\" onclick=\"window.open('img/hacauto5.png', 'popUpWindow', 'height=757,width=1097')\">[Topology]</a></h3>";}
        elseif ($name == 'hac4')
        {   echo "<h3> $NAME - HiOS multi-device - HACPY Regression page  <a href=\"#\" class=\"link\" onclick=\"window.open('img/hacauto4_mstp.png', 'popUpWindow','height=897, width=1560')\">[Layer2<a/> <a href=\"#\" class=\"link\" onclick=\"window.open('img/hacauto4_mcast.png', 'popUpWindow', 'height=757, width=1097')\">/Layer3]</a> </h3>";}
        else 
        {   echo "<h3> $NAME HACPY Regression page</h3>";}

        if (!$res and !file_exists($filename)) 
        {   echo "<h3 style=\"color:red;\">Remote regression file is missing or \"ps ax\" failed on $name; old local file is missing</h3>";
            return False;}
        elseif (!$res and file_exists($filename))
        {   echo "<h4 style=\"color:red;\">Remote regression file is missing - will use old local file. Check if path to remote regression file is correct</h4>";}
        else 
        {   foreach($res as $line)
            {   if (strpos($line, "./hacpy --regression_file") == true and strpos($line, rtrim($path,'/')) == true)
                {   $rr = "Regression is running";
                    $found +=1;
                }
                elseif (strpos($line, "./hacpy -t") !== false and !strpos($line, "grep --") !== false)
                {   $dut = preg_split("/[\s]+/", trim($line))[9]; 
                    $run_tst = preg_split("/[\s]+/", trim($line))[7];
                    array_push($duts, $dut); 
                }
            }
        }
        if ($found == 0) 
        {   $rr = 'Regression stopped!';}

        $duts = implode(',', $duts);    #joining all duts with ',' inbetween

        $content = file($filename);     #RegressionResults.txt file content read

        $tests = [];
           
        $reg_start = [];        #for regression reruns
        $failed_counter = 0;    #counter for failed tests for current regression
        $nr_run_tst = 0;        #number of ran tests at that moment for current regression
        $total_run_tst = 0;     #total number of tests that will be ran in the current regression

        foreach ($content as $key => $val) 
        {
            if (strpos($val, "P4") !== false || strpos($val, "P5") !== false)
            {   $line = preg_replace('/\s+/','',explode('-', $val));
                if ($line[1] == null)
                {   $line[1] = "Running";}
                elseif (!$line[2] == null)
                {   $line[1] = $line[1] . " - " . $line[2];}
                if ($line[1] == 'PASSED')
                {   $failed_counter = 0;}
                else
                {   $failed_counter += 1;}
            $tests[$line[0]] = [$line[1]];
            $nr_run_tst += 1;
            }
            elseif (strpos($val, "Regression run started") !== false)
            {   $failed_counter = 0;
                $nr_run_tst = 0;
            }
            if (strpos($val, "version") == true) 
            {   $version = $val;}
            if (strpos($val, "Regression run started") !== false and strpos($val, "tests") == false)
            {   array_push($reg_start, $val);}
            elseif (strpos($val, "Regression run started") !== false and strpos($val, "tests") !== false)
            {   array_push($reg_start, $val);
                $arr = explode(' ', $val);     
                $total_run_tst = array_slice($arr, -2, 1)[0];
            }
        }

    $start = $reg_start[0];
    if (count($reg_start) != 1)
    {   foreach ($reg_start as $key =>$line)
        {   if ($key == 1)
            {   $line = explode(' ', $line);
                $start = $start . ' and re-runs started on ' . implode(' ',array_slice($line, 5));
            }
            elseif ($key > 1 )
            {   $line = explode(' ', $line);
                $start = $start . ' and on ' . implode(' ',array_slice($line, 5));
            }
        }       
    }

    $passed = 0;    #counts number of tests that have passed
    $failed = 0;    #counts number of tests that are not passed nor running (failed, blocked, etc.)

    foreach ($tests as $test => $result)
    {   if (strpos($result[0], "PASSED") !== false)
        {   $passed += 1;}
        elseif (strpos($result[0], 'Running') !== false)
        {   continue;}
        elseif (strpos($result[0], "PASSED") == false)
        {   $failed += 1;}
    }

    if ($failed_counter >=5)
        {   echo "<h3 style=\"color:red;\">WARNING! $failed_counter consecutive tests have failed!</h3>";
            echo "<iframe width=\"0\" frameborder=\"0\" height=\"0\" onload=\"notifyMe('$NAME','$failed_counter')\"> </iframe>";
        }
    if ($nr_run_tst == 0) {echo "<h4>No test was found in regression file</h4>"; return False;}

    $wpc = '23px';

    if ($rr !== 'Regression is running')
    {   echo "<p style=\"color: red;\"><b>$rr</b></p>";}
    else
    {   $rr = $rr . " test $run_tst on device(s) $duts." .'<br />' ."Currently at $nr_run_tst out of $total_run_tst tests.";
        echo "<p style=\"color: red;\"><b>$rr</b></p>";
        $nr_run_tst = $nr_run_tst - 1;              #because of running test
        $pcr = $nr_run_tst/$total_run_tst*100;      #percent of finished tests
        $pcrn = 1/$total_run_tst*100;               #percent of running tests at the moment
        $pct = 100 - $pcr - $pcrn;                  #percent of left tests
        $remaining = $total_run_tst - $nr_run_tst - 1;
        echo "<div class=\"progress\" style=\"width:50%; height: $wpc;\">";
        echo "  <div class=\"progress-bar progress-bar-success\" role=\"progressbar\" style=\"width:$pcr%; vertical-align: middle; line-height: $wpc;\">";
        echo "    Done $nr_run_tst";
        echo "    </div>";
        echo "  <div class=\"progress-bar progress-bar-warning\" role=\"progressbar\" style=\"width:$pcrn%; vertical-align: middle; line-height: $wpc;\">";
        echo "    Running 1";
        echo "    </div>";
        echo "  <div class=\"progress-bar progress-bar-info\" role=\"progressbar\" style=\"width:$pct%; vertical-align: middle; line-height: $wpc;\" >";
        echo "    Remaining $remaining";
        echo "    </div>";
        echo "</div>";
    }
    echo "<p> $start </p>";
    echo "<p> $version </p>";

    $total = $failed + $passed;
    if ($passed !== 0)
    {   $pcf = number_format((float)($failed/$total), 2, '.', '')*100;}  #failed
    else 
    {   $pcf = 100;}
    $pcp = 100-$pcf;

    if ($passed == 0)
    {   echo "<p><b>No test has passed ($total)</b></p>";}
    elseif ($failed == 0)
    {   echo "<p><b>All the tests have passed ($total)</b></p>";}
    else
    {   echo "<p><b>$passed tests have passed, $failed have failed</b></p>";
        echo "<p><b>$pcf % failed of the total ($total)  tests ran</b></p>";
    } 

    echo "<div class=\"progress\" style=\"width:50%; height: $wpc;\">";
    echo "  <div class=\"progress-bar progress-bar-success\" role=\"progressbar\" style=\"width:$pcp%; vertical-align: middle; line-height: $wpc;\">";
    echo "    Passed - $pcp%";
    echo "  </div>";
    echo "  <div class=\"progress-bar progress-bar-danger\" role=\"progressbar\" style=\"width:$pcf%; vertical-align: middle; line-height: $wpc;\" >";
    echo "    Failed - $pcf%";
    echo "  </div>";
    echo "</div>";

    echo "<h4 style=\"color:blue;\" id=filtered.$name></h4>";
    echo "<form onkeyup=\"mySearch('$name', 'test.$name', 'status.$name', 'filtered.$name')\" method=\"post\">";
    echo "<input type=\"text\" id=\"test.$name\"  placeholder=\"Search for test..\" title=\"Put ! in front of text for negative search\">";

    echo "<input type=\"text\" id=\"status.$name\"  placeholder=\"Search for status..\" title=\"Put ! in front of text for negative search\">";
    echo "</form>";

    echo "<table id=\"$name\">";
    echo "<tr class=\"header\">";
    echo "<th>Test</th>";
    echo "<th>Status</th>";
    echo "</tr>";

#####Code for puttin running test on first row of table - not needed at the moment
#    foreach ($tests as $test => $result)
#    {   if ($result[0] == 'Running')
#        {   echo "<tr>";
#            echo "<td align=\"left\">$test</td>";
#            echo "<td align=\"center\" bgcolor=#1a53ff>$result[0] - $duts</td>";
#            echo "</tr>";
#        }
#    }

    foreach ($tests as $test => $result)
    {   if ($result[0] == "PASSED")
        {   echo "<tr>";
            echo "<td align=\"left\">$test</td>";
            echo "<td align=\"center\" bgcolor=#00FF7F>$result[0]</td>";
            echo "</tr>";
        }
        elseif ($result[0] == 'Running')
        {   echo "<tr>";
            echo "<td align=\"left\">$test</td>";
            echo "<td align=\"center\" bgcolor=#1a53ff>$result[0] - $duts</td>";
            echo "</tr>";
        }

        elseif ($result[0] !== "PASSED")
        {   echo "<tr>";
            echo "<td align=\"left\">$test</td>";
            echo "<td align=\"center\" bgcolor=\"#FF6347\">$result[0]</td>";
            echo "</tr>";
        }
    }
    echo "</table>";

    echo "<br />";
    echo "<br />";
    echo "<br />";
    }
?>
