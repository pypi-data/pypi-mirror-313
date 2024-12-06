from fontbakery.prelude import check, Message, FAIL, PASS


@check(
    id="opentype/STAT_has_axis_value_tables",
    rationale="""
        According to the OpenType spec, in a variable font, it is strongly recommended
        that axis value tables be included for every element of typographic subfamily
        names for all of the named instances defined in the 'fvar' table.

        Axis value tables are particularly important for variable fonts, but can also
        be used in non-variable fonts. When used in non-variable fonts, axis value
        tables for particular values should be implemented consistently across fonts
        in the family.

        If present, Format 4 Axis Value tables are checked to ensure they have more than
        one AxisValueRecord (a strong recommendation from the OpenType spec).

        https://docs.microsoft.com/en-us/typography/opentype/spec/stat#axis-value-tables
    """,
    conditions=["has_STAT_table"],
    proposal="https://github.com/fonttools/fontbakery/issues/3090",
)
def check_STAT_has_axis_value_tables(ttFont, is_variable_font):
    """STAT table has Axis Value tables?"""
    passed = True
    STAT_table = ttFont["STAT"].table

    if ttFont["STAT"].table.AxisValueCount == 0:
        yield FAIL, Message(
            "no-axis-value-tables",
            "STAT table has no Axis Value tables.",
        )
        return

    if is_variable_font:
        # Collect all the values defined for each design axis in the STAT table.
        STAT_axes_values = {}
        for axis_index, axis in enumerate(STAT_table.DesignAxisRecord.Axis):
            axis_tag = axis.AxisTag
            axis_values = set()

            # Iterate over Axis Value tables.
            for axis_value in STAT_table.AxisValueArray.AxisValue:
                axis_value_format = axis_value.Format

                if axis_value_format in (1, 2, 3):
                    if axis_value.AxisIndex != axis_index:
                        # Not the axis we're collecting for, skip.
                        continue

                    if axis_value_format == 2:
                        axis_values.add(axis_value.NominalValue)
                    else:
                        axis_values.add(axis_value.Value)

                elif axis_value_format == 4:
                    # check that axisCount > 1. Also, format 4 records DO NOT
                    # contribute to the "STAT_axes_values" list used to check
                    # against fvar instances.
                    # see https://github.com/fonttools/fontbakery/issues/3957
                    if axis_value.AxisCount <= 1:
                        yield FAIL, Message(
                            "format-4-axis-count",
                            "STAT Format 4 Axis Value table has axis count <= 1.",
                        )

                else:
                    # FAIL on unknown axis_value_format
                    yield FAIL, Message(
                        "unknown-axis-value-format",
                        f"AxisValue format {axis_value_format} is unknown.",
                    )

            STAT_axes_values[axis_tag] = axis_values

        # Iterate over the 'fvar' named instances, and confirm that every coordinate
        # can be represented by the STAT table Axis Value tables.
        for inst in ttFont["fvar"].instances:
            for coord_axis_tag, coord_axis_value in inst.coordinates.items():
                if (
                    coord_axis_tag in STAT_axes_values
                    and coord_axis_value in STAT_axes_values[coord_axis_tag]
                ):
                    continue

                yield FAIL, Message(
                    "missing-axis-value-table",
                    f"STAT table is missing Axis Value for"
                    f" {coord_axis_tag!r} value '{coord_axis_value}'",
                )
                passed = False

    if passed:
        yield PASS, "STAT table has Axis Value tables."
