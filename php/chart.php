<?php
    $query = "SELECT * FROM `camera`";
    #binary可區分英文大小寫 若用=或LIKE，則abcd會等於ABCD

    if ( !( $database = mysqli_connect( "localhost", "1073320", "" ) ) )			#( "主機", "使用者", "密碼" )
        die( "Could not connect to database </body></html>" );
    if ( !mysqli_select_db($database,"iot" ) )				#1073320改成資料庫的名稱
        die( "Could not open database </body></html>" );
    if ( !( $result = mysqli_query($database, $query) ) )
    {
        print( "<p>Could not execute query!</p>" );
        die( mysqli_error() . "</body></html>" );
    }
    
    $maxTime = 0;
    $r = 0;
    while($row = $result->fetch_assoc())		#得到某筆資料的name和email
    {
        $name[$r] = $row['name'];
        $time[$r] = $row['count'];
        if($time[$r] > $maxTime)
            $maxTime = $time[$r];
        $r++;
    }
?>
<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>F^2</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>	
        <link href = "../../maker/vendors/bootstrap/dist/css/bootstrap.min.css">
        <link href="../../maker/vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
        <link href="../../maker/vendors/nprogress/nprogress.css" rel="stylesheet">
        <link href="../../maker/vendors/malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.min.css" rel="stylesheet"/>
    
        <link href="../../maker/build/css/custom.min.css" rel="stylesheet">
        <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
        <style>
            .outer 
			{
                position: relative; 
            }
            .inner 
			{
                background-color: #d5e1a3;
                position: absolute;  
                top: 50%;           
                transform: translateY(-50%);   
            }
        </style>
        <script>
            function start()
            {
                var data = [
                    {
                        x: [
                            <?php
                                for($i = 0; $i < count($time); $i++)
                                {
                                    echo '"'.$name[$i].'"';
                                    if($i < count($time) - 1)
                                        echo ",";
                                }
                            ?>
                        ],
                        y: [
                            <?php
                                for($i = 0; $i < count($time); $i++)
                                {
                                    echo '"'.$time[$i].'"';
                                    if($i < count($time) - 1)
                                        echo ",";
                                }
                            ?>
                        ],
                        marker:{
                            color: [
                                <?php
                                    for($i = 0; $i < count($time); $i++)
                                    {
                                        if($time[$i] == $maxTime)
                                            echo '"rgba(222,45,38,0.8)"';
                                        else
                                            echo '"rgba(204,204,204,1)"';
                                        if($i < count($time) - 1)
                                            echo ",";
                                    }
                                ?>
                            ]
                        },
                        type: 'bar'
                    }
                ];

                Plotly.newPlot('myDiv', data);
            }

            window.addEventListener('load', start, false);
        </script>
    </head>
    <body style = "background-color:#DDF3FF;font-family: Microsoft JhengHei;">
        <div class="top_nav">
            <div class="nav_menu">
                
            </div>
        </div>
        <div role="main">
            <div class = "">
            <table height = "300px" width = "100%">
                    <tr height = "40%">
                        <td>
                            <br><br><br>
                        </td>
                    </tr>
                    <tr height = "15%">
                        <td align = "center">
                            <h1 style = "color:black">排行榜</h1>
                        </td>
                    </tr>
                    <tr height = "15%">
                        <td>
                            <br><br>
                        </td>
                    </tr>
                    <tr height = "30%">
                        <td align = "center">
                            <div>
                                <div id='myDiv' height = "20%"></div>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </body>
</html>