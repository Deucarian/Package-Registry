import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deucarian_refactor_comparison import analyze_sources, clone_metrics, revision_files


class RefactorComparisonTests(unittest.TestCase):
    def files(self, body, path="Runtime/Example.cs"):
        return {path: body, "Runtime/Example.asmdef": json.dumps({"name": "Example"})}

    def source(self, name="Work", local="value", number=8):
        return f'''class Example {{ public int {name}(int {local}) {{
            int multiplier = 3;
            if ({local} < {number}) {{ return {local} + {number}; }}
            return {local} * {number} + ({local} - 2) * multiplier;
        }} }}'''

    def test_file_move_and_whitespace_do_not_change_fingerprints(self):
        before = analyze_sources("One", self.files(self.source()))["methods"][0]
        after = analyze_sources("One", self.files(self.source().replace("return", "/* comment */ return"), "Runtime/Moved.cs"))["methods"][0]
        self.assertEqual(before["exactHash"], after["exactHash"])
        self.assertEqual(before["tokens"], after["tokens"])

    def test_local_rename_is_only_a_structural_candidate(self):
        before = analyze_sources("One", self.files(self.source()))["methods"][0]
        after = analyze_sources("One", self.files(self.source(local="amount")))["methods"][0]
        self.assertNotEqual(before["exactHash"], after["exactHash"])
        self.assertEqual(before["localNameNormalizedHash"], after["localNameNormalizedHash"])

    def test_literals_are_not_erased(self):
        before = analyze_sources("One", self.files(self.source()))["methods"][0]
        after = analyze_sources("One", self.files(self.source(number=9)))["methods"][0]
        self.assertNotEqual(before["localNameNormalizedHash"], after["localNameNormalizedHash"])

    def test_member_names_are_not_treated_as_same_named_locals(self):
        first = self.source().replace('return value * 8', 'return sink.value(value) * 8')
        renamed = self.source(local='amount').replace('return amount * 8', 'return sink.value(amount) * 8')
        changed_api = renamed.replace('sink.value(', 'sink.amount(')
        hashes = [analyze_sources('One', self.files(code))['methods'][0]['localNameNormalizedHash']
                  for code in [first, renamed, changed_api]]
        self.assertEqual(hashes[0], hashes[1])
        self.assertNotEqual(hashes[1], hashes[2])

    def test_parameter_identity_and_operand_order_are_preserved(self):
        source = '''class Example { int Work(int left, int right) {
            int total = left + right;
            if (total < 8) { return total + left; }
            return left - right + total * 3;
        } }'''
        changed = source.replace('return left - right', 'return right - left')
        first = analyze_sources('One', self.files(source))['methods'][0]
        second = analyze_sources('One', self.files(changed))['methods'][0]
        self.assertNotEqual(first['localNameNormalizedHash'], second['localNameNormalizedHash'])

    def test_intra_package_clones_count_once_per_redundant_copy(self):
        first = analyze_sources("One", self.files(self.source()))["methods"][0]
        rows = [first, {**first, "symbol": "Second"}, {**first, "symbol": "Third"}]
        metric = clone_metrics(rows, "exactHash")
        self.assertEqual(1, metric["cloneGroups"])
        self.assertEqual(0, metric["crossPackageCloneGroups"])
        self.assertEqual(first["tokens"] * 2, metric["redundantBodyTokens"])
        self.assertAlmostEqual(66.6667, metric["redundantBodyTokenPercent"])

    def test_cross_package_groups_are_not_double_counted(self):
        first = analyze_sources("One", self.files(self.source()))["methods"][0]
        metric = clone_metrics([first, {**first, "repository": "Two"}], "exactHash")
        self.assertEqual(1, metric["crossPackageCloneGroups"])
        self.assertEqual(first["tokens"], metric["redundantBodyTokens"])

    def test_tests_samples_generated_and_tiny_wrappers_are_excluded(self):
        files = self.files("class Example { public int Tiny() { return 1; } }")
        files.update({"Tests/Example.cs": self.source(), "Samples~/Example.cs": self.source(),
                      "Runtime/Example.g.cs": self.source(),
                      "Tests/Tests.asmdef": json.dumps({"name": "Example.Tests", "optionalUnityReferences": ["TestAssemblies"]})})
        result = analyze_sources("One", files)
        self.assertEqual([], result["methods"])
        self.assertEqual(1, result["productionFiles"])

    def test_partial_type_metrics_are_aggregated(self):
        files = self.files("partial class Example { public int One() { return 1; } }")
        files["Runtime/Other.cs"] = "partial class Example { public int Two() { return 2; } }"
        result = analyze_sources("One", files)
        self.assertEqual(1, len(result["types"]))
        self.assertEqual(2, next(iter(result["types"].values()))["methods"])

    def test_invalid_source_does_not_silently_lower_totals(self):
        with self.assertRaisesRegex(ValueError, "Unparsed"):
            analyze_sources("One", self.files("class Broken { public int ;"))

    def test_empty_denominator_and_mutable_revision_are_explicit(self):
        self.assertEqual(0, clone_metrics([], "exactHash")["redundantBodyTokenPercent"])
        with self.assertRaisesRegex(ValueError, "immutable"):
            revision_files(Path("."), "main")


if __name__ == "__main__":
    unittest.main()
