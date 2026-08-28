"""helper function for the "Order" test"""

def create_order_objects(profile_business, profile_customer, Offer, OfferDetail, Order, range_stop = 12):
    """Created Order Objects"""
    for offer_number in range(0, range_stop -1):
        offer = Offer.objects.all()[offer_number]
        for order_number in range(0, (range_stop -1)*3):
            offer_detail = OfferDetail.objects.all()[order_number]
            Order.objects.create(customer_user= profile_customer, business_user = profile_business, offer = offer, offer_detail = offer_detail)

def create_order_selected_status_objects(profile_business, profile_customer, Offer, OfferDetail, Order, range_stop = 12):
    """Created Order Objects with status 'in progress' or 'completed'"""
    counter = 0
    for offer_number in range(0, range_stop -1):
        offer = Offer.objects.all()[offer_number]
        for order_number in range(0, 3):
            counter += 1
            offer_detail = OfferDetail.objects.all()[order_number]

            if counter %3 == 0:
                status = "in_progress"
            else:
                status = "completed"

            Order.objects.create(customer_user= profile_customer, business_user = profile_business, offer = offer, offer_detail = offer_detail, status = status)