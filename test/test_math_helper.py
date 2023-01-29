
from pytest import fixture
import datetime as dt
from wss_backtesting.math_helper import MathHelper
import pytest


@fixture
def math_helper():        
    return MathHelper()

def test_variation_normal_numbers(math_helper):
    var = math_helper.variation(10,15)
    assert var == 50

def test_variation_final_with_zero(math_helper):
    var = math_helper.variation(10,0)
    assert var == -100
    
def test_variation_initial_with_zero(math_helper):  
    with pytest.raises(ZeroDivisionError):
        math_helper.variation(0,10) == 100
  