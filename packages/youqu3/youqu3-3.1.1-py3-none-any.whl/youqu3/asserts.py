#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

from funnylog2 import log

@log
class Asserts():

    @staticmethod
    def assert_equal(expect, actual):
        """断言预期值: {{expect} 与 实际值 {{actual}} 相等"""
        if expect != actual:
            raise AssertionError(f"预期值: {expect} 与 实际值 {actual} 不相等")

    @staticmethod
    def assert_not_equal(expect, actual):
        """断言预期值: {{expect}} 与 实际值 {{actual}} 不相等"""
        if expect == actual:
            raise AssertionError(f"预期值: {expect} 与 实际值 {actual} 相等")

    @staticmethod
    def assert_in(target: str, pool: str):
        """断言: {{target}} 在 {{pool}} 中"""
        if target not in pool:
            raise AssertionError(f": {target} 不在 {pool} 中")

    @staticmethod
    def assert_not_in(target: str, pool: str):
        """断言: {{target}} 不在 {{pool}} 中"""
        if target in pool:
            raise AssertionError(f": {target} 在 {pool} 中")

    @staticmethod
    def assert_sequence_in(target: list, pool: list):
        """断言: {{target}} 在 {{pool}} 中"""
        for i in target:
            if i not in pool:
                raise AssertionError(f"{pool}中不存在{i}")

    @staticmethod
    def assert_sequence_not_in(target: list, pool: list):
        """断言: {{target}} 不在 {{pool}} 中"""
        for i in target:
            if i in pool:
                raise AssertionError(f"{pool}中存在{i}")

    @staticmethod
    def assert_true(expect):
        """断言 {{expect}} 结果为真"""
        if not expect:
            raise AssertionError(f"{expect} 不为真")

    @staticmethod
    def assert_false(expect):
        """断言: {{expect}} 结果为假"""
        if expect:
            raise AssertionError(f": {expect} 不为假")

    @staticmethod
    def assert_any(expect):
        """断言: 任一 {{expect}} 结果为真"""
        if not any(expect):
            raise AssertionError(f": {expect} 均不为真")

    @staticmethod
    def assert_all(expect):
        """断言: 所有 {{expect}} 结果为真"""
        if not all(expect):
            raise AssertionError(f": {expect} 不均为真")
