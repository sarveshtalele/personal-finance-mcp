"""Output formatting utilities for MCP tool responses."""


def format_currency(amount: float, symbol: str = "₹") -> str:
    """Format number as Indian currency."""
    if amount < 0:
        return f"-{symbol}{abs(amount):,.2f}"
    return f"{symbol}{amount:,.2f}"


def format_percentage(value: float) -> str:
    """Format as percentage."""
    return f"{value:.2f}%"


def format_section(title: str, content: dict, indent: int = 2) -> str:
    """Format a section with title and key-value pairs."""
    lines = [f"\n{'═' * 50}", f"  {title}", f"{'═' * 50}"]
    prefix = " " * indent

    for key, value in content.items():
        if key in ("formula", "reference"):
            continue
        display_key = key.replace("_", " ").title()
        if isinstance(value, float):
            if (
                "ratio" in key
                or "rate" in key
                or "pct" in key
                or "yield" in key
                or "return" in key
            ):
                lines.append(f"{prefix}{display_key}: {format_percentage(value)}")
            elif abs(value) >= 100:
                lines.append(f"{prefix}{display_key}: {format_currency(value)}")
            else:
                lines.append(f"{prefix}{display_key}: {value}")
        elif isinstance(value, dict):
            lines.append(f"{prefix}{display_key}:")
            for k, v in value.items():
                k_display = k.replace("_", " ").title()
                if isinstance(v, float) and abs(v) >= 100:
                    lines.append(f"{prefix}  {k_display}: {format_currency(v)}")
                else:
                    lines.append(f"{prefix}  {k_display}: {v}")
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            lines.append(f"{prefix}{display_key}:")
            for item in value[:10]:  # limit list output
                item_str = " | ".join(
                    f"{k}: {format_currency(v) if isinstance(v, float) and abs(v) >= 100 else v}"
                    for k, v in item.items()
                )
                lines.append(f"{prefix}  {item_str}")
            if len(value) > 10:
                lines.append(f"{prefix}  ... and {len(value) - 10} more rows")
        else:
            lines.append(f"{prefix}{display_key}: {value}")

    return "\n".join(lines)


def format_tool_response(title: str, result: dict, reference: str = "") -> str:
    """Format complete tool response with title, results, formula, and reference."""
    output = format_section(title, result)

    if "formula" in result:
        output += f"\n\n  Formula: {result['formula']}"

    if reference:
        output += f"\n\n  Reference: {reference}"

    return output


def format_table(headers: list[str], rows: list[list], title: str = "") -> str:
    """Format data as ASCII table."""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    header_line = (
        "|" + "|".join(f" {h:<{col_widths[i]}} " for i, h in enumerate(headers)) + "|"
    )

    lines = []
    if title:
        lines.append(f"\n  {title}")
    lines.append(separator)
    lines.append(header_line)
    lines.append(separator)
    for row in rows:
        row_line = (
            "|"
            + "|".join(f" {str(cell):<{col_widths[i]}} " for i, cell in enumerate(row))
            + "|"
        )
        lines.append(row_line)
    lines.append(separator)

    return "\n".join(lines)
