# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from core.views.mydatatableview import MyDatatable, columns, helpers
from core.views import crud
from core.models import Reglement


class Page(crud.Page):
    model = Reglement
    menu_code = "liste_reglements_especes"
    url_liste = "liste_reglements_especes"
    objet_pluriel = "des règlements en espèces"


class Liste(Page, crud.Liste):
    model = Reglement

    def get_queryset(self):
        return Reglement.objects.select_related("mode", "emetteur", "famille", "payeur").filter(self.Get_filtres("Q"), mode__label__icontains="Espèces")

    def get_context_data(self, **kwargs):
        context = super(Liste, self).get_context_data(**kwargs)
        context['page_titre'] = "Liste des règlements en espèces"
        context['box_titre'] = "Liste des règlements en espèces des familles"
        context['box_introduction'] = "Voici ci-dessous la liste des règlements en espèces des familles."
        context['impression_introduction'] = ""
        context['impression_conclusion'] = ""
        return context

    class datatable_class(MyDatatable):
        filtres = ["fgenerique:famille", "idreglement", "date", "mode__label", "emetteur__nom", "numero_piece", "payeur__nom", "montant"]
        mode = columns.TextColumn("Mode", sources=['mode__label'])
        emetteur = columns.CompoundColumn("Emetteur", sources=['emetteur__nom'])
        famille = columns.TextColumn("Famille", sources=['famille__nom'])
        payeur = columns.TextColumn("Payeur", sources=['payeur__nom'])

        class Meta:
            structure_template = MyDatatable.structure_template
            columns = ["idreglement", "date", "mode", "emetteur", "numero_piece", "famille", "payeur", "montant"]
            processors = {
                'date': helpers.format_date('%d/%m/%Y'),
            }
            ordering = ["date"]
