# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django.urls import reverse_lazy, reverse
from core.views.mydatatableview import MyDatatable, columns, helpers
from core.views import crud
from core.models import Famille, Prestation
from fiche_famille.forms.famille_prestations import Formulaire, FORMSET_DEDUCTIONS
from fiche_famille.views.famille import Onglet
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages


class Page(Onglet):
    model = Prestation
    url_liste = "famille_prestations_liste"
    url_ajouter = "famille_prestations_ajouter"
    url_modifier = "famille_prestations_modifier"
    url_supprimer = "famille_prestations_supprimer"
    url_supprimer_plusieurs = "famille_prestations_supprimer_plusieurs"
    description_liste = "Saisissez ici les prestations de la famille."
    description_saisie = "Saisissez toutes les informations concernant la prestation et cliquez sur le bouton Enregistrer."
    objet_singulier = "une prestation"
    objet_pluriel = "des prestations"

    def get_context_data(self, **kwargs):
        """ Context data spécial pour onglet """
        context = super(Page, self).get_context_data(**kwargs)
        if not hasattr(self, "verbe_action"):
            context['box_titre'] = "Prestations"
        context['onglet_actif'] = "prestations"
        context['boutons_liste'] = [
            {"label": "Ajouter", "classe": "btn btn-success", "href": reverse_lazy(self.url_ajouter, kwargs={'idfamille': self.kwargs.get('idfamille', None)}), "icone": "fa fa-plus"},
        ]
        # Ajout l'idfamille à l'URL de suppression groupée
        context['url_supprimer_plusieurs'] = reverse_lazy(self.url_supprimer_plusieurs, kwargs={'idfamille': self.kwargs.get('idfamille', None), "listepk": "xxx"})
        return context

    def get_form_kwargs(self, **kwargs):
        """ Envoie l'idindividu au formulaire """
        form_kwargs = super(Page, self).get_form_kwargs(**kwargs)
        form_kwargs["idfamille"] = self.Get_idfamille()
        return form_kwargs

    def get_success_url(self):
        """ Renvoie vers la liste après le formulaire """
        url = self.url_liste
        if "SaveAndNew" in self.request.POST:
            url = self.url_ajouter
        return reverse_lazy(url, kwargs={'idfamille': self.kwargs.get('idfamille', None)})



class Liste(Page, crud.Liste):
    model = Prestation
    template_name = "fiche_famille/famille_liste.html"

    def get_queryset(self):
        return Prestation.objects.select_related("individu", "activite", "activite__structure").filter(Q(famille__pk=self.Get_idfamille()) & self.Get_filtres("Q"))

    def get_context_data(self, **kwargs):
        context = super(Liste, self).get_context_data(**kwargs)
        context['impression_introduction'] = ""
        context['impression_conclusion'] = ""
        context['active_checkbox'] = True
        return context

    class datatable_class(MyDatatable):
        filtres = ['idprestation', 'date', 'individu__nom', 'activite__nom', 'label', 'montant']

        check = columns.CheckBoxSelectColumn(label="")
        actions = columns.TextColumn("Actions", sources=None, processor='Get_actions_speciales')

        class Meta:
            structure_template = MyDatatable.structure_template
            columns = ['check', 'idprestation', 'date', 'individu', 'activite', 'label', 'montant']
            #hidden_columns = = ["idprestation"]
            processors = {
                'date': helpers.format_date('%d/%m/%Y'),
            }
            ordering = ['date']

        def Get_actions_speciales(self, instance, *args, **kwargs):
            """ Inclut l'idindividu dans les boutons d'actions """
            view = kwargs["view"]
            kwargs = view.kwargs
            kwargs["pk"] = instance.pk
            if not instance.activite or instance.activite.structure in view.request.user.structures.all():
                # Affiche les boutons d'action si l'utilisateur est associé à la prestation
                html = [
                    self.Create_bouton_modifier(url=reverse(view.url_modifier, kwargs=kwargs)),
                    self.Create_bouton_supprimer(url=reverse(view.url_supprimer, kwargs=kwargs)),
                ]
            else:
                # Afficher que l'accès est interdit
                html = ["<span class='text-red'><i class='fa fa-minus-circle margin-r-5' title='Accès non autorisé'></i>Accès interdit</span>",]
            return self.Create_boutons_actions(html)




class ClasseCommune(Page):
    form_class = Formulaire
    template_name = "parametrage/famille_edit.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(ClasseCommune, self).get_context_data(**kwargs)

        # Traitement du Combi aides
        if self.request.POST:
            context_data['formset_combi'] = FORMSET_DEDUCTIONS(self.request.POST, instance=self.object)
        else:
            context_data['formset_combi'] = FORMSET_DEDUCTIONS(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset_combi = FORMSET_DEDUCTIONS(self.request.POST, instance=self.object)
        if formset_combi.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form))

        # Sauvegarde de l'aide
        self.object = form.save()

        # Sauvegarde des combi
        if formset_combi.is_valid():
            for formline in formset_combi.forms:
                if formline.cleaned_data.get('DELETE') and form.instance.pk:
                    formline.instance.delete()
                if formline.cleaned_data.get('DELETE') == False:
                    instance = formline.save(commit=False)
                    instance.prestation = self.object
                    instance.famille = self.object.famille
                    instance.date = self.object.date
                    instance.save()
                    formline.save_m2m()

        return super().form_valid(form)



class Ajouter(ClasseCommune, crud.Ajouter):
    form_class = Formulaire
    template_name = "fiche_famille/famille_edit.html"


class Modifier(ClasseCommune, crud.Modifier):
    form_class = Formulaire
    template_name = "fiche_famille/famille_edit.html"


class Supprimer(Page, crud.Supprimer):
    template_name = "fiche_famille/famille_delete.html"


class Supprimer_plusieurs(Page, crud.Supprimer_plusieurs):
    template_name = "fiche_famille/famille_delete.html"