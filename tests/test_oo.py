import unittest
import os
import tempfile
from typing import Any
from hypothesis import given, settings, strategies as st
from paprika import data, NonNull, singleton, serial
class OOTestCases(unittest.TestCase):
    @data
    class TestClass:
        field1: NonNull[int]
        field2: str

    @singleton
    class TestSingleton:
        field1: str

    def test_nonnull(self):
        self.assertRaises(
            ValueError, self.TestClass, None, {"field1": None, "field2": "test"}
        )

    def test_to_string(self):
        self.assertEqual(
            str(self.TestClass(field1=42, field2="test")),
            "TestClass@[field1=42, field2=test]",
        )

    def test_eq(self):
        t1 = self.TestClass(field1=42, field2="test")
        t2 = self.TestClass(field1=42, field2="test")
        self.assertEqual(t1, t2)

    def test_hash(self):
        t1 = self.TestClass(field1=42, field2="test")
        t2 = self.TestClass(field1=42, field2="test")
        self.assertEqual(hash(t1), hash(t2))

    def test_singleton(self):
        s1 = self.TestSingleton(field1="test")
        s2 = self.TestSingleton()
        self.assertEqual(s1, s2)

    @data
    @serial
    class TestSerialClass:
        field1: Any

    @given(st.binary())
    @settings(max_examples=10)
    def test_serial(self, b):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file_path = os.path.join(tmp_dir, 'data.pickle')

            c = self.TestSerialClass(b)
            c.__dump__(tmp_file_path)
            deserialized = self.TestSerialClass.__load__(tmp_file_path)

            self.assertEqual(deserialized, c)
            
    @data
    @serial(protocol=3)
    class TestSerialClassProtocol3:
        field1: Any
        
    @given(st.binary())
    @settings(max_examples=10)
    def test_serial_protocol_4(self, b):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file_path = os.path.join(tmp_dir, 'data.pickle')

            c = self.TestSerialClassProtocol3(b)
            c.__dump__(tmp_file_path)
            deserialized = self.TestSerialClassProtocol3.__load__(tmp_file_path)

            self.assertEqual(deserialized, c)
