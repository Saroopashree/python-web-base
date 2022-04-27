ALTER TABLE `todos`
ADD COLUMN `assignee` INT(11)
ADD FOREIGN KEY `todos_ibfk_2` (`user_id`) REFERENCES `users` (`id`);
