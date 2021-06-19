# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django.urls import reverse_lazy, reverse
from core.views.mydatatableview import MyDatatable, columns, helpers
from core.views import crud
from core.models import ContactUrgence
from fiche_individu.forms.individu_contacts import Formulaire
from fiche_individu.views.individu import Onglet
from django.db.models import Q


class Page(Onglet):
    model = ContactUrgence
    url_liste = "individu_contacts_liste"
    url_ajouter = "individu_contacts_ajouter"
    url_modifier = "individu_contacts_modifier"
    url_supprimer = "individu_contacts_supprimer"
    description_liste = "Saisissez ici les contacts d'urgence et de sortie de l'individu."
    description_saisie = "Saisissez toutes les informations concernant le contact et cliquez sur le bouton Enregistrer."
    objet_singulier = "un contact d'urgence et de sortie"
    objet_pluriel = "des contacts d'urgence et de sortie"

    def get_context_data(self, **kwargs):
        """ Context data spécial pour onglet """
        context = super(Page, self).get_context_data(**kwargs)
        if not hasattr(self, "verbe_action"):
            context['box_titre'] = "Contacts d'urgence et de sortie"
        context['onglet_actif'] = "contacts"
        context['boutons_liste'] = [
            {"label": "Ajouter", "classe": "btn btn-success", "href": reverse_lazy(self.url_ajouter, kwargs={'idindividu': self.Get_idindividu(), 'idfamille': self.kwargs.get('idfamille', None)}), "icone": "fa fa-plus"},
        ]
        return context

    def get_form_kwargs(self, **kwargs):
        """ Envoie l'idindividu au formulaire """
        form_kwargs = super(Page, self).get_form_kwargs(**kwargs)
        form_kwargs["idindividu"] = self.Get_idindividu()
        form_kwargs["idfamille"] = self.Get_idfamille()
        return form_kwargs

    def get_success_url(self):
        """ Renvoie vers la liste après le formulaire """
        url = self.url_liste
        if "SaveAndNew" in self.request.POST:
            url = self.url_ajouter
        return reverse_lazy(url, kwargs={'idindividu': self.Get_idindividu(), 'idfamille': self.kwargs.get('idfamille', None)})



class Liste(Page, crud.Liste):
    model = ContactUrgence
    template_name = "fiche_individu/individu_liste.html"

    def get_queryset(self):
        return ContactUrgence.objects.filter(Q(individu=self.Get_idindividu()) & Q(famille=self.Get_idfamille()) & self.Get_filtres("Q"))

    def get_context_data(self, **kwargs):
        context = super(Liste, self).get_context_data(**kwargs)
        context['impression_introduction'] = ""
        context['impression_conclusion'] = ""
        context['box_conclusion'] = """<a class="btn btn-default" href="%s"><i class="fa fa-download margin-r-5"></i> Importer un contact depuis la fiche d'un autre individu</a>""" % reverse_lazy("individu_contacts_liste", args=(self.kwargs['idfamille'], self.kwargs['idindividu']))
        return context

    class datatable_class(MyDatatable):
        filtres = ["idcontact", "nom", "prenom", "rue_resid", "tel_domicile", "tel_mobile", "tel_travail", "autorisation_sortie", "autorisation_appel"]
        actions = columns.TextColumn("Actions", sources=None, processor='Get_actions_speciales')
        autorisations = columns.TextColumn("Autorisations", sources=["autorisation_sortie", "autorisation_appel"], processor='Get_autorisations')

        class Meta:
            structure_template = MyDatatable.structure_template
            columns = ["idcontact", "nom", "prenom", "tel_domicile", "tel_mobile", "tel_travail", "autorisations", "actions"]
            ordering = ['nom', 'prenom']

        def Get_autorisations(self, instance, *args, **kwargs):
            return instance.Get_autorisations()

        def Get_actions_speciales(self, instance, *args, **kwargs):
            """ Inclut l'idindividu dans les boutons d'actions """
            view = kwargs["view"]
            # Récupération idindividu et idfamille
            kwargs = view.kwargs
            # Ajoute l'id de la ligne
            kwargs["pk"] = instance.pk
            html = [
                self.Create_bouton_modifier(url=reverse(view.url_modifier, kwargs=kwargs)),
                self.Create_bouton_supprimer(url=reverse(view.url_supprimer, kwargs=kwargs)),
            ]
            return self.Create_boutons_actions(html)



class Ajouter(Page, crud.Ajouter):
    form_class = Formulaire
    template_name = "fiche_individu/individu_edit.html"

class Modifier(Page, crud.Modifier):
    form_class = Formulaire
    template_name = "fiche_individu/individu_edit.html"

class Supprimer(Page, crud.Supprimer):
    template_name = "fiche_individu/individu_delete.html"