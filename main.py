import weakref

from catalogo import (
    Categoria,
    Producto,
    ProductoCombo,
    ProductoPorPeso,
    ProductoSimple,
    UnidadMedida,
    exportar_catalogo,
)
from libreria_externa import FichaPuntoDeVenta


def main():
    print("--- 1. CONFIGURACIÓN DEL CATÁLOGO ---")
    cat_bebidas = Categoria("Bebidas", "Gaseosas, jugos y aguas")
    cat_fiambreria = Categoria("Fiambrería")
    cat_combos = Categoria("Combos Especiales")
    
    u_unidad = UnidadMedida("Unidad", "u", "unidad")
    u_kilo = UnidadMedida("Kilogramo", "kg", "masa")

    # Fallo temprano: Demostración de prohibición de instanciar ABC
    try:
        class ProductoIncompleto(Producto):
            pass
        p_falla = ProductoIncompleto("Test", 10.0, 5.0, cat_bebidas)
    except TypeError as e:
        print(f"[OK] Fallo temprano al instanciar ABC/incompleta: {e}")

    # Creación de Productos (Cumpliendo estrictamente "al menos 4 productos")
    coca_cola = ProductoSimple("Coca Cola 2L", 2500.0, 50, cat_bebidas, u_unidad)
    agua_mineral = ProductoSimple("Agua Mineral 1.5L", 1500.0, 30, cat_bebidas, u_unidad)
    queso_tybo = ProductoPorPeso("Queso Tybo", 8000.0, 15, cat_fiambreria, u_kilo)
    salamin = ProductoPorPeso("Salamin", 12000.0, 10, cat_fiambreria, u_kilo)
    
    # Composición: Se clasifica nuevamente y se marca como principal
    cat_ofertas = Categoria("Ofertas Semanales")
    coca_cola.clasificar_en(cat_ofertas, es_principal=True)
    print(f"La nueva categoría principal de la Coca es: {coca_cola.categoria_principal().nombre}")

    print("\n--- 2. DEMOSTRACIÓN DE AGREGACIÓN (CON WEAKREF) ---")
    
    # 1) Creamos referencias débiles a los componentes sueltos
    ref_queso = weakref.ref(queso_tybo)
    ref_salamin = weakref.ref(salamin)

    # 2) Armamos el combo pasándole los componentes (Agregación)
    combo_picada = ProductoCombo(
        "Combo Picada Express", 
        stock_cantidad=10, 
        categoria_principal=cat_combos, 
        componentes=[queso_tybo, salamin], 
        descuento=0.10
    )
    print(f"Se creó el '{combo_picada.nombre}' con los componentes:")
    for c in combo_picada.componentes():
        print(f" - {c.nombre}")

    # 3) Destruimos el combo explícitamente
    print("\nSimulando la eliminación del 'Combo Picada Express' (del combo_picada)...")
    del combo_picada

    # 4) Verificamos la supervivencia consultando las referencias débiles
    if ref_queso() is not None and ref_salamin() is not None:
        print("¡Comprobación exitosa! Las referencias débiles confirman que los componentes SOBREVIVIERON.")
        print(f"Objetos intactos en memoria: {ref_queso().nombre} y {ref_salamin().nombre}")
    else:
        print("Error: Los componentes fueron destruidos por el Garbage Collector.")

    # 5) Demostramos la reagrupación
    combo_mega_picada = ProductoCombo(
        "Mega Picada + Bebidas",
        stock_cantidad=5,
        categoria_principal=cat_combos,
        componentes=[queso_tybo, salamin, coca_cola, agua_mineral],
        descuento=0.20
    )
    print(f"\nSe los volvió a agrupar con éxito en uno nuevo: '{combo_mega_picada.nombre}'")

    print("\n--- 3. CÁLCULO DE PRECIOS FINALES ---")
    print(f"{coca_cola.nombre} (2 un.): $ {coca_cola.precio_final(2):.2f}")
    print(f"{queso_tybo.nombre} (0.350 kg): $ {queso_tybo.precio_final(0.350):.2f}")
    print(f"{combo_mega_picada.nombre} (1 combo): $ {combo_mega_picada.precio_final(1):.2f}")

    print("\n--- 4. EXPORTACIÓN POLIMÓRFICA AL PUNTO DE VENTA ---")
    ficha_externa = FichaPuntoDeVenta("POS-001", "Caja Registradora Principal")
    
    # El catálogo ahora cuenta con los 4 productos sueltos exigidos y el combo final
    catalogo_items = [coca_cola, agua_mineral, queso_tybo, salamin, combo_mega_picada, ficha_externa]
    
    resultado_exportacion = exportar_catalogo(catalogo_items)
    for linea in resultado_exportacion:
        print(linea)

if __name__ == "__main__":
    main()