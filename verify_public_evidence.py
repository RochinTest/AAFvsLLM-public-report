#!/usr/bin/env python3
"""Recompute the claims exposed by the sanitized public evidence capsules.

This verifier checks the disclosed rows, aggregates, cross-file invariants and
SHA-256 manifest. It does not claim to reproduce the private experiments or to
authenticate the provenance of the published capsules.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "public"


class VerificationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def load_json(name: str) -> dict[str, Any]:
    path = EVIDENCE / name
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"{name}: корень JSON должен быть объектом")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_manifest() -> str:
    manifest = load_json("manifest.json")
    require(manifest.get("schema") == "AAFPublicEvidenceManifestV1", "manifest: неизвестная схема")
    files = manifest.get("files")
    require(isinstance(files, dict) and len(files) == 4, "manifest: ожидаются четыре evidence-файла")
    expected_names = {
        "conflict_characterization.json",
        "nonexpressibility.json",
        "three_questions.json",
        "v3_integrity.json",
    }
    require(set(files) == expected_names, "manifest: набор файлов не совпадает с публичным корпусом")
    for name, expected_digest in files.items():
        require(isinstance(expected_digest, str) and len(expected_digest) == 64, f"manifest: неверный SHA-256 для {name}")
        require(sha256(EVIDENCE / name) == expected_digest, f"manifest: содержимое {name} изменено")
    return "4 файла совпали с SHA-256 manifest"


def verify_v3(data: dict[str, Any]) -> str:
    require(data.get("schema") == "AAFPublicRetainedV3EvidenceV1", "V3: неизвестная схема")
    architecture = data["architecture"]
    specialists = architecture["specialists"]
    components = data["integrity_recovery"]["components"]
    require(len(specialists) == 4, "V3: число специалистов не равно 4")
    require(len({row["label"] for row in specialists}) == 4, "V3: метки специалистов не уникальны")
    require(Counter(row["relation"] for row in specialists) == Counter({"author": 2, "inventor": 1, "capital": 1}), "V3: состав областей не совпал")
    require(architecture["component_count"] == len(components) == 10, "V3: число компонентов не равно 10")
    require(len({row["role"] for row in components}) == 10, "V3: роли компонентов не уникальны")
    mismatches = sum(
        row["expected_bytes"] != row["actual_bytes"]
        or row["expected_sha256"] != row["actual_sha256"]
        for row in components
    )
    recovery = data["integrity_recovery"]
    require(mismatches == recovery["component_mismatches"] == 0, "V3: обнаружено несовпадение компонента")
    require(recovery["components_compared"] == len(components), "V3: агрегат компонентов неверен")
    guards = recovery["guards"]
    guard_mismatches = sum(
        row["expected_sha256"] != row["actual_sha256"]
        or row["target_mismatches"] != 0
        for row in guards
    )
    require(len(guards) == recovery["guards_compared"] == 2, "V3: число guards не равно 2")
    require(len({row["label"] for row in guards}) == 2, "V3: метки guards не уникальны")
    require(all(row["target_count"] == 12 for row in guards), "V3: число guard targets не равно 12")
    require(guard_mismatches == recovery["guard_mismatches"] == 0, "V3: обнаружено несовпадение guard")
    require(recovery["production_route_bytes"] == next(row["actual_bytes"] for row in components if row["role"] == "route_runtime_implementation"), "V3: размер runtime не согласован")
    require(recovery["production_route_sha256"] == next(row["actual_sha256"] for row in components if row["role"] == "route_runtime_implementation"), "V3: SHA-256 runtime не согласован")

    court = data["historical_bounded_court"]
    require(court["prior_gap_traffic_cases"] + court["fresh_domain_cases"] == court["sealed_cases"] == 328, "V3: размер исторического court не пересчитался")
    require(court["new_source_backed_answers"] == court["fresh_domain_cases"] == 24, "V3: число новых ответов не пересчиталось")
    require(sum(court[key] for key in ("baseline_preemptions", "false_applicability", "unsupported_answers")) == 0, "V3: исторические нулевые ошибки не подтверждены")
    require(architecture["fact_count"] == 72, "V3: число опубликованных source-backed фактов не равно 72")
    require(data["release"]["version"] == 3, "V3: версия release неверна")
    require(data["lifecycle_witness"]["default_enabled"] is False, "V3: historical default должен быть OFF")
    require(data["lifecycle_witness"]["rollback_domain_d_answer_count"] == 0, "V3: rollback оставил ответы области D")
    return "4 специалиста, 72 факта, 10/10 компонентов, 2/2 guards; historical court aggregate 328 = 304 + 24"


def verify_conflict(data: dict[str, Any]) -> str:
    require(data.get("schema") == "AAFPublicConflictCharacterizationV1", "conflict: неизвестная схема")
    observation = data["normal_runtime_observation"]
    rows = observation["rows"]
    require(len(rows) == observation["case_count"] == 35, "conflict: число строк не равно 35")
    require(len({row["case_id"] for row in rows}) == len(rows), "conflict: case_id не уникальны")

    recomputed_families = Counter((row["family"], row["observed"]) for row in rows)
    reported_families = Counter(
        {(row["family"], row["observed"]): row["cases"] for row in observation["families"]}
    )
    require(recomputed_families == reported_families, "conflict: family-агрегаты не совпали со строками")
    leaks = [row for row in rows if row["conflict_present"] and row["answer_present"]]
    controls = [row for row in rows if not row["conflict_present"] and row["answer_present"]]
    require(len(leaks) == 32, "conflict: ожидалось 32 утечки ответа")
    require(len(controls) == 3, "conflict: ожидалось 3 контрольных ответа")
    require(all(row["distinct_claim_count"] > 1 and row["applicable_fact_count"] >= 2 for row in leaks), "conflict: утечки не содержат разные claims")
    require(data["invalid_repair"]["classification_revoked"] is True, "conflict: невалидный repair должен оставаться отозванным")
    require(all(candidate["installed"] is False for candidate in data["candidate_experiments"]), "conflict: лабораторный candidate ошибочно отмечен установленным")
    return "35 строк пересчитаны: 32 conflict leaks и 3 контроля"


def verify_three_questions(data: dict[str, Any]) -> str:
    require(data.get("schema") == "AAFPublicThreeQuestionsV1", "three questions: неизвестная схема")
    questions = data["questions"]

    plasticity = questions["plasticity"]
    rows = plasticity["case_rows"]
    require(len(rows) == 36 and len({row["case_id"] for row in rows}) == 36, "plasticity: нужны 36 уникальных строк")
    totals = {
        name: sum(bool(row[f"{name}_correct"]) for row in rows)
        for name in ("baseline", "post", "fresh", "rollback")
    }
    require(totals == {"baseline": 21, "post": 19, "fresh": 19, "rollback": 21}, "plasticity: результаты строк не равны 21/19/19/21")
    require(plasticity["baseline_held_out"] == {"cases": 36, "correct": totals["baseline"]}, "plasticity: baseline-агрегат неверен")
    require(plasticity["fresh_process_held_out"] == {"cases": 36, "correct": totals["fresh"]}, "plasticity: fresh-агрегат неверен")
    require(plasticity["rollback_held_out"] == {"cases": 36, "correct": totals["rollback"]}, "plasticity: rollback-агрегат неверен")
    delta = 100.0 * (totals["fresh"] - totals["baseline"]) / len(rows)
    require(abs(delta - plasticity["held_out_change_percentage_points"]) < 1e-12, "plasticity: процентное изменение неверно")
    parameter_rows = plasticity["parameter_rows"]
    require(len(parameter_rows) == 47 and len({row["label"] for row in parameter_rows}) == 47, "plasticity: нужны 47 уникальных parameter rows")
    changed_parameters = sum(bool(row["changed"]) for row in parameter_rows)
    require(changed_parameters == plasticity["changed_parameter_groups"] == 41, "plasticity: число изменённых групп неверно")
    require(len(parameter_rows) == plasticity["parameter_group_count"], "plasticity: число parameter groups неверно")
    parameter_by_label = {row["label"]: row["changed"] for row in parameter_rows}
    require(parameter_by_label.get("embeddings") is plasticity["embedding_changed"] is False, "plasticity: embeddings row не согласована")
    require(parameter_by_label.get("out_proj") is plasticity["shared_output_layer_changed"] is True, "plasticity: output layer row не согласована")
    require(plasticity["representation_probe_present"] is False, "plasticity: representation probe ошибочно заявлен")

    economics = questions["economics"]
    seed_rows = economics["seed_rows"]
    require(len(seed_rows) == economics["seed_record_count"] == 12, "economics: число seed-строк не равно 12")
    require(len({row["index"] for row in seed_rows}) == 12 and len({row["seed"] for row in seed_rows}) == 12, "economics: seed/index не уникальны")
    parent_external = sum(row["parent_route"]["external_decisions"] for row in seed_rows)
    composite_external = sum(row["composite_route"]["external_decisions"] for row in seed_rows)
    parent_exec = sum(row["parent_route"]["specialist_executions"] for row in seed_rows)
    composite_exec = sum(row["composite_route"]["specialist_executions"] for row in seed_rows)
    require((parent_external, composite_external, parent_exec, composite_exec) == (1848, 1296, 1848, 1848), "economics: seed-суммы неверны")
    require(economics["external_decisions"] == {"parent_route": parent_external, "composite_route": composite_external, "reduction": parent_external - composite_external}, "economics: агрегат внешних решений неверен")
    require(economics["actual_specialist_executions"] == {"parent_route": parent_exec, "composite_route": composite_exec, "reduction": parent_exec - composite_exec}, "economics: агрегат запусков неверен")
    require(economics["fair_comparison_court_present"] is False, "economics: fair comparison не проводился")
    return "пластичность 21→19→19→21; экономика: решения −552, executions 0"


def verify_nonexpressibility(data: dict[str, Any], three_questions: dict[str, Any]) -> str:
    require(data.get("schema") == "AAFPublicNonexpressibilityAuditV1", "synthesis: неизвестная схема")
    space = data["program_space"]
    specialists = space["known_specialist_count"]
    min_depth = space["minimum_chain_depth"]
    max_depth = space["maximum_chain_depth"]
    enumerated_count = sum(specialists**depth for depth in range(min_depth, max_depth + 1))
    require(enumerated_count == space["pre_enumerated_program_count"] == 39, "synthesis: пространство 3+9+27 не пересчиталось")

    targets = data["targets"]
    rows = targets["rows"]
    aliases = set(targets["allowed_aliases"])
    admitted_chains = set(itertools.product(sorted(aliases), repeat=space["target_chain_depth"]))
    expressible = [row for row in rows if tuple(row["chain"]) in admitted_chains]
    require(len(rows) == targets["total"] == 24, "synthesis: число target-строк не равно 24")
    require(len(expressible) == targets["expressible_as_fixed_known_chain"] == 24, "synthesis: не все targets являются известными цепочками")
    world_roles = Counter((row["world"], row["role"]) for row in rows)
    require(all(count == 1 for count in world_roles.values()), "synthesis: world/role повторяется")
    require(set(row["role"] for row in rows) == {"primary", "counterfactual"}, "synthesis: неизвестная роль")
    require(len({row["world"] for row in rows}) == data["worlds"]["count"] == 12, "synthesis: число миров не равно 12")
    require(all(sum(row["world"] == world for row in rows) == 2 for world in {row["world"] for row in rows}), "synthesis: в каждом мире должны быть две роли")

    runtime = data["runtime_counts"]
    require(runtime["semantic_target_induction_processes"] == len(rows), "synthesis: target processes не равны строкам")
    require(runtime["semantic_target_induction_processes"] + runtime["control_ablation_execution_or_invariance_processes"] == runtime["total_runtime_processes"] == 420, "synthesis: 420 процессов не пересчитались")
    require(data["sealing_and_isolation"]["protected_write_attempts"] == 0, "synthesis: неожиданная write attempt")
    require(data["sealing_and_isolation"]["os_denied_protected_writes"] == 0, "synthesis: неожиданная OS rejection")
    require(data["sealing_and_isolation"]["write_rejection_witness_present"] is False, "synthesis: ложный write rejection witness")
    require(data["sealing_and_isolation"]["prereveal_hidden_result_hash_committed_before_later_raw_manifest"] is False, "synthesis: ложное pre-reveal hash commitment")
    boundary = data["public_recomputation_boundary"]
    require(boundary["structure_and_fixed_chain_membership_recomputable_from_public_rows"] is True, "synthesis: публичная граница structure неверна")
    require(boundary["full_domain_equivalence_recomputable_from_public_capsule"] is False, "synthesis: public truth tables отсутствуют")

    published = three_questions["questions"]["synthesis"]
    require(published["target_ast_count"] == len(rows), "synthesis: cross-file target count неверен")
    require(published["target_asts_expressible"] == len(expressible), "synthesis: cross-file expressible count неверен")
    require(published["pre_enumerated_program_count"] == enumerated_count, "synthesis: cross-file program count неверен")
    require(data["decision"]["new_operation_interpretation"] == "rejected", "synthesis: итог должен отвергать новую операцию")
    return "39 заранее известных программ; 24/24 targets — фиксированные цепочки; 420 = 24 + 396"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="вывести машинно-читаемый результат")
    args = parser.parse_args()

    checks: list[dict[str, str]] = []
    try:
        checks.append({"name": "manifest", "result": verify_manifest()})
        v3 = load_json("v3_integrity.json")
        checks.append({"name": "retained_v3", "result": verify_v3(v3)})
        conflict = load_json("conflict_characterization.json")
        checks.append({"name": "conflict", "result": verify_conflict(conflict)})
        questions = load_json("three_questions.json")
        checks.append({"name": "three_questions", "result": verify_three_questions(questions)})
        synthesis = load_json("nonexpressibility.json")
        checks.append({"name": "synthesis", "result": verify_nonexpressibility(synthesis, questions)})
    except (KeyError, TypeError, ValueError, OSError, json.JSONDecodeError, VerificationError) as error:
        if args.json:
            print(json.dumps({"status": "FAIL", "error": str(error), "checks_completed": checks}, ensure_ascii=False, indent=2))
        else:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    result = {
        "status": "PASS",
        "checks": checks,
        "boundary": "Проверена внутренняя согласованность опубликованных строк и агрегатов; это не независимая репликация приватных экспериментов.",
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS — публичные evidence-капсулы пересчитаны")
        for check in checks:
            print(f"- {check['name']}: {check['result']}")
        print(f"Граница: {result['boundary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
