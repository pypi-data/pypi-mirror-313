from pathlib import Path

from anylearn.analyzers import ArtifactCollector
from tests.base_test_case import BaseTestCase


class TestArtifactCollector(BaseTestCase):
    def test_artifact_collection_cases(self):
        file_path = Path(__file__).parent.parent / \
            "assets" / \
            "analyzers" / \
            "artifact_collection_cases.py"
        names = ArtifactCollector().collect(file_path)
        self.assertIn('datasets', names)
        self.assertIn('models', names)
        self.assertIn('task_outputs', names)
        self.assertEqual(
            names['datasets'],
            set([
                'my/dataset1',
                'my/dataset2',
                'my/dataset3',
                'my/dataset4',
                'my/dataset5',
            ]),
        )
        self.assertEqual(
            names['models'],
            set([
                'my/model1',
                'my/model2',
            ]),
        )
        self.assertEqual(
            names['task_outputs'],
            set([
                'mytask1',
                'mytask2',
            ]),
        )
