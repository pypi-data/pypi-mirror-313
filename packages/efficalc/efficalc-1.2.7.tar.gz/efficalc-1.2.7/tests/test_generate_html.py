import html

import pytest
from latexexpr_efficalc import brackets

from efficalc import (
    Assumption,
    Calculation,
    CalculationLength,
    Comparison,
    ComparisonStatement,
    FigureBase,
    FigureFromFile,
    Heading,
    Input,
    InputTable,
    Symbolic,
    Table,
    TextBlock,
    Title,
    clear_saved_objects,
)
from efficalc.canvas import Canvas
from efficalc.generate_html import generate_html_for_calc_items


@pytest.fixture
def common_setup_teardown():
    # Set up a sample number
    yield None  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    clear_saved_objects()


def test_assumption(common_setup_teardown):
    a = Assumption("the text")
    result = generate_html_for_calc_items([a])
    assert "[ASSUME]" in result
    assert a.text in result


def test_calculation_number(common_setup_teardown):
    a = Calculation("calc", 5, "in", "describing text", "refer to code")
    result = generate_html_for_calc_items([a])
    assert a.estimate_display_length() == CalculationLength.NUMBER
    assert a.description in result
    assert a.reference in result
    assert a.name in result
    assert a.str_result_with_unit() in result
    assert r"\therefore" not in result


def test_calculation_short(common_setup_teardown):
    a = Input("a", 2, "mm")
    b = Input("b", 7, "mm")
    calc = Calculation("calc_1", a + b, "in", "describing text", "refer to code")
    result = generate_html_for_calc_items([calc])
    assert calc.estimate_display_length() == CalculationLength.SHORT
    assert calc.description in result
    assert calc.reference in result
    assert calc.name in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert calc.str_result_with_unit() in result
    assert r"\therefore" in result


def test_calculation_long(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    calc = Calculation(
        "calc_1",
        a - c + brackets(b * a * c) + b - c - a - b,
        "in",
        "describing text",
        "refer to code",
    )
    result = generate_html_for_calc_items([calc])
    assert calc.estimate_display_length() == CalculationLength.LONG
    assert calc.description in result
    assert calc.reference in result
    assert calc.name in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert calc.str_result_with_unit() in result
    assert r"\therefore" in result


def test_calculation_without_ref(common_setup_teardown):
    a = Input("a", 2, "mm")
    b = Input("b", 7, "mm")
    calc = Calculation("calc_1", a + b, "in", "describing text")
    result = generate_html_for_calc_items([calc])
    assert calc.estimate_display_length() == CalculationLength.SHORT
    assert calc.description in result
    assert calc.name in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert calc.str_result_with_unit() in result
    assert r"\therefore" in result
    assert "[]" not in result  # empty reference tag


def test_calculation_error(common_setup_teardown):
    a = Input("a", 2, "mm")
    calc = Calculation("calc_1", a / 0, "in", "describing text", "refer to code")
    result = generate_html_for_calc_items([calc])
    assert calc.estimate_display_length() == CalculationLength.SHORT
    assert calc.description in result
    assert calc.reference in result
    assert calc.name in result
    assert calc.str_symbolic() in result
    assert calc.str_substituted() in result
    assert calc.str_result_with_unit() in result
    assert r"\therefore" in result
    assert "ERROR:" in result
    assert "could not be calculated because zero was in the denominator." in result


def test_symbolic(common_setup_teardown):
    a = Input("a", 2, "mm")
    b = Input("b", 7, "mm")
    sym = Symbolic("sym", a + b, "describing text", "refer to code")
    result = generate_html_for_calc_items([sym])
    assert sym.description in result
    assert sym.reference in result
    assert sym.name in result
    assert sym.str_symbolic() in result
    assert r"\therefore" not in result


def test_symbolic_without_ref_or_desc(common_setup_teardown):
    sym = Symbolic("calc_1", "sym_str")
    result = generate_html_for_calc_items([sym])
    assert sym.name in result
    assert sym.str_symbolic() in result
    assert r"\therefore" not in result
    assert "[]" not in result  # empty reference tag


def test_symbolic_error(common_setup_teardown):
    a = Input("a", 2, "mm")
    sym = Symbolic("sym", a / 0, "describing text", "refer to code")
    sym.result()
    result = generate_html_for_calc_items([sym])
    assert sym.estimate_display_length() == CalculationLength.SHORT
    assert sym.description in result
    assert sym.reference in result
    assert sym.name in result
    assert sym.str_symbolic() in result
    assert r"\therefore" not in result
    assert "ERROR:" in result
    assert "could not be calculated because zero was in the denominator." in result


def test_comparison_number(common_setup_teardown):

    calc = Comparison(5, ">", 2, "good", "nah", "a describer", "the ref")
    result = generate_html_for_calc_items([calc])
    assert calc.description in result
    assert calc.reference in result
    assert ">" in result
    assert calc.get_message() in result
    assert html.escape(calc.str_symbolic()) in result
    assert html.escape(calc.str_substituted()) in result
    assert r"\therefore" in result


def test_comparison_variable(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    calc = Comparison(a, ">", c, "good", "nah", "a describer", "the ref")
    result = generate_html_for_calc_items([calc])
    assert calc.description in result
    assert calc.reference in result
    assert ">" in result
    assert calc.get_message() in result
    assert html.escape(calc.str_symbolic()) in result
    assert html.escape(calc.str_substituted()) in result
    assert r"\therefore" in result


def test_comparison_without_ref_or_desc(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    calc = Comparison(a, ">", c, "good", "nah")
    result = generate_html_for_calc_items([calc])
    assert ">" in result
    assert calc.get_message() in result
    assert html.escape(calc.str_symbolic()) in result
    assert html.escape(calc.str_substituted()) in result
    assert r"\therefore" in result
    assert "[]" not in result  # empty reference tag
    assert "None" not in result


def test_comparison_statement(common_setup_teardown):
    calc = ComparisonStatement(5, ">", 2, ">=", 1.5, "a describer", "the ref")
    result = generate_html_for_calc_items([calc])
    assert calc.description in result
    assert calc.reference in result
    assert ">" in result
    assert html.escape(calc.str_symbolic()) in result


def test_comparison_statement_without_ref_or_desc(common_setup_teardown):
    calc = ComparisonStatement(5, ">", 2, ">=", 1.5)
    result = generate_html_for_calc_items([calc])
    assert ">" in result
    assert html.escape(calc.str_symbolic()) in result
    assert "[]" not in result  # empty reference tag
    assert "None" not in result


def test_heading_max_size(common_setup_teardown):
    h = Heading("the text", 0, False)
    result = generate_html_for_calc_items([h])
    assert h.text in result
    assert "<h2>" in result


def test_heading_mid_size(common_setup_teardown):
    h = Heading("the text", 2, False)
    result = generate_html_for_calc_items([h])
    assert h.text in result
    assert "<h3>" in result


def test_heading_min_size(common_setup_teardown):
    h = Heading("the text", 6, False)
    result = generate_html_for_calc_items([h])
    assert h.text in result
    assert "<h4>" in result


def test_heading_numbering(common_setup_teardown):
    h0 = Heading("Test 1.")
    h1 = Heading("Test 2.")
    h2 = Heading("Test 2.1.", 2)
    h3 = Heading("Test 2.2.", 2)
    h4 = Heading("Test 2.2.1.", 3)
    h5 = Heading("Test 2.2.1.1.", 4)
    h6 = Heading("Test 2.3.", 2)
    h7 = Heading("Test 2.3.1.", 3)
    h8 = Heading("Test 3.", 1)
    h9 = Heading("Test 4.", 1)
    h10 = Heading("Test 5.", 1)
    h11 = Heading("Test 5.1.1.1.", 4)
    result = generate_html_for_calc_items(
        [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11]
    )
    assert "1.\u00A0 Test 1." in result
    assert "2.\u00A0 Test 2." in result
    assert "2.1.\u00A0 Test 2.1." in result
    assert "2.2.\u00A0 Test 2.2." in result
    assert "2.2.1.\u00A0 Test 2.2.1." in result
    assert "2.2.1.1.\u00A0 Test 2.2.1.1." in result
    assert "2.3.\u00A0 Test 2.3." in result
    assert "2.3.1.\u00A0 Test 2.3.1." in result
    assert "3.\u00A0 Test 3." in result
    assert "4.\u00A0 Test 4." in result
    assert "5.\u00A0 Test 5." in result
    assert "5.1.1.1.\u00A0 Test 5.1.1.1." in result


def test_heading_no_numbering(common_setup_teardown):
    h0 = Heading("Test 1.", numbered=False)
    h1 = Heading("Test 2.", numbered=False)
    h2 = Heading("Test 2.1.", 2, numbered=False)
    h3 = Heading("Test 2.2.", 2, numbered=False)
    h4 = Heading("Test 2.2.1.", 3, numbered=False)
    h5 = Heading("Test 2.2.1.1.", 4, numbered=False)
    result = generate_html_for_calc_items([h0, h1, h2, h3, h4, h5])

    assert "1.\u00A0 Test 1." not in result
    assert "Test 1." in result

    assert "2.\u00A0 Test 2." not in result
    assert "Test 2." in result

    assert "2.1.\u00A0 Test 2.1." not in result
    assert "Test 2.1." in result

    assert "2.2.\u00A0 Test 2.2." not in result
    assert "Test 2.2." in result

    assert "2.2.1.\u00A0 Test 2.2.1." not in result
    assert "Test 2.2.1." in result

    assert "2.2.1.1.\u00A0 Test 2.2.1.1." not in result
    assert "Test 2.2.1.1." in result


def test_input(common_setup_teardown):
    a = Input("calc", 5, "in", "describing text", "refer to code")
    result = generate_html_for_calc_items([a])
    assert a.description in result
    assert "[" + a.reference + "]" in result
    assert a.name in result
    assert str(a) in result
    assert r"\text{" not in result


def test_input_without_desc(common_setup_teardown):
    a = Input("calc", 5, "in", "", "refer to code")
    result = generate_html_for_calc_items([a])
    assert "[" + a.reference + "]" in result
    assert a.name in result
    assert str(a) in result
    assert "None" not in result
    assert r"\text{" not in result


def test_input_without_ref(common_setup_teardown):
    a = Input("calc", 5, "in", "A variable")
    result = generate_html_for_calc_items([a])
    assert "]" not in result
    assert "[" not in result
    assert a.description in result
    assert a.name in result
    assert str(a) in result
    assert "None" not in result
    assert r"\text{" not in result


def test_input_without_unit(common_setup_teardown):
    a = Input("calc", 5, description="A variable")
    result = generate_html_for_calc_items([a])
    assert "]" not in result
    assert "[" not in result
    assert a.description in result
    assert a.name in result
    assert str(a) in result
    assert "None" not in result
    assert r"\text{" not in result


def test_input_plain_text(common_setup_teardown):
    a = Input("calc", "No & no", plain_text_value=True)
    result = generate_html_for_calc_items([a])
    assert a.name in result
    assert r"\text{No &amp; no}" in result
    assert "None" not in result


def test_text_block(common_setup_teardown):
    a = TextBlock("the text", reference="any ref")
    result = generate_html_for_calc_items([a])
    assert a.text in result
    assert a.reference in result


def test_text_block_without_ref(common_setup_teardown):
    a = TextBlock("the text", reference="")
    b = TextBlock("the other text", reference=None)
    result = generate_html_for_calc_items([a, b])
    assert a.text in result
    assert b.text in result
    assert "[" not in result  # empty reference tag
    assert "]" not in result  # empty reference tag
    assert "None" not in result


def test_title(common_setup_teardown):
    a = Title("the text")
    result = generate_html_for_calc_items([a])
    assert a.text in result
    assert "<h1>" in result


def test_figure_default_values(common_setup_teardown):
    fig = FigureBase()
    fig._figure_bytes = b"the figure bytes"
    result = generate_html_for_calc_items([fig])
    assert "<figure>" in result
    assert '<figcaption style="color:#6f6f6f; font-size:0.9em;">' not in result
    assert f'<img src="data:image/png;base64,{fig.get_base64_str()}' in result
    assert "; width:100%;" not in result
    assert 'alt="Calculation figure"' in result
    assert "None" not in result


def test_figure_with_caption_and_full_width(common_setup_teardown):
    fig = FigureBase(caption="Figure Description", full_width=True)
    fig._figure_bytes = b"the figure bytes"
    result = generate_html_for_calc_items([fig])
    assert "<figure>" in result
    assert '<figcaption style="color:#6f6f6f; font-size:0.9em;">' in result
    assert f"{fig.caption}</figcaption>" in result
    assert f'<img src="data:image/png;base64,{fig.get_base64_str()}' in result
    assert "; width:100%;" in result
    assert 'alt="Calculation figure"' not in result
    assert f'alt="{fig.caption}"' in result


def test_figure_invalid_path(common_setup_teardown):
    invalid_image_path = "/invalid/path/none.jpg"
    fig = FigureFromFile(invalid_image_path)
    result = generate_html_for_calc_items([fig])
    assert "<figure>" not in result
    assert "There was an error loading this image" in result
    assert invalid_image_path in result


def test_canvas(common_setup_teardown):
    canvas = Canvas(5, 5, caption=None)
    result = generate_html_for_calc_items([canvas])
    assert "<svg " in result
    assert "<div style=" in result
    assert "<p " not in result


def test_canvas_caption(common_setup_teardown):
    canvas = Canvas(5, 5, caption="test-description", centered=False)
    result = generate_html_for_calc_items([canvas])
    assert "<svg " in result
    assert "<div style=" in result
    assert f'<p style="color:#6f6f6f; font-size:0.9em;">test-description</p>' in result


def test_canvas_centered_caption(common_setup_teardown):
    canvas = Canvas(5, 5, caption="test-description", centered=True)
    result = generate_html_for_calc_items([canvas])
    assert "<svg " in result
    assert "<div style=" in result
    assert (
        f'<p style="color:#6f6f6f; text-align:center; font-size:0.9em;">test-description</p>'
        in result
    )


def test_table_full_composition(common_setup_teardown):
    table = Table(
        [["alpha", 1], ["beta", 2]], ["greeks", "numbers"], "greek letters and numbers"
    )
    result = generate_html_for_calc_items([table])
    assert "<table" in result
    assert (
        "<caption><b>greek letters and numbers</b></caption>"
        "<thead><tr><th>greeks</th><th>numbers</th></tr></thead>"
        "<tbody><tr><td>alpha</td><td>1</td></tr>"
        "<tr><td>beta</td><td>2</td></tr></tbody></table>"
    ) in result


def test_input_table_full_composition(common_setup_teardown):
    table = InputTable(
        [["alpha", 1], ["beta", 2]], ["greeks", "numbers"], "greek letters and numbers"
    )
    result = generate_html_for_calc_items([table])
    assert "<table" in result
    assert (
        "<caption><b>greek letters and numbers</b></caption>"
        "<thead><tr><th>greeks</th><th>numbers</th></tr></thead>"
        "<tbody><tr><td>alpha</td><td>1</td></tr>"
        "<tr><td>beta</td><td>2</td></tr></tbody></table>"
    ) in result


def test_table_data_only(common_setup_teardown):
    table = Table([[1, 2, 3], [1]])
    result = generate_html_for_calc_items([table])
    assert "<table" in result
    assert "caption" not in result
    assert "thead" not in result
    assert "th>" not in result
    assert (
        "<tbody><tr><td>1</td><td>2</td><td>3</td></tr>"
        "<tr><td>1</td></tr></tbody></table>"
    ) in result


def test_table_with_all_styling(common_setup_teardown):
    table = Table([[3]], full_width=True, striped=True)
    result = generate_html_for_calc_items([table])
    assert '<table class="striped" style="margin:auto; width:100%;">' in result
    assert "<tbody><tr><td>3</td></tr></tbody></table>" in result
    assert "1</td>" not in result


def test_table_with_no_styling(common_setup_teardown):
    table = Table([[3]], full_width=False, striped=False)
    result = generate_html_for_calc_items([table])
    assert (
        '<table style="margin:auto;"><tbody><tr><td>3</td></tr></tbody></table>'
        in result
    )
    assert "1" not in result


def test_table_no_data(common_setup_teardown):
    table = Table([], ["greeks", "numbers"])

    result = generate_html_for_calc_items([table])
    assert "<table" in result
    assert (
        "<thead><tr><th>greeks</th><th>numbers</th></tr></thead>"
        "<tbody></tbody></table>"
    ) in result
    assert "1" not in result


def test_table_with_row_numbers(common_setup_teardown):
    table = Table(
        [["f", "g"], ["i", "j"], ["l", "m"]],
        ["greeks", "numbers"],
        numbered_rows=True,
    )

    result = generate_html_for_calc_items([table])
    assert "<table" in result
    assert "0" not in result
    assert "<tr><th></th><th>greeks</th><th>numbers</th></tr>" in result
    assert "<tr><td>1</td><td>f</td><td>g</td></tr>" in result
    assert "<td>2</td><td>i</td>" in result
    assert "<td>3</td><td>l</td>" in result


def test_table_with_row_numbers_without_headers(common_setup_teardown):
    table = Table([["f"]], numbered_rows=True)

    result = generate_html_for_calc_items([table])
    assert "<table" in result
    assert "<tr><td>1</td><td>f</td></tr>" in result
    assert "2</td>" not in result


def test_inline_equation_escapes_hash_character(common_setup_teardown):
    a = Input("calc#", 5, "in", "describing text", "refer to code")
    result = generate_html_for_calc_items([a])
    assert r"calc\#" in result
    assert r"calc#" not in result
    assert a.description in result
    assert "[" + a.reference + "]" in result


def test_equation_escapes_hash_character(common_setup_teardown):
    a = Input("a", 2)
    b = Input("b", 3)
    c = Calculation("c", a + b)
    calc = Calculation(
        "calc #1",
        a - c + brackets(b * a * c) + b - c - a - b,
        "in",
        "describing # text",
        "refer to code",
    )
    result = generate_html_for_calc_items([calc])
    assert calc.estimate_display_length() == CalculationLength.LONG
    assert calc.name not in result
    assert "calc \#1" in result
    assert calc.description in result
    assert calc.reference in result
    assert r"\therefore" in result
