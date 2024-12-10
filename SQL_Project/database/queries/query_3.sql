SELECT
    s.group_id AS group_identifier,
    AVG(g.grade) AS avg_grade
FROM grades g
JOIN students s ON s.id = g.student_id
WHERE g.subject_id = 2
GROUP BY s.group_id
ORDER BY avg_grade DESC;



