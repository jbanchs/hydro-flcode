# Frequency Engine Spec

## Purpose

The Frequency Engine determines monitoring or reporting frequency based on the case provided by the user.

## Rule Evaluation Order

1. Match parameter/topic.
2. Match jurisdiction/regulation if provided.
3. Match system type.
4. Match source type.
5. Match population range.
6. Match result condition.
7. Match waiver status.
8. Return most specific rule.
9. If required fields are missing, return missing information.
10. If no rule matches, return insufficient regulatory basis.

## Confidence

- High: Exact rule matched and citation exists.
- Medium: General rule matched but some optional context is missing.
- Low: No direct rule match; answer cannot be confirmed.
