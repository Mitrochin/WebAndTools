SELECT
    s.name AS student_name,
    sbj.name AS course_name,
    t.name AS teacher_name
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects sbj ON g.subject_id = sbj.id
JOIN teachers t ON sbj.teacher_id = t.id
WHERE s.id = 2
  AND t.id = 2;



