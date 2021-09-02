from dataclasses import dataclass


class OutOfStock(Exception):
    pass


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref, sku, qty, eta):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    def __repr__(self):
        return f'<Batch {self.reference}>'

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self):
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self):
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line):
        return self.sku == line.sku and self.available_quantity >= line.qty


def allocate(line, batches):
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
    batch.allocate(line)
    return batch.reference
