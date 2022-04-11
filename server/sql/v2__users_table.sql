CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `salt` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 AUTO_INCREMENT=1001 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `todos`
ADD COLUMN `user_id` INT(11) NOT NULL AFTER `id`;
ADD FOREIGN KEY `todos_ibfk_1` (`user_id`) REFERENCES `users` (`id`);
