<?php
	$name = $_GET['name'];	
	
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

    $maxCount = 0;
    $nameCount = 0;
	
	while($row = $result->fetch_assoc())		#得到某筆資料的name和email
	{
        $count = $row['count'];
        if($count > $maxCount)
            $maxCount = $count;
        if($row['name'] == $name)
            $nameCount = $count;
	}
	
	if(mysqli_num_rows($result) == 0 || $nameCount != $maxCount)   #mysqli_num_rows($result)計算符合的資料筆數
	{
       header("Location: http://192.168.43.162:80/isMax=0");
	}
	else
	{
        header("Location:  http://192.168.43.162:80/isMax=1");
	}
?>
