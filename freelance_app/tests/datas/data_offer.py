test_offer_list_offer_type_double_value_post_400_data = {
    "title": "Grafikdesign-Paket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
                ],
            "offer_type": "basic"
        },
        {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200.99,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "basic"
        },
        {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
        }
    ]
}


test_offer_list_no_three_details_objects_post_400_data = {
    "title": "Grafikdesign-Paket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
                ],
            "offer_type": "basic"
        },
        {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200.99,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
        }
    ]
}


test_offer_list_not_a_valid_choice_post_400_data = {
    "title": "Grafikdesign-Paket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
                ],
            "offer_type": "basiccccc"
        },
        {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200.99,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
        },
        {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
        }
    ]
}


test_offer_list_post_401_data = {
    "title": "Grafikdesign-Paket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "basic"
        },
        {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200.99,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
        },
        {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
        }
    ]
}


test_offer_list_post_403_data = {
    "title": "Grafikdesign-Paket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "basic"
        },
        {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200.99,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
        },
        {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
        }
    ]
}


test_profile_detail_post_201_data = {
    "title": "Grafikdesign-Paket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "basic"
        },
        {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200.99,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
        },
        {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
        }
    ]
}


test_offer_detail_without_offer_type_patch_400_data = {
    "title": "Updated Grafikdesign-Paket",
    "details": [
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Flyer"
            ],
        }
    ]
}


test_offer_detail_with_wrong_value_patch_400_data = {
    "title": "Updated Grafikdesign-Paket",
    "details": [
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Flyer"
            ],
            "offer_type": "basicccccc"
        }
    ]
}


test_offer_detail_multiple_offer_type_value_patch_400_data = {
    "title": "Updated Grafikdesign-Paket",
    "details": [
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Flyer"
            ],
            "offer_type": "basic"
        },
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Flyer"
            ],
            "offer_type": "basic"
        },
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Flyer"
            ],
            "offer_type": "standard"
        }
    ]
}


test_offer_detail_patch_401_data = {
    "title": "Updated Grafikdesign-Paket",
    "details": [
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Flyer"
            ],
            "offer_type": "basic"
        }
    ]
}


test_offer_detail_patch_403_data = {
    "title": "Updated Grafikdesign-Paket",
    "details": [
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Flyer"
            ],
            "offer_type": "basic"
        }
    ]
}


test_offer_detail_patch_404_data = {
    "title": "Updated Grafikdesign-Paket",
    "details": [
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Flyer"
            ],
            "offer_type": "basic"
        }
    ]
}


test_offer_detail_with_details_patch_200_data = {
    "title": "Updated Grafikdesign-Paket",
    "details": [
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Visitenkarte",
            ],
            "offer_type": "basic"
        },
        {
            "title": "Standard Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
        }
    ]
}


test_offer_detail_without_details_patch_200_data = {
    "title": "Updated Grafikdesign-Paket"
}


def create_offer_objects(profile_business, Offer, OfferDetail, range_stop = 12):
    for offer_number in range(1, range_stop):
        offer = Offer.objects.create(user= profile_business, title= f"Grafikdesign-Paket{offer_number}", image= None, description= f"Ein umfassendes Grafikdesign-Paket für Unternehmen{offer_number}.")
        OfferDetail.objects.create(title= f"Basic Design{offer_number}", revisions= 2, delivery_time_in_days= 5, price= 100.99, features= [f"Logo Design{offer_number}", f"Visitenkarte{offer_number}"], offer_type= "basic", offer= offer)
        OfferDetail.objects.create(title= f"Standard Design{offer_number}", revisions= 5, delivery_time_in_days= 7, price= 200, features= [f"Logo Design{offer_number}", f"Visitenkarte{offer_number}", f"Briefpapier{offer_number}"], offer_type= "standard", offer= offer)
        OfferDetail.objects.create(title= f"Premium Design{offer_number}", revisions= 10, delivery_time_in_days= 10, price= 500, features= [f"Logo Design{offer_number}", f"Visitenkarte{offer_number}", f"Briefpapier{offer_number}", f"Flyer{offer_number}"], offer_type= "premium", offer= offer)
        