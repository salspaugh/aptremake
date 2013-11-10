
import unittest

from composition import *
from data import *
from languages import *


class TestBase(unittest.TestCase):

    def setUp(self):
        self.make_set = Set(name="Make")
        self.make_set.tuples = ["Honda", "Audi", "Dodge", "Nissan"]
        self.make_set.type = Type.nominal
        self.make_set.domain = "Make"
   
        self.type_set = Set()
        self.type_set.tuples = ["suv", "sedan", "coupe"]
        self.type_set.type = Type.nominal
        self.type_set.domain = "Type"
    
        self.price_set = Set()
        self.price_set.tuples = [5000, 10000, 3000, 6000]
        self.price_set.type = Type.quantitative
        self.price_set.domain = "Price"

        self.mileage_set = Set()
        self.mileage_set.tuples = [48500, 32000, 60010, 20500]
        self.mileage_set.type = Type.quantitative
        self.mileage_set.domain = "Mileage"

        self.weight_set = Set()
        self.weight_set.tuples = [400, 600, 800, 500] 
        self.weight_set.type = Type.quantitative
        self.weight_set.domain = "Weight"
        
        self.repair_set = Set()
        self.repair_set.tuples = ["ok", "ok", "good", "bad"]
        self.repair_set.type = Type.ordinal
        self.repair_set.domain = "Repair"
        
        self.nation_set = Set()
        self.nation_set.tuples = ["Korea", "Germany", "US", "Japan"]
        self.nation_set.type = Type.nominal
        self.nation_set.domain = "Nation"
        
        self.price = FunctionalDependency(name="Price")
        self.price.domain = self.make_set
        self.price.range = self.price_set

        self.mileage = FunctionalDependency(name="Mileage")
        self.mileage.domain = self.make_set
        self.mileage.range = self.mileage_set

        self.weight = FunctionalDependency(name="Weight")
        self.weight.domain = self.make_set
        self.weight.range = self.weight_set
        
        self.repair = FunctionalDependency(name="Repair")
        self.repair.domain = self.make_set
        self.repair.range = self.repair_set
        
        self.nation = FunctionalDependency(name="Nation")
        self.nation.domain = self.make_set
        self.nation.range = self.nation_set

        self.type = FunctionalDependency(name="Type")
        self.type.domain = self.make_set
        self.type.range = self.type_set
        self.type.tuples = [("Honda", "sedan"), ("Audi", "sedan"), ("Dodge", "suv"), ("Nissan", "coupe")]


class TestColorExpression(TestBase):

    def setUp(self):
        super(TestColorExpression, self).setUp()
        
    def test_nominal_set(self): 
        assert Color.can_express(self.make_set)
        assert Color.can_express(self.nation_set)

    def test_ordinal_set(self):
        assert not Color.can_express(self.repair_set)

    def test_quantitative_set(self):
        assert not Color.can_express(self.weight_set)

    def test_nominal_nominal_fd(self):      
        assert Color.can_express(self.type)

    def test_nominal_ordinal_fd(self):
        assert not Color.can_express(self.repair)

    def test_nominal_quantitative_fd(self):
        assert not Color.can_express(self.mileage)


class TestHorizontalAxisExpression(TestBase):

    def setUp(self):
        super(TestHorizontalAxisExpression, self).setUp()

    def test_nominal_set(self):
        assert not HorizontalAxis.can_express(self.make_set)

    def test_ordinal_set(self):
        assert not HorizontalAxis.can_express(self.repair_set)

    def test_quantitative_set(self):
        assert not HorizontalAxis.can_express(self.weight_set)

    def test_nominal_nominal_fd(self):
        assert HorizontalAxis.can_express(self.type)

    def test_nominal_quantitative_fd(self):
        assert HorizontalAxis.can_express(self.price)
        assert HorizontalAxis.can_express(self.mileage)

    def test_nominal_ordinal_fd(self):
        assert HorizontalAxis.can_express(self.repair)


class TestVerticalAxisExpression(TestBase):

    def setUp(self):
        super(TestVerticalAxisExpression, self).setUp()

    def test_nominal_set(self):
        assert not VerticalAxis.can_express(self.make_set)

    def test_ordinal_set(self):
        assert not VerticalAxis.can_express(self.repair_set)

    def test_quantitative_set(self):
        assert not VerticalAxis.can_express(self.weight_set)

    def test_nominal_nominal_fd(self):
        assert VerticalAxis.can_express(self.type)

    def test_nominal_quantitative_fd(self):
        assert VerticalAxis.can_express(self.price)
        assert VerticalAxis.can_express(self.mileage)

    def test_nominal_ordinal_fd(self):
        assert VerticalAxis.can_express(self.repair)


class TestComposition(TestBase):
   
    def setUp(self):
        super(TestComposition, self).setUp()
        self.haxis_price = HorizontalAxis.design(self.price)
        self.haxis_mileage = HorizontalAxis.design(self.mileage)
        self.vaxis_price = VerticalAxis.design(self.price)
        self.color_nation = Color.design(self.nation)

    def test_compose_haxis_vaxis(self):
        assert compose([self.haxis_mileage, self.vaxis_price])

    def test_compose_haxis_haxis(self):
        assert not compose([self.haxis_price, self.haxis_mileage])

    def test_compose_haxis_color(self):
        assert compose([self.haxis_price, self.color_nation])

    def test_compose_haxis_vaxis_color(self):
        assert compose([self.haxis_mileage, self.vaxis_price, self.color_nation])

if __name__ == "__main__":
    unittest.main()
