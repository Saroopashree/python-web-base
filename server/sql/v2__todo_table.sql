CREATE TABLE IF NOT EXISTS `todos` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `desc` TEXT NOT NULL,
    `is_completed` TINYINT(1) DEFAULT 0,
    `assignee` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
    FOREIGN KEY (`assignee`) REFERENCES `users` (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 AUTO_INCREMENT=101 COLLATE=utf8mb4_unicode_ci;
