from django.shortcuts import render

from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DeleteView

from .models import Product, ProductIndex
from .forms import ProductForm, ProductTagFormSet

# — Listado usando la VIEW unmanaged —
class ProductIndexListView(ListView):
    model               = ProductIndex
    template_name       = 'crud/product_list.html'
    context_object_name = 'products'

# ——————————————————————————————————————————————————————————————————————————
class ProductCreateView(View):
    template_name = 'crud/product_form.html'

    def get(self, request):
        form    = ProductForm()
        # Al crear, le pasamos un objeto NO salvado; initial_forms=0
        formset = ProductTagFormSet(instance=Product())
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
        })

    def post(self, request):
        form = ProductForm(request.POST)
        # IMPORTANTE: no salvamos aún el form, solo creamos el objeto en memoria
        if form.is_valid():
            product = form.save(commit=False)
            # Ahora instanciamos el formset con el mismo objeto
            formset = ProductTagFormSet(request.POST, instance=product)
            if formset.is_valid():
                # Primero guardamos el product para que tenga PK…
                product.save()
                # …y luego guardamos el formset (que usa product.pk)
                formset.save()
                return redirect('product_list')

        # Si algo falla, recargamos tanto form como formset con errores
        else:
            # si el form no era válido, necesitamos un formset vacío para mostrar errores genéricos
            formset = ProductTagFormSet(request.POST, instance=Product())

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
        })



# ——————————————————————————————————————————————————————————————————————————
class ProductUpdateView(View):
    template_name = 'crud/product_form.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form    = ProductForm(instance=product)
        # Para update pasamos siempre instance=product
        formset = ProductTagFormSet(instance=product)
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
        })

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form    = ProductForm(request.POST, instance=product)
        formset = ProductTagFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()       # ya hay instancia, actualiza el product
            formset.save()    # aplica adds/changes/deletes a ProductTag
            return redirect('product_list')

        # si hay errores
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
        })

# — Eliminar Product (en cascada borrará sus ProductTag gracias a on_delete=CASCADE) —
class ProductDeleteView(DeleteView):
    model         = Product
    template_name = 'crud/product_confirm_delete.html'
    success_url   = reverse_lazy('product_list')
