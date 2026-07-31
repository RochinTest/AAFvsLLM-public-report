# AAFvsLLM — specialist-based learning research

> **Status:** research programme closed on 30 July 2026
>
> **Outcome:** a governed modular knowledge system was built; the claim of a
> new intellectual model was not established
>
> **Access:** the research narrative and curated evidence are public; system
> source and deeper reproduction bundles require a separate request

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

## Public evidence

The repository includes sanitized evidence capsules and a standard-library
verifier:

```bash
python3 verify_public_evidence.py
```

Start with the [Russian research dossier](README.md), the
[evidence ledger](docs/EVIDENCE_LEDGER.md), and the
[postmortem](POSTMORTEM.md).

System/server/Turbo-memory source, private sessions, old Git history and
unreviewed third-party material are not public. Named sanitized research
bundles may be [requested separately](CODE_ACCESS.md).
