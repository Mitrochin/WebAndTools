SELECT
    s.name AS student_name,
    g.name AS group_name
FROM students s
JOIN groups g ON s.group_id = g.id
WHERE s.group_id = 2;

