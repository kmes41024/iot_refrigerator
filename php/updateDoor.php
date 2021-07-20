<?php
	header("content-type: text/html; charset=utf-8");

    $doorPos = $_GET['doorPos'];
    $isOpen = $_GET['isOpen'];

	$query = "UPDATE `door` SET `isOpen` = '".$isOpen."' WHERE `doorPos` = ".$doorPos;

	if ( !( $database = mysqli_connect( "localhost", "1073320", "" ) ) )				#( "主機", "使用者", "密碼" )
	   die( "Could not connect to database </body></html>" );
   
	mysqli_query($database, "set names 'utf8'");							
	mysqli_query($database,"set character_set_client=utf8");
	mysqli_query($database,"set character_set_results=utf8");	
   
	if ( !mysqli_select_db($database,"iot" ) )						#crud改成資料庫的名稱
	   die( "Could not open database </body></html>" );
	if ( !( $result = mysqli_query($database, $query) ) )
	{
	   print( "<p>Could not execute query!</p>" );
	   die( mysqli_error() . "</body></html>" );
	}

	if ($database->query($query) === TRUE) 
	{
		echo "OK";
	} 
	else 
	{
		echo "error";
	}
   
	mysqli_close( $database );
?>