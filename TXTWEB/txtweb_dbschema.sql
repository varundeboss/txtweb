delimiter $$

CREATE TABLE `cust_account` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `UserID` varchar(10) CHARACTER SET latin1 NOT NULL,
      `Username` varchar(30) CHARACTER SET latin1 NOT NULL DEFAULT '',
      `Password` varchar(20) CHARACTER SET latin1 NOT NULL DEFAULT '',
      `Mobile` varchar(40) NOT NULL DEFAULT '',
      `LastMobile` varchar(40) CHARACTER SET latin1 NOT NULL DEFAULT '',
      `Firstname` varchar(20) NOT NULL,
      `Lastname` varchar(20) NOT NULL,
      `Email` varchar(45) CHARACTER SET latin1 NOT NULL,
      `Sex` char(1) CHARACTER SET latin1 NOT NULL,
      `Age` smallint(3) NOT NULL,
      `City` varchar(20) NOT NULL,
      `DOB` date NOT NULL,
      `LogFlag` tinyint(1) NOT NULL DEFAULT '0',
      `LoggedOn` datetime NOT NULL,
      `LogValidity` mediumint(4) NOT NULL DEFAULT '1440',
      `VerifyID` varchar(10) NOT NULL,
      `VerifyFlag` tinyint(1) NOT NULL DEFAULT '0',
      `CreatedOn` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `UpdatedOn` datetime DEFAULT NULL,
      PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8$$


