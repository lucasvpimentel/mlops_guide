"""
Testes unitários para os schemas Pydantic.
Não requerem modelo treinado.
"""

import pytest
from pydantic import ValidationError

from app.schemas import DiamondFeatures

VALID_DIAMOND = {
    "carat": 0.89,
    "cut": "Ideal",
    "color": "E",
    "clarity": "VS1",
    "depth": 62.3,
    "table": 57.0,
    "x": 6.18,
    "y": 6.21,
    "z": 3.86,
}


class TestDiamondFeatures:
    def test_valid_input_accepted(self):
        d = DiamondFeatures(**VALID_DIAMOND)
        assert d.carat == 0.89
        assert d.cut == "Ideal"

    def test_invalid_cut_rejected(self):
        with pytest.raises(ValidationError):
            DiamondFeatures(**{**VALID_DIAMOND, "cut": "Perfeito"})

    def test_invalid_color_rejected(self):
        with pytest.raises(ValidationError):
            DiamondFeatures(**{**VALID_DIAMOND, "color": "Z"})

    def test_invalid_clarity_rejected(self):
        with pytest.raises(ValidationError):
            DiamondFeatures(**{**VALID_DIAMOND, "clarity": "XPTO"})

    def test_carat_below_min_rejected(self):
        with pytest.raises(ValidationError):
            DiamondFeatures(**{**VALID_DIAMOND, "carat": 0.0})

    def test_carat_above_max_rejected(self):
        with pytest.raises(ValidationError):
            DiamondFeatures(**{**VALID_DIAMOND, "carat": 99.0})

    def test_extra_field_rejected(self):
        with pytest.raises(ValidationError):
            DiamondFeatures(**{**VALID_DIAMOND, "campo_extra": "não permitido"})

    def test_missing_field_rejected(self):
        """Todos os campos são obrigatórios."""
        data = VALID_DIAMOND.copy()
        del data["clarity"]
        with pytest.raises(ValidationError):
            DiamondFeatures(**data)

    def test_all_valid_cuts_accepted(self):
        for cut in ["Fair", "Good", "Very Good", "Premium", "Ideal"]:
            d = DiamondFeatures(**{**VALID_DIAMOND, "cut": cut})
            assert d.cut == cut

    def test_all_valid_colors_accepted(self):
        for color in ["D", "E", "F", "G", "H", "I", "J"]:
            d = DiamondFeatures(**{**VALID_DIAMOND, "color": color})
            assert d.color == color
