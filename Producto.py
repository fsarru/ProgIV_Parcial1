from abc import ABC

import Categoria


class Producto(ABC):
    def __init__(self, nombre: str, precio_base: float, stock_cantidad: float, categoria_principal: Categoria, unidad_venta: Optional[UnidadMedida] = None) -> None:
        # Validaciones de dominio
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo.")
        if stock_cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        # Atributos internos
        self._nombre = nombre
        self._precio_base = precio_base
        self._stock_cantidad = stock_cantidad
        self._habilitado = True
        self._unidad_venta = unidad_venta
        
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def unidad_venta(self) -> Optional[UnidadMedida]:
        return self._unidad_venta

    @property
    def disponible(self) -> bool:
        return self._habilitado and self._stock_cantidad > 0

    @property
    def precio_publicado(self) -> str:
        if self._unidad_venta:
            return f"$ {self._precio_base:.2f} / {self._unidad_venta.simbolo}"
        return f"$ {self._precio_base:.2f}"