# PassportPal

Gives a personalised passport document checklist and answers on annexures, Tatkal, police verification and fees.

**Status:** Day 1 foundation (FastAPI skeleton, quality gates). Live URL from Day 5.

## Who it's for

Farmer's son in Ariyalur applying for his first passport for a job abroad, confused about documents and police verification.

## The problem

Document rules depend on the case (minor, name change, ECR/ECNR, Tatkal, re-issue) and need specific annexures. Applicants depend on agents.

## Data sources

Passports Act 1967 and Passport Rules 1980, Passport Seva instructions, document advisor content, fee schedule, annexure formats, MEA circulars.

- https://www.passportindia.gov.in/
- https://www.mea.gov.in/
- Terms: Public government instructions.

## Hardest problem (my interview story)

Case-specific document rules: the checklist depends on many combinations (minor, name change, address proof type, ECR) and must list exact annexures. Rules must be combined in code, with retrieval for explanations.

## Signature feature

Checklist builder: answer 7 questions and get your exact documents and annexures, printable in Tamil and English.

## Target metric

Checklist exact for 95%+ of 30 applicant scenarios.

## Run it locally

```bash
uv sync
cp .env.example .env   # Windows: copy .env.example .env
uv run uvicorn passportpal.api.main:create_app --factory --reload
```

Then open http://localhost:8000/docs

## Checks

```bash
uv run pytest
uv run ruff check .
```
