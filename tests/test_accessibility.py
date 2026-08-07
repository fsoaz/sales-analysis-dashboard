from src.styles import ACCENT, DANGER, MUTED, PRIMARY_DARK, SUCCESS, WARNING


def _relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def test_text_palette_meets_wcag_aa_against_white():
    white = _relative_luminance("#FFFFFF")
    for color in (PRIMARY_DARK, ACCENT, SUCCESS, DANGER, WARNING, MUTED):
        luminance = _relative_luminance(color)
        contrast = (max(luminance, white) + 0.05) / (min(luminance, white) + 0.05)
        assert contrast >= 4.5, f"{color} has only {contrast:.2f}:1 contrast"
