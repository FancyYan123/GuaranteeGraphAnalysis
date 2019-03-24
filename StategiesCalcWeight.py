# -*- coding: utf-8 -*-

"""
TODO: accomplish these methods according to expert evaluation
"""
from enum import Enum

loan_state = Enum('loan_state', ('due', 'overdue', 'during_duration'))


class CalcWeight(object):
    @classmethod
    def calc_weight(cls, guarantee_sum: int, duration: int, state: loan_state):
        return 0


class GeneralGuarantee(CalcWeight):
    """一般保证"""

    @classmethod
    def calc_weight(cls, guarantee_sum: int, duration: int, state: loan_state):
        return guarantee_sum


class JointLiabilityGuaranteeCalcWeight(CalcWeight):
    """连带责任保证"""

    @classmethod
    def calc_weight(cls, guarantee_sum: int, duration: int, state: loan_state):
        return guarantee_sum


class PledgeCalcWeight(CalcWeight):
    """抵押"""

    @classmethod
    def calc_weight(cls, guarantee_sum: int, duration: int, state: loan_state):
        return guarantee_sum


class MortgageCalcWeight(CalcWeight):
    """质押"""

    @classmethod
    def calc_weight(cls, guarantee_sum: int, duration: int, state: loan_state):
        pass


class LienCalcWeight(CalcWeight):
    """留置"""

    @classmethod
    def calc_weight(cls, guarantee_sum: int, duration: int, state: loan_state):
        pass


class EarnestCalcWeight(CalcWeight):
    """定金"""

    @classmethod
    def calc_weight(cls, guarantee_sum: int, duration: int, state: loan_state):
        pass
