def create_order_objects(self, Offer, OfferDetail, Order, range_stop = 12):
    for offer_number in range(0, range_stop -1):
        offer = Offer.objects.all()[offer_number]
        for order_number in range(0, (range_stop -1)*3):
            offer_detail = OfferDetail.objects.all()[order_number]
            Order.objects.create(customer_user= self.profile_customer, business_user = self.profile, offer = offer, offer_detail = offer_detail)