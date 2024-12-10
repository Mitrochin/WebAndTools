SELECT
    g.subject_id AS subject_identifier,
    s.name AS subject_name,
    s.teacher_id AS teacher_identifier,
    AVG(g.grade) AS avg_grade
FROM grades g
JOIN subjects s ON g.subject_id = s.id
WHERE s.teacher_id = 2
GROUP BY s.teacher_id, g.subject_id, s.name;



