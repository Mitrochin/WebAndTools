SELECT
    s.id AS student_id,
    s.name AS student_name,
    AVG(g.grade) AS avg_grade
FROM grades g
JOIN students s ON s.id = g.student_id
WHERE g.subject_id = 1
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 1;


