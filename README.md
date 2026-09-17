# Primera Evaluación Parcial — Programación IV
## Food Store — Catálogo de productos

Tecnicatura Universitaria en Programación (UTN) — Modalidad a distancia.

# *Alumno*: Franco Sarrú


## Descripción

Modelo de catálogo para un comercio (Food Store) que vende productos por
pieza, por peso y en combos, con clasificación en categorías y exportación
unificada hacia un sistema de punto de venta de terceros.

## Estructura del proyecto

| Archivo | Qué resuelve |
|---|---|
| `catalogo.py` | Dominio completo: `Producto` (ABC), `ProductoSimple`, `ProductoPorPeso`, `ProductoCombo`, `Categoria`, `ProductoCategoria`, `UnidadMedida`, y el contrato `Exportable` (Protocol). |
| `libreria_externa.py` | `FichaPuntoDeVenta`, clase de un tercero — se entrega sin modificar. |
| `main.py` | Demo ejecutable: arma el catálogo, clasifica productos, calcula precios, exporta todo junto con una `FichaPuntoDeVenta`, y deja a la vista la falla temprana, la composición y la agregación. |
| `uml/modelo_final.md` | Diagrama de clases final (Mermaid), reflejando la decisión sobre `ProductoDestacado`. |

## Decisiones de diseño

- **`ProductoDestacado`** no se mantuvo como subclase de `Producto`: "estar
  destacado" no cambia el tipo de venta del producto (un producto destacado
  sigue siendo `ProductoSimple`, `ProductoPorPeso` o `ProductoCombo`), así que
  se resolvió como un atributo más (`_orden_vidriera`) + property
  (`orden_vidriera`) + método (`destacar_en_vidriera()`) directamente en
  `Producto` — el mismo patrón que `_habilitado`/`disponible`/`habilitar()`.
- **`Exportable`** se implementó como `typing.Protocol` en vez de `ABC`,
  porque `FichaPuntoDeVenta` no puede modificarse ni heredar de nada propio;
  el `Protocol` permite conformidad estructural sin tocar la librería externa.
- Las relaciones estructurales se distinguen por **quién construye la parte**
  y **qué le pasa al todo desaparecer**: composición (`Producto`—`ProductoCategoria`,
  el producto fabrica el vínculo), agregación (`ProductoCombo`—componentes,
  se reciben ya construidos y sobreviven al combo) y asociación
  (`Producto`—`UnidadMedida`, ninguno depende del otro).

## Cómo ejecutarlo

Requiere Python 3.12 o superior, sin dependencias externas.

```bash
python main.py
```

La salida muestra, en orden: la falla temprana al instanciar una clase
abstracta incompleta, la clasificación de productos con reasignación de
categoría principal, la demostración de agregación (con `weakref`, probando
que los componentes de un combo sobreviven a su eliminación), el cálculo de
precios finales con distintas cantidades, y la exportación conjunta de
productos propios junto con una ficha de punto de venta externa.