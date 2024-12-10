SELECT
    t.name AS teacher_name,
    s.name AS course_name
FROM teachers t
JOIN subjects s ON t.id = s.teacher_id;



