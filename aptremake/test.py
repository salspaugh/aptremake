
import unittest

from plantree import *
from composition import *
from metadata import *
from languages import *
from apt import generate_presentation

CARS = "/Users/salspaugh/classes/visualization/project/aptremake/data/cars.spec"

class TestBase(unittest.TestCase):

    def setUp(self):
        self.data = read_data(CARS) 

class TestColorExpression(TestBase):

    def setUp(self):
        super(TestColorExpression, self).setUp()
        
    def test_nominal_set(self): 
        assert Color.can_express(self.data["Nation"])

    def test_ordinal_set(self):
        assert Color.can_express(self.data["Repair"])

    def test_quantitative_set(self):
        assert not Color.can_express(self.data["Weight"])

    def test_nominal_nominal_fd(self):      
        assert Color.can_express(self.data["Car nationality for 1979"])

    def test_nominal_ordinal_fd(self):
        assert Color.can_express(self.data["Repair record for 1979"])

    def test_nominal_quantitative_fd(self):
        assert not Color.can_express(self.data["Car mileage for 1979"])


class TestHorizontalAxisExpression(TestBase):

    def setUp(self):
        super(TestHorizontalAxisExpression, self).setUp()

    def test_nominal_set(self):
        assert not HorizontalAxis.can_express(self.data["Car"])

    def test_ordinal_set(self):
        assert not HorizontalAxis.can_express(self.data["Repair"])

    def test_quantitative_set(self):
        assert not HorizontalAxis.can_express(self.data["Weight"])

    def test_nominal_nominal_fd(self):
        assert HorizontalAxis.can_express(self.data["Car nationality for 1979"])

    def test_nominal_quantitative_fd(self):
        assert HorizontalAxis.can_express(self.data["Car price for 1979"])
        assert HorizontalAxis.can_express(self.data["Car mileage for 1979"])

    def test_nominal_ordinal_fd(self):
        assert HorizontalAxis.can_express(self.data["Repair record for 1979"])


class TestVerticalAxisExpression(TestBase):

    def setUp(self):
        super(TestVerticalAxisExpression, self).setUp()

    def test_nominal_set(self):
        assert not VerticalAxis.can_express(self.data["Car"])

    def test_ordinal_set(self):
        assert not VerticalAxis.can_express(self.data["Repair"])

    def test_quantitative_set(self):
        assert not VerticalAxis.can_express(self.data["Weight"])

    def test_nominal_nominal_fd(self):
        assert VerticalAxis.can_express(self.data["Car nationality for 1979"])

    def test_nominal_quantitative_fd(self):
        assert VerticalAxis.can_express(self.data["Car price for 1979"])
        assert VerticalAxis.can_express(self.data["Car mileage for 1979"])

    def test_nominal_ordinal_fd(self):
        assert VerticalAxis.can_express(self.data["Repair record for 1979"])

class TestComposition(TestBase):
   
    def setUp(self):
        super(TestComposition, self).setUp()
        

        self.haxis_price = HorizontalAxis.design(self.data["Car price for 1979"])
        self.haxis_mileage = HorizontalAxis.design(self.data["Car mileage for 1979"])
        self.haxis_car = HorizontalAxis.design(self.data["Car"])

        self.vaxis_price = VerticalAxis.design(self.data["Car price for 1979"])
        self.vaxis_mileage = VerticalAxis.design(self.data["Car mileage for 1979"])
        self.vaxis_weight = VerticalAxis.design(self.data["Car weight for 1979"])
        
        self.color_nationality = Color.design(self.data["Car nationality for 1979"])
        self.color_repair = Color.design(self.data["Repair record for 1979"])

    def test_compose_haxis_vaxis(self):
        assert compose([self.haxis_mileage, self.vaxis_price])

    def test_compose_haxis_haxis(self):
        assert not compose([self.haxis_price, self.haxis_mileage])

    def test_compose_haxis_color(self):
        assert compose([self.haxis_price, self.color_nationality])

    def test_compose_haxis_vaxis_color(self):
        assert compose([self.haxis_mileage, self.vaxis_price, self.color_nationality])

    def test_compose_haxis_vaxis_color_color(self):
        assert not compose([self.haxis_price, self.vaxis_mileage, self.color_nationality, self.color_repair])

class TestSelections(TestBase):
    
    def setUp(self):
        super(TestSelections, self).setUp()

    def test_mileagefd_selections(self):
        p = PartitionTreeNode([self.data["Car mileage for 1979"]])
        p.generate_children()

class TestDesign(TestBase):

    def setUp(self):
        super(TestDesign, self).setUp()
        self.mileage_design = generate_presentation([self.data["Car mileage for 1979"]])
    
    def test_mileagefd_design(self):
        print self.mileage_design

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner(verbosity=2).run(TestDesign("test_mileagefd_design"))
