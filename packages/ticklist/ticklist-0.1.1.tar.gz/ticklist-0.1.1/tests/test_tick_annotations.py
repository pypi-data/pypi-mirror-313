from ticklist.tick_annotations import BooleanLabels, Label, to_tick_annotations


def test_tick_annotations_success():
    annotations = [Label("mylabel"), BooleanLabels("YES", "NO"), "somevalue"]

    tick_annotations = to_tick_annotations(annotations)

    assert tick_annotations == {
        "boolean_labels": BooleanLabels("YES", "NO"),
        "label": Label("mylabel"),
    }
