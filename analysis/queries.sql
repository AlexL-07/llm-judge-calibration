-- Agreement queries. Assumes two tables loaded from CSV into SQLite:
--   gold(item_id, accuracy, resolution, tone, verdict, reason)
--   judge_outputs(item_id, judge, accuracy, resolution, tone, verdict, reason)

-- 1. Exact agreement with gold, per judge and per dimension
SELECT
    j.judge,
    ROUND(AVG(j.accuracy   = g.accuracy),   2) AS accuracy_agree,
    ROUND(AVG(j.resolution = g.resolution), 2) AS resolution_agree,
    ROUND(AVG(j.tone       = g.tone),       2) AS tone_agree,
    ROUND(AVG(j.verdict    = g.verdict),    2) AS verdict_agree
FROM judge_outputs j
JOIN gold g USING (item_id)
GROUP BY j.judge;

-- 2. Leniency: average score per judge vs gold (positive = judge grades easier)
SELECT
    j.judge,
    ROUND(AVG(j.accuracy   - g.accuracy),   2) AS accuracy_diff,
    ROUND(AVG(j.resolution - g.resolution), 2) AS resolution_diff,
    ROUND(AVG(j.tone       - g.tone),       2) AS tone_diff
FROM judge_outputs j
JOIN gold g USING (item_id)
GROUP BY j.judge;

-- 3. Items where gold is Fail but a judge said Pass (missed failures)
SELECT j.item_id, j.judge, g.reason AS gold_reason, j.reason AS judge_reason
FROM judge_outputs j
JOIN gold g USING (item_id)
WHERE g.verdict = 'Fail' AND j.verdict = 'Pass'
ORDER BY j.item_id;

-- 4. Items where all 3 judges disagree with gold on verdict (likely rubric gap)
SELECT j.item_id, g.verdict AS gold_verdict, COUNT(*) AS judges_disagreeing
FROM judge_outputs j
JOIN gold g USING (item_id)
WHERE j.verdict <> g.verdict
GROUP BY j.item_id
HAVING COUNT(*) = 3;
