from abc import ABC
from datetime import datetime

# examples translated to Python from https://bottega.com.pl/pdf/materialy/receptury/ocp.pdf


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
        self.products: List[Product]

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
