"""
Validadores para formularios de la aplicación
Centraliza validación de entradas del usuario
"""

import re
from typing import Optional


class ValidationResult:
    """
    Resultado de una validación
    """

    def __init__(self, is_valid: bool, error_message: str = ""):
        self.is_valid = is_valid
        self.error_message = error_message

    def __bool__(self) -> bool:
        return self.is_valid

    def __repr__(self) -> str:
        return f"ValidationResult(valid={self.is_valid}, error='{self.error_message}')"


class FormValidator:
    """
    Validador centralizado para formularios
    Implementa validaciones comunes y específicas del dominio
    """

    @staticmethod
    def validate_not_empty(value: str, field_name: str = "Campo") -> ValidationResult:
        """
        Valida que un campo no esté vacío

        Args:
            value: Valor a validar
            field_name: Nombre del campo para el mensaje de error

        Returns:
            ValidationResult con el resultado
        """
        if not value or not value.strip():
            return ValidationResult(False, f"{field_name} no puede estar vacío")
        return ValidationResult(True)

    @staticmethod
    def validate_length(
        value: str,
        min_length: int = 0,
        max_length: Optional[int] = None,
        field_name: str = "Campo",
    ) -> ValidationResult:
        """
        Valida la longitud de un campo

        Args:
            value: Valor a validar
            min_length: Longitud mínima
            max_length: Longitud máxima (opcional)
            field_name: Nombre del campo

        Returns:
            ValidationResult con el resultado
        """
        length = len(value)

        if length < min_length:
            return ValidationResult(
                False, f"{field_name} debe tener al menos {min_length} caracteres"
            )

        if max_length and length > max_length:
            return ValidationResult(
                False, f"{field_name} no puede exceder {max_length} caracteres"
            )

        return ValidationResult(True)

    @staticmethod
    def validate_product_name(product_name: str) -> ValidationResult:
        """
        Valida un nombre de producto

        Args:
            product_name: Nombre del producto

        Returns:
            ValidationResult con el resultado
        """
        # Verificar que no esté vacío
        result = FormValidator.validate_not_empty(product_name, "Nombre del producto")
        if not result:
            return result

        # Verificar longitud
        result = FormValidator.validate_length(
            product_name, min_length=3, max_length=200, field_name="Nombre del producto"
        )
        if not result:
            return result

        # Validar caracteres permitidos (letras, números, espacios, guiones)
        if not re.match(r"^[a-zA-Z0-9\s\-_áéíóúñÁÉÍÓÚÑ]+$", product_name):
            return ValidationResult(
                False,
                "Nombre del producto contiene caracteres no permitidos. Use solo letras, números, espacios y guiones",
            )

        return ValidationResult(True)

    @staticmethod
    def validate_float(
        value: str,
        field_name: str = "Precio",
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> ValidationResult:
        """
        Valida que un precio sea un decimal válido

        Args:
            precio: Valor a validar
            field_name: Nombre del campo
            min_value: Valor mínimo permitido (opcional)
            max_value: Valor máximo permitido (opcional)

        Returns:
            ValidationResult con el resultado
        """
        try:
            int_value = float(value)
        except ValueError:
            return ValidationResult(False, f"{field_name} debe ser un número decimal")

        if min_value is not None and int_value < min_value:
            return ValidationResult(
                False, f"{field_name} debe ser al menos {min_value}"
            )

        if max_value is not None and int_value > max_value:
            return ValidationResult(
                False, f"{field_name} no puede ser mayor que {max_value}"
            )

        return ValidationResult(True)

    @staticmethod
    def validate_file_path(path: str, must_exist: bool = False) -> ValidationResult:
        """
        Valida una ruta de archivo

        Args:
            path: Ruta a validar
            must_exist: Si True, verifica que el archivo exista

        Returns:
            ValidationResult con el resultado
        """
        from pathlib import Path

        if not path or not path.strip():
            return ValidationResult(False, "Debe proporcionar una ruta de archivo")

        try:
            file_path = Path(path)

            if must_exist and not file_path.exists():
                return ValidationResult(False, f"El archivo no existe: {path}")

            return ValidationResult(True)
        except Exception as e:
            return ValidationResult(False, f"Ruta de archivo inválida: {str(e)}")
