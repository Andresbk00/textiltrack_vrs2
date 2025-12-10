from django import forms
from .models import Producto, Categoria, MovimientoInventario

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "categoria", "precio", "stock"]


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ["producto", "tipo", "cantidad"]

from django import forms
from .models import ReporteProductoAgotado, Producto

class ReporteProductoAgotadoForm(forms.ModelForm):
    class Meta:
        model = ReporteProductoAgotado
        fields = ['producto', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # SOLO productos agotados
        self.fields['producto'].queryset = Producto.objects.filter(stock=0)

        # Estilos
        self.fields['descripcion'].widget.attrs.update({
            'placeholder': 'Descripción adicional (opcional)',
            'class': 'input-text',
            'rows': 3
        })
