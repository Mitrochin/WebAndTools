SELECT
    s.name AS student_name,
    sbj.name AS course_name
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects sbj ON g.subject_id = sbj.id
WHERE s.id = 2;
