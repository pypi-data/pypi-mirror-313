# -*- coding: utf-8 -*-
{
    "name": "crm_metadata",
    "summary": """
        Add metadata to crm lead""",
    "author": "Coopdevs Treball SCCL",
    "website": "",
    "category": "crm",
    "version": "16.0.0.1.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "crm", "metadata"],
    # always loaded
    "data": ["security/ir.model.access.csv", "views/crm_lead.xml"],
    # only loaded in demonstration mode
}
