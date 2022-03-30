CREATE TABLE userinfo
(`id` int not null AUTO_INCREMENT,
`email` VARCHAR(255) not null,
`token` VARCHAR(255) not null,
`courses` JSON,
 PRIMARY KEY (`id`));