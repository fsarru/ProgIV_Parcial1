from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple, Protocol


@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str


class Producto(ABC):
    # Corrección: Uso de comillas en "Categoria" y "UnidadMedida" para evitar NameError por declaración tardía
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        categoria_principal: "Categoria",
        unidad_venta: Optional["UnidadMedida"] = None,
    ) -> None:
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
        self._orden_vidriera = None

        # Corrección: El atributo debe llevar el guion bajo interno (_unidad_venta)
        self._unidad_venta = unidad_venta

        # Corrección: El producto fabrica internamente el primer vínculo usando categoria_principal
        self._clasificaciones = []
        self._clasificaciones.append(ProductoCategoria(categoria_principal, True))

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def unidad_venta(self) -> Optional["UnidadMedida"]:
        return self._unidad_venta

    @property
    def disponible(self) -> bool:
        return self._habilitado and self._stock_cantidad > 0

    @property
    def precio_publicado(self) -> str:
        if self._unidad_venta:
            return f"$ {self._precio_base:.2f} / {self._unidad_venta.simbolo}"
        return f"$ {self._precio_base:.2f}"

    def destacar_en_vidriera(self, orden: Optional[int]) -> None:
        if orden is not None and (not isinstance(orden, int) or orden < 1):
            raise ValueError("El orden debe ser un entero positivo.")
        self._orden_vidriera = orden

    def _validar_cantidad(self, cantidad: float) -> None:
        if not isinstance(cantidad, (int, float)) or cantidad < 1 or cantidad % 1 != 0:
            raise ValueError("La cantidad debe ser entera y mayor a 0.")

    def clasificar_en(self, categoria: "Categoria", es_principal: bool = False) -> None:
        for clasificacion in self._clasificaciones:
            if clasificacion.categoria == categoria:
                raise ValueError("El producto ya está clasificado en esta categoría.")

        if es_principal:
            for clasificacion in self._clasificaciones:
                if clasificacion.es_principal:
                    clasificacion._marcar_principal(False)

        # El código cliente pasa la categoría, el producto fabrica el vínculo
        self._clasificaciones.append(ProductoCategoria(categoria, es_principal))

    def categorias(self) -> Tuple["ProductoCategoria", ...]:
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> "Categoria":
        for clasificacion in self._clasificaciones:
            if clasificacion.es_principal:
                return clasificacion.categoria
        raise RuntimeError("Invariante roto: No hay categoría principal.")

    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        pass

    def exportar(self) -> str:
        return f"PROD {self._nombre} | {self.precio_publicado} | Stock: {self._stock_cantidad}"


class Categoria:
    def __init__(self, nombre: str, descripcion: str = "") -> None:
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion


# Corrección: Se eliminó la duplicación de la clase ProductoCategoria. Se conservó esta que tiene la property 'categoria'.
class ProductoCategoria:
    def __init__(self, categoria: Categoria, es_principal: bool) -> None:
        self._categoria = categoria
        self._es_principal = es_principal

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def es_principal(self) -> bool:
        return self._es_principal

    def _marcar_principal(self, valor: bool) -> None:
        self._es_principal = valor


class ProductoCombo(Producto):
    def __init__(
        self,
        nombre: str,
        stock_cantidad: float,
        categoria_principal: Categoria,
        componentes: List[Producto],
        descuento: float,
    ) -> None:
        if len(componentes) < 2:
            raise ValueError("Un combo debe tener al menos 2 componentes.")
        if not (0 <= descuento < 1):
            raise ValueError("El descuento debe estar entre 0 y 0.99.")

        precio_base = sum(c.precio_final(1) for c in componentes) * (1 - descuento)
        super().__init__(nombre, precio_base, stock_cantidad, categoria_principal, None)

        self._componentes = list(componentes)
        self._descuento = descuento

    def componentes(self) -> Tuple[Producto, ...]:
        return tuple(self._componentes)

    def precio_final(self, cantidad: float) -> float:
        self._validar_cantidad(cantidad)
        return self.precio_base * cantidad


class ProductoSimple(Producto):
    def precio_final(self, cantidad: float) -> float:
        self._validar_cantidad(cantidad)
        return self.precio_base * cantidad


class ProductoPorPeso(Producto):
    def precio_final(self, cantidad: float) -> float:
        self._validar_cantidad(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser > 0.")
        return round(self.precio_base * cantidad, 2)


# Requerimiento 4: Protocolo de contrato estructural
class Exportable(Protocol):
    def exportar(self) -> str: ...

def exportar_catalogo(items: List[Exportable]) -> List[str]:
    return [item.exportar() for item in items]
