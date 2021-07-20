<?php
	$name = $_GET['name'];
	
	$query = "SELECT * FROM `camera` WHERE `name` = '".$name."'";
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
	
	while($row = $result->fetch_assoc())		#得到某筆資料的name和email
	{
		$count = $row['count'];
	}
    
    $query1 = "UPDATE `camera` SET `count` = '".$addCount."' WHERE `name` = '".$name."'";
    if ($database->query($query1) === TRUE) 
	{
		echo 'EDIT OK';			
	} 
	else 
	{
		echo 'EDIT ERROR';
	}
?>