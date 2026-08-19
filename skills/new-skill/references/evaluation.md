# Evaluation and iteration

Use evaluation to answer two separate questions:

1. Does the description trigger on the right requests?
2. Does the invoked skill improve execution and output quality?

Do not infer one from the other.

## Build output-quality evals

Start with two or three realistic prompts while drafting, then expand after the workflow stabilizes. Cover:

- a representative happy path
- a consequential edge case
- a boundary case that should require clarification or refusal
- different input shapes or client environments when relevant

For each prompt, record its `kind` (`representative`, `edge-case`, `near-miss`, or `regression`), expected output, input files, and objective expectations. Every maintained suite covers at least the first three kinds. Good expectations are independently verifiable and discriminating: a baseline should not pass them automatically. Use human review for taste, clarity, and visual quality instead of forcing subjective judgments into brittle assertions.

Use `templates/evals.json.template` as the starting schema.

## Compare fairly

For a new skill, compare with-skill runs against no-skill runs. For an improved skill, snapshot the previous version and use it as the baseline. Keep prompts, input files, model, permissions, and environment constant.

Run configurations together where isolated parallel sessions are supported. Otherwise run them sequentially in clean sessions. Repeat stochastic runs when the decision matters; three runs per prompt is a practical starting point.

Capture:

- expectation pass/fail with evidence
- artifacts and execution transcript
- errors and retries
- elapsed time and token usage when available
- user feedback

Programmatically check file formats, schemas, counts, links, and deterministic properties. Do not grade those by eye.

## Minimal file layout

```text
<skill>-workspace/
└── iteration-1/
    ├── eval-name/
    │   ├── with-skill/
    │   │   ├── outputs/
    │   │   ├── grading.json
    │   │   └── timing.json
    │   └── baseline/
    │       ├── outputs/
    │       ├── grading.json
    │       └── timing.json
    └── benchmark.json
```

Use exact grading fields so simple tooling can aggregate them:

```json
{
  "expectations": [
    {
      "text": "The generated skill includes a README with three example prompts",
      "passed": true,
      "evidence": "README.md lines 42–48 contain three distinct prompts"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 0,
    "total": 1,
    "pass_rate": 1.0
  }
}
```

Aggregate mean and standard deviation for pass rate, time, and tokens. Flag expectations that always pass, high-variance cases, and quality gains that require disproportionate cost.

## Human review

Show the prompt, outputs, baseline, formal grades, and any previous iteration side by side. Empty feedback means acceptable; specific feedback should drive the next revision. Blind A/B review is useful when comparing close variants: hide which version produced each output and judge against the same rubric.

Do not revise only from aggregate scores. Inspect traces for wasted work, ignored instructions, repeated improvised helpers, and hidden assumptions.

## Trigger evaluation

Create about 20 realistic queries:

- 8–10 should-trigger requests spanning formal, casual, terse, detailed, explicit, and implicit phrasing
- 8–10 near misses that share vocabulary but need an adjacent capability

Avoid obviously unrelated negatives. Include file paths, project context, typos, and multi-step requests.

Run each query multiple times and record whether the client loaded the skill. Three runs provide an initial trigger rate. Split the query set once into approximately 60% training and 40% held-out validation, preserving positive/negative balance.

Iterate on training failures:

- missed positives indicate a description that is too narrow or uses the wrong intent language
- false positives indicate a description that lacks boundaries
- repeated keyword patches indicate overfitting; revise the conceptual framing instead

Choose the best description by held-out validation rate, not by the final iteration or training score. Keep the portable description at or below 1024 characters. Finish with fresh queries that were not used during optimization.

## Improvement loop

1. Draft or snapshot.
2. Run with-skill and baseline cases.
3. Grade objective expectations and collect human feedback.
4. Identify the smallest generalizable instruction, reference, script, or routing change.
5. Prune any line that no longer earns its context cost.
6. Rerun the complete set in a new iteration.

Stop when all material expectations pass and qualitative feedback is acceptable, or when additional revisions do not produce meaningful held-out gains.
