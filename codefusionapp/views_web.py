from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from .models import Country


# ──────────────────────────  Form  ──────────────────────────
class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = "__all__"



# ──────────────────────  Country details  ───────────────────
@login_required
def country_detail_view(request, pk):
    c = get_object_or_404(Country, pk=pk)
    same_region = Country.objects.filter(region=c.region).exclude(pk=pk)
    return render(request, 'codefusionapp/detail.html', {
        'c': c,
        'same_region': same_region,
    })

# ───────────────────  List & Search view  ───────────────────

@login_required
def countries_view(request):
    q = request.GET.get('q', '')
    qs = Country.objects.filter(name__icontains=q).order_by('name')
    return render(request, 'codefusionapp/countries.html', {
        'countries': qs,
        'query': q,
        'languages': _language_codes(Country.objects.all()),   # full list
    })

@login_required
def language_view(request, code):
    qs = Country.objects.filter(languages__icontains=code)
    return render(request, 'codefusionapp/countries.html', {
        'countries': qs,
        'header': f"Countries that speak “{code}”",
        'languages': _language_codes(Country.objects.all()),   # keep dropdown
        'query': '',
    })

@login_required
def regional_view(request, pk):
    country = get_object_or_404(Country, pk=pk)
    same = Country.objects.filter(region=country.region).exclude(pk=pk)
    return render(request, 'codefusionapp/countries.html', {
        'countries': same,
        'header': f"Same-regional countries as {country.name}",
        'languages': _language_codes(Country.objects.all()),
        'query': '',
    })


# ───────────────────────  CRUD helpers  ─────────────────────
@login_required
def add_country(request):
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = CountryForm()
    return render(request, 'codefusionapp/form.html',
                  {'form': form, 'mode': 'Add'})


@login_required
def edit_country(request, pk):
    c = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        form = CountryForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = CountryForm(instance=c)
    return render(request, 'codefusionapp/form.html',
                  {'form': form, 'mode': 'Edit'})


@login_required
def delete_country(request, pk):
    c = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        c.delete()
        return redirect('countries')
    return render(request, 'codefusionapp/confirm_delete.html', {'c': c})


def _language_codes(qs):
    """Return sorted unique language codes from a queryset."""
    return sorted({code for c in qs for code in (c.languages or {}).keys()})
