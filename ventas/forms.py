from django import forms
from .models import Cliente, Pedido, DetallePedido, Cotizacion, DetalleCotizacion, Factura, DetalleFactura

# CLIENTE
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "email", "telefono", "direccion", "documento"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "documento": forms.TextInput(attrs={"class": "form-control"}),
        }

# PEDIDO
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["cliente", "notas"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ["producto", "cantidad"]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control"}),
        }

# COTIZACION
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ["cliente", "detalle", "valor_estimado"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "detalle": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "valor_estimado": forms.NumberInput(attrs={"class": "form-control"}),
        }

# FACTURA
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ["cliente", "descripcion", "monto"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
        }


