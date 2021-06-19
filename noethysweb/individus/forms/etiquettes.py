# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Hidden, Submit, HTML, Row, Column, Fieldset, Div, ButtonHolder
from crispy_forms.bootstrap import Field, PrependedText
from core.utils.utils_commandes import Commandes
from django_select2.forms import Select2Widget
from core.models import ModeleDocument


class Formulaire_categorie(forms.Form):
    categorie = forms.ChoiceField(label="Catégorie", choices=[("individu", "Individus"), ("famille", "Familles")], required=False)

    def __init__(self, *args, **kwargs):
        categorie = kwargs.pop("categorie", "individu")
        super(Formulaire_categorie, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form_categorie'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.form_show_labels = False

        self.fields["categorie"].initial = categorie

        self.helper.layout = Layout(
            Field('categorie'),
            HTML("""<button type="submit" name="appliquer_date" class="btn btn-default btn-block btn-flat btn-sm" style="margin-top: -5px;" title="Appliquer">Appliquer</button>"""),

        )


class Formulaire_parametres(forms.Form):
    modele = forms.ModelChoiceField(label="Modèle", widget=Select2Widget({"lang": "fr"}), queryset=ModeleDocument.objects.all(), required=False)
    largeur = forms.IntegerField(label="Largeur de la page", initial=210, min_value=0, required=True)
    hauteur = forms.IntegerField(label="Hauteur de la page", initial=297, min_value=0, required=True)
    espace_vertical = forms.IntegerField(label="Espace vertical", initial=5, min_value=0, required=True)
    espace_horizontal = forms.IntegerField(label="Espace horizontal", initial=5, min_value=0, required=True)
    marge_haut = forms.IntegerField(label="Marge haut", initial=10, min_value=0, required=True)
    marge_bas = forms.IntegerField(label="Marge bas", initial=5, min_value=0, required=True)
    marge_gauche = forms.IntegerField(label="Marge gauche", initial=10, min_value=0, required=True)
    marge_droite = forms.IntegerField(label="Marge droite", initial=10, min_value=0, required=True)
    nbre_copies = forms.IntegerField(label="Nbre copies", initial=1, min_value=1, required=True)
    contours = forms.BooleanField(label="Afficher les contours", required=False, initial=True)
    reperes = forms.BooleanField(label="Afficher les repères de découpe", required=False, initial=True)

    def __init__(self, *args, **kwargs):
        categorie = kwargs.pop("categorie")
        super(Formulaire_parametres, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form_parametres'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["largeur"].label = "Options"
        self.fields["hauteur"].label = False
        self.fields["espace_vertical"].label = False
        self.fields["espace_horizontal"].label = False
        self.fields["marge_haut"].label = False
        self.fields["marge_bas"].label = False
        self.fields["marge_gauche"].label = False
        self.fields["marge_droite"].label = False
        self.fields["nbre_copies"].label = False

        self.fields['modele'].queryset = ModeleDocument.objects.filter(categorie=categorie).order_by("nom")

        self.helper.layout = Layout(
            Field('modele'),
            PrependedText('largeur', 'Largeur'),
            PrependedText('hauteur', 'Hauteur'),
            PrependedText('espace_vertical', 'Espace vertical'),
            PrependedText('espace_horizontal', 'Espace horizontal'),
            PrependedText('marge_haut', 'Marge haut'),
            PrependedText('marge_bas', 'Marge bas'),
            PrependedText('marge_gauche', 'Marge gauche'),
            PrependedText('marge_droite', 'Marge droite'),
            PrependedText('nbre_copies', 'Nbre copies'),
            Field('contours'),
            Field('reperes'),
        )