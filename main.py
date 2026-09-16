from catalogo import (
    UnidadMedida, Categoria, Producto, ProductoSimple, 
    ProductoPorPeso, ProductoCombo, exportar_catalogo
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

    # Creación de Productos
    coca_cola = ProductoSimple("Coca Cola 2L", 6500.0, 50, cat_bebidas, u_unidad)
    queso_tybo = ProductoPorPeso("Queso Tybo", 18000.0, 15, cat_fiambreria, u_kilo)
    
    # Composición: Se clasifica nuevamente y se marca como principal
    cat_ofertas = Categoria("Ofertas Semanales")
    coca_cola.clasificar_en(cat_ofertas, es_principal=True)
    print(f"La nueva categoría principal de la Coca es: {coca_cola.categoria_principal().nombre}")

    # Agregación: Creación del combo
    combo_picada = ProductoCombo(
        "Combo Picada Express", 
        stock_cantidad=10, 
        categoria_principal=cat_combos, 
        componentes=[coca_cola, queso_tybo], 
        descuento=0.15
    )

    print("\n--- 2. CÁLCULO DE PRECIOS FINALES ---")
    print(f"{coca_cola.nombre} (2 un.): $ {coca_cola.precio_final(2):.2f}")
    print(f"{queso_tybo.nombre} (0.350 kg): $ {queso_tybo.precio_final(0.350):.2f}")
    print(f"{combo_picada.nombre} (1 combo): $ {combo_picada.precio_final(1):.2f}")

    print("\n--- 3. EXPORTACIÓN POLIMÓRFICA AL PUNTO DE VENTA ---")
    ficha_externa = FichaPuntoDeVenta("POS-001", "Caja Registradora Principal")
    
    # Lista combinada que cumple con el Protocol 'Exportable'
    catalogo_items = [coca_cola, queso_tybo, combo_picada, ficha_externa]
    
    resultado_exportacion = exportar_catalogo(catalogo_items)
    for linea in resultado_exportacion:
        print(linea)

if __name__ == "__main__":
    main()