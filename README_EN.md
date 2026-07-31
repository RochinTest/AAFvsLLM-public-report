# AAFvsLLM — specialist-based learning research

> **Status:** research programme closed on 30 July 2026
>
> **Outcome:** a governed modular knowledge system was built; the claim of a
> new intellectual model was not established
>
> **Access:** the research narrative and curated evidence are public; system
> source and deeper reproduction bundles require a separate request

## Name, author and scale

**AAF** was the internal working name of the architecture. The project records
do not contain one stable official English expansion, so this publication does
not invent one retrospectively. `vsLLM` referred to testing an additional
learning architecture beside a base language model, not to a comparison of two
finished products.

The project was led by **Alex Zak** under the GitHub account **RochinTest**. It
was a solo research project using LLMs and Codex as analysis, programming and
verification tools. The main cycle represented in the public timeline ran from
March to July 2026.

## What the system did operationally

AAF was not one new neural network. It was a software layer around a base
model:

1. a normal request entered the baseline path;
2. bounded specialists could propose a fact or a local action;
3. an arbiter was expected to collect relevant claims, detect conflicts and
   either select an answer or abstain;
4. validated knowledge and modules were packaged as versioned retained units;
5. Memory Core, registry, quarantine and rollback controlled their lifecycle;
6. restart tests checked whether new behaviour persisted without breaking old
   behaviour.

A concrete example was source-backed fact lookup. An `author` specialist could
propose the author of a book with provenance. If two incompatible claims
applied to the same semantic slot, the runtime should abstain instead of
returning the first claim. A later ordinary-runtime test found that this safety
property did not hold in 32 conflict cases.

## Research question

AAF asked whether a machine could improve after experience through local
specialists, causal credit, retained memory and coalition formation—without a
full external retraining cycle and without destroying older capabilities.

The project implemented substantial knowledge middleware: typed facts with
provenance, Memory Core learning units, retained specialists, claim
arbitration, deny-by-default writes, quarantine, rollback and a versioned V3
package. It did not demonstrate beneficial shared-representation plasticity or
the synthesis of a new operation by a coalition.

## Decisive results

| Question | Result |
|---|---|
| Bounded retained specialists | Implemented and narrowly tested |
| Retained V3 integrity recovery | Supported for the ten-component package |
| Normal-runtime conflict safety | Not established; a real conflict leak was observed |
| Shared plasticity | Not supported by the available witness |
| Novel coalition operation | Refuted for the decisive witness |
| Relative economics | Unknown |

Retained V3 contained four specialists, 72 source-backed facts and ten hashed
components. Its bounded court recorded 328 requests and 24 new source-backed
answers. After an invalid repair, exact V3 integrity was restored; a subsequent
ordinary-runtime characterization nevertheless observed 32 conflicting cases
returning an answer and three non-conflicting controls behaving normally.

The final synthesis control found that all 24 claimed target ASTs were fixed
three-call chains already present in a pre-enumerated 39-program hypothesis
space. The broader “new composition” claim was therefore revoked.

## Public evidence available now

GitHub may collapse part of the repository tree behind **View all files**. The
published evidence is linked directly here:

- [standard-library verifier](verify_public_evidence.py);
- [SHA-256 manifest](evidence/public/manifest.json);
- [retained V3 integrity capsule](evidence/public/v3_integrity.json);
- [conflict characterization capsule](evidence/public/conflict_characterization.json);
- [plasticity and economics capsule](evidence/public/three_questions.json);
- [nonexpressibility capsule](evidence/public/nonexpressibility.json);
- [evidence ledger](docs/EVIDENCE_LEDGER.md).

```bash
git clone https://github.com/RochinTest/AAFvsLLM-public-report.git
cd AAFvsLLM-public-report
python3 verify_public_evidence.py
```

The verifier uses only the Python standard library. It recomputes the disclosed
claims from the published capsules, but it is not a full independent
replication of the private runtime or the complete raw archive.

Start with the [Russian research dossier](README.md), the
[evidence ledger](docs/EVIDENCE_LEDGER.md), the
[glossary](docs/GLOSSARY.md), and the [postmortem](POSTMORTEM.md).

System/server/Turbo-memory source, private sessions, old Git history and
unreviewed third-party material are not public. Named sanitized research
bundles may be [requested separately](CODE_ACCESS.md).
