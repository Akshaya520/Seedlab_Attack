<?php 
	define('DB_SERVER', 'db');
	define('DB_USER', 'user');
	define('DB_PASS', 'test');
	define('DB_NAME', 'library');
	
	// 1. Create database connection
	$connection = mysqli_connect(DB_SERVER,DB_USER,DB_PASS,DB_NAME);
	if (mysqli_connect_errno()) {
		die("Database connection failed------: ".mysqli_connect_error()."(".mysqli_connect_errno().")");
	}
?>
