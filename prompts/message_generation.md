You are helping build a test set of customer support messages for Fernleaf Kitchen, a fictional meal kit delivery company. The messages will be answered by AI support agents, and those replies will be graded against the company policy below.

## Company policy

{policy}

## Your task

Write {count} new customer messages about this topic: **{topic}**

Topic focus: {topic_description}

Here are example messages on this topic. Match their realism, not their wording:

{examples}

## Requirements

- Each message is what a real customer would type into a support chat or email. First person, 1 to 4 sentences.
- Vary the customers: calm, confused, rushed, frustrated, polite, blunt. Some have typos or no capital letters. At most one in five should be angry.
- Vary the difficulty. About a third should be clear-cut. The rest should sit near an edge of the policy: close to a deadline or dollar limit, missing information the policy requires, asking for something the policy doesn't allow, or touching two rules at once.
- When timing or money matters, include the specific details (days, dates, dollar amounts) so the correct answer can be worked out from the message and the policy.
- Do not quote or mention the policy. Customers don't know the rules.
- Do not repeat the examples or each other. Each message should test something slightly different.
- No real company names, real people, or real addresses.

## Output

Return only a JSON array, with no other text. Each element:

{{
  "customer_message": "the message",
  "correct_handling": "one sentence: what a correct reply does under the policy",
  "why_its_tricky": "one short sentence, or 'Baseline case' if it is clear-cut"
}}
