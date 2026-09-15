from typing import Tuple

from ProductoCategoria import ProductoCategoria


class Categoria:
    def __init__(self, nombre: str, descripcion: str = "") -> None:
        self._nombre = nombre
        self._descripcion = descripcion
        self._clasificaciones = []

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

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

    def categorias(self) -> Tuple[ProductoCategoria, ...]:
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> "Categoria":
        for clasificacion in self._clasificaciones:
            if clasificacion.es_principal:
                return clasificacion.categoria
        raise RuntimeError("Invariante roto: No hay categoría principal.")