<?php
    $query = "SELECT * FROM `drink`";
    if ( !( $database = mysqli_connect( "localhost", "1073320", "" ) ) )
        die( "Could not connect to database </body></html>" );
    if ( !mysqli_select_db($database,"iot" ) )
        die( "Could not open maker database </body></html>" );
    if ( !( $result = mysqli_query($database, $query) ) )
    {
        print( "<p>Could not execute query!</p>" );
        die( mysqli_error() . "</body></html>" );
    }
   
    echo("<table border='1px solid black'>");
    while($row = $result->fetch_assoc())        #得到某筆資料的id和brand
    {
        echo("<tr>");
        echo("<td id = 'id'>".$row['id']."</td>");
        echo("<td id = 'name'>".$row['name']."</td>");
        echo("<td id = 'drinkPos'>".$row['drinkPos']."</td>");
        echo("<td id = 'originalWeight'>".$row['originalWeight']."</td>");
       echo("<td id = 'nowWeight'>".$row['nowWeight']."</td>");
       echo("</tr>");
    }
 echo("</table>");

    mysqli_close( $database );
?>