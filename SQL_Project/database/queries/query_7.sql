SELECT
    s.name AS student_name,
    s.group_id AS group_identifier,
    g.subject_id AS subject_identifier,
    g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.group_id = 2 AND g.subject_id = 3;

