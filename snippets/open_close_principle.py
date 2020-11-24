from abc import ABC, abstractmethod
from datetime import datetime

# examples translated to Python from https://bottega.com.pl/pdf/materialy/receptury/ocp.pdf


def generate_offer(order: Order) -> Offer:
    offer = Offer(order.client)

    for product in order.get_ordered_products():
        product_price = product.price
        if product.quantity > 10:
            product_price = product.price * 0.9

        offer.addItem(product, product_price)

    return offer


def generate_offer(order: Order) -> Offer:
    offer = Offer(order.client)

    for product in order.get_ordered_products():
        product_price = product.price

        if order.client.is_regular:
            # imagine more complex logic here
            if product.quantity > 10:
                discount = 0.9  # complicated logic
                product_price = product_price * discount
            elif product.quantity > 5:
                product_price = product_price * 0.95
        elif order.client.is_vip:
            discount = 0.9  # complicated logic
            product_price = product_price * discount
        else:
            if product.quantity > 15:
                # imagine more complex logic here
                product_price = product_price * 0.05

        offer.addItem(product, product_price)

    return offer


# HOW
class DiscountPolicy(ABC):
    @abstractmethod
    def calculate(self, product: Product) -> Price:
        pass


class RegularClientDiscountPolicy(DiscountPolicy):
    def calculate(self, product: Product) -> Price:
        # complex logic
        if product.quantity > 10:
            discount = 0.9  # complicated logic
            return product_price * discount
        elif product.quantity > 5:
            return product_price * 0.95


class VIPClientDiscountPolicy(DiscountPolicy):
    def calculate(self, product: Product) -> Price:
        # complex logic
        return product.price * 0.9


class NewClientDiscountPolicy(DiscountPolicy):
    def calculate(self, product: Product) -> Price:
        # complex logic
        if product.quantity > 15:
            return product.price * 0.95


# WHY
class BidderFactory:
    def create(self, client, *args) -> Bidder:
        if client.is_vip:
            return Bidder(VIPClientDiscountPolicy())
        if client.is_regular:
            return Bidder(RegularClientDiscountPolicy())
        return Bidder(NewClientDiscountPolicy())


# WHAT is stable. It shouldn't change in the feature.
class Bidder:
    def __init__(self, discount_policy: DiscountPolicy):
        self.discount_policy = discount_policy

    def generate_offer(self, order: Order) -> Offer:
        offer = Offer(client)

        for product in order.get_ordered_products():
            offer.add_item(product, self.discount_policy.calculate(product))

        return offer


def new_client_discount_calculator(product):
    return


def vip_client_discount_calculator(product):
    return


def discount_calculator_factory(client):
    if client.is_vip:
        return vip_client_discount_calculator
    return new_client_discount_calculator


def generate_offer(order: Order, discount_calculator=new_client_discount_calculator) -> Offer:
    offer = Offer(client)

    for product in order.get_ordered_products():
        offer.add_item(product, discount_calculator(product))

    return offer


generate_offer(order, discount_calculator_factory(client))


# anty-pattern
def naive_implementation(order: Order) -> Invoice:
    client = order.get_client()
    invoice = Invoice(client)

    for product in order.get_ordered_products():
        net = product.get_efffective_cost()

        if client.is_vip:
            tax = net * 0.1
            # bla bla logic form tax calculations
            if client.annual_transaction > 1000:
                pass
            elif client.annual_transaction < 500 and phase_of_the_moon.is_favorable:
                pass

        elif client.is_enemy:
            tax = net * 1000
            # bla bla logic form tax calculations
        invoice_line = InvoiceLine(product, product.getQuantity(), net, tax)

        invoice.addItem(invoice_line)

    return invoice


class DiscountFactory:
    def create(self, *args) -> "DiscountStrategy":
        pass


class DiscountStrategy:
    def calculate(self, product: Product) -> Discount:
        pass


class Reservation:
    def __init__(self):
        self.products: List[Product] = []

    def generate_pricing_plan(self, client, discount_strategy: DiscountStrategy) -> PricingPlan:
        pricing_plan = PricingPlan(client)

        for product in self.products:
            pricing_plan.add_item(product, discount_strategy.calculate(product))

        return pricing_plan


reservation = Reservation()
client = Client()
discount_strategy = DiscountFactory.create(client, datetime.now())
reservation.generate_pricing_plan(client, discount_strategy)

# or inject policy as argument and use factory for building whole object


class TaxPolicy(ABC):
    def calculate_tax(self, product, net):
        pass


class BookKeeperFactory:
    def create(self, client, *args):
        if client.is_vip():
            return BookKeeper(BetterTaxPolicy())
        return BookKeeper(RegularTaxPolicy())


class BookKeeper:
    def __init__(self, tax_policy: TaxPolicy):
        self.tax_policy = tax_policy

    def issuance(self, order: Order) -> Invoice:
        invoice = Invoice(order.getClient())

        for product in order.getOrderedProducts():
            net = product.getEffectiveCost()
            tax = self.tax_policy.calculate_tax(product.getType(), net)

            invoice_line = InvoiceLine(product, product.getQuantity(), net, tax)

            invoice.addItem(invoice_line)

        return invoice
