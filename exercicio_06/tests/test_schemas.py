"""
Testes unitários para os schemas Pydantic.

Não requerem modelo treinado — testam apenas a validação de dados.
"""

import pytest
from pydantic import ValidationError

from app.schemas import ImageArrayInput


VALID_PIXELS = [128.0] * 784


class TestImageArrayInput:
    """Testes de validação do schema ImageArrayInput."""

    def test_accepts_exactly_784_pixels(self):
        """Array com exatamente 784 pixels deve ser aceito."""
        data = ImageArrayInput(pixels=VALID_PIXELS)
        assert len(data.pixels) == 784

    def test_rejects_array_too_short(self):
        """Array com menos de 784 pixels deve ser rejeitado."""
        with pytest.raises(ValidationError) as exc_info:
            ImageArrayInput(pixels=[128.0] * 783)
        assert "784" in str(exc_info.value)

    def test_rejects_array_too_long(self):
        """Array com mais de 784 pixels deve ser rejeitado."""
        with pytest.raises(ValidationError):
            ImageArrayInput(pixels=[128.0] * 785)

    def test_rejects_extra_fields(self):
        """Campos extras não declarados devem ser rejeitados (extra='forbid')."""
        with pytest.raises(ValidationError):
            ImageArrayInput(pixels=VALID_PIXELS, extra_field="não permitido")

    def test_accepts_zero_pixels(self):
        """Array de 784 zeros (imagem preta) deve ser aceito."""
        data = ImageArrayInput(pixels=[0.0] * 784)
        assert data.pixels[0] == 0.0

    def test_accepts_max_pixel_value(self):
        """Array de 784 valores 255 (imagem branca) deve ser aceito."""
        data = ImageArrayInput(pixels=[255.0] * 784)
        assert data.pixels[0] == 255.0

    def test_accepts_float_pixels(self):
        """Pixels com valores decimais devem ser aceitos."""
        pixels = [float(i % 256) for i in range(784)]
        data = ImageArrayInput(pixels=pixels)
        assert len(data.pixels) == 784

    def test_empty_array_rejected(self):
        """Array vazio deve ser rejeitado."""
        with pytest.raises(ValidationError):
            ImageArrayInput(pixels=[])
