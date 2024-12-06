#!/usr/bin/python

"""Test the classic PyGreSQL interface.

Sub-tests for large object support.

Contributed by Christoph Zwerschke.

These tests need a database to test against.
"""

import os
import tempfile
import unittest
from contextlib import suppress
from typing import Any

import pg  # the module under test

from .config import dbhost, dbname, dbpasswd, dbport, dbuser

windows = os.name == 'nt'


# noinspection PyArgumentList
def connect():
    """Create a basic pg connection to the test database."""
    connection = pg.connect(dbname, dbhost, dbport,
                            user=dbuser, passwd=dbpasswd)
    connection.query("set client_min_messages=warning")
    return connection


class TestModuleConstants(unittest.TestCase):
    """Test the existence of the documented module constants."""

    def test_large_object_int_constants(self):
        names = 'INV_READ INV_WRITE SEEK_SET SEEK_CUR SEEK_END'.split()
        for name in names:
            try:
                value = getattr(pg, name)
            except AttributeError:
                self.fail(f'Module constant {name} is missing')
            self.assertIsInstance(value, int)


class TestCreatingLargeObjects(unittest.TestCase):
    """Test creating large objects using a connection."""

    def setUp(self):
        self.c = connect()
        self.c.query('begin')

    def tearDown(self):
        self.c.query('rollback')
        self.c.close()

    def assertIsLargeObject(self, obj):  # noqa: N802
        self.assertIsNotNone(obj)
        self.assertTrue(hasattr(obj, 'open'))
        self.assertTrue(hasattr(obj, 'close'))
        self.assertTrue(hasattr(obj, 'oid'))
        self.assertTrue(hasattr(obj, 'pgcnx'))
        self.assertTrue(hasattr(obj, 'error'))
        self.assertIsInstance(obj.oid, int)
        self.assertNotEqual(obj.oid, 0)
        self.assertIs(obj.pgcnx, self.c)
        self.assertIsInstance(obj.error, str)
        self.assertFalse(obj.error)

    def test_lo_create(self):
        large_object = self.c.locreate(pg.INV_READ | pg.INV_WRITE)
        try:
            self.assertIsLargeObject(large_object)
        finally:
            del large_object

    def test_get_lo(self):
        large_object = self.c.locreate(pg.INV_READ | pg.INV_WRITE)
        try:
            self.assertIsLargeObject(large_object)
            oid = large_object.oid
        finally:
            del large_object
        data = b'some data to be shared'
        large_object = self.c.getlo(oid)
        try:
            self.assertIsLargeObject(large_object)
            self.assertEqual(large_object.oid, oid)
            large_object.open(pg.INV_WRITE)
            large_object.write(data)
            large_object.close()
        finally:
            del large_object
        large_object = self.c.getlo(oid)
        try:
            self.assertIsLargeObject(large_object)
            self.assertEqual(large_object.oid, oid)
            large_object.open(pg.INV_READ)
            r = large_object.read(80)
            large_object.close()
            large_object.unlink()
        finally:
            del large_object
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, data)

    def test_lo_import(self):
        f : Any
        if windows:
            # NamedTemporaryFiles don't work well here
            fname = 'temp_test_pg_largeobj_import.txt'
            f = open(fname, 'wb')  # noqa: SIM115
        else:
            f = tempfile.NamedTemporaryFile()  # noqa: SIM115
            fname = f.name
        data = b'some data to be imported'
        f.write(data)
        if windows:
            f.close()
            f = open(fname, 'rb')  # noqa: SIM115
        else:
            f.flush()
            f.seek(0)
        large_object = self.c.loimport(f.name)
        try:
            f.close()
            if windows:
                os.remove(fname)
            self.assertIsLargeObject(large_object)
            large_object.open(pg.INV_READ)
            large_object.seek(0, pg.SEEK_SET)
            r = large_object.size()
            self.assertIsInstance(r, int)
            self.assertEqual(r, len(data))
            r = large_object.read(80)
            self.assertIsInstance(r, bytes)
            self.assertEqual(r, data)
            large_object.close()
            large_object.unlink()
        finally:
            del large_object


class TestLargeObjects(unittest.TestCase):
    """Test the large object methods."""

    def setUp(self):
        self.pgcnx = connect()
        self.pgcnx.query('begin')
        self.obj = self.pgcnx.locreate(pg.INV_READ | pg.INV_WRITE)

    def tearDown(self):
        if self.obj.oid:
            with suppress(SystemError, OSError):
                self.obj.close()
            with suppress(SystemError, OSError):
                self.obj.unlink()
        del self.obj
        with suppress(SystemError):
            self.pgcnx.query('rollback')
        self.pgcnx.close()

    def test_class_name(self):
        self.assertEqual(self.obj.__class__.__name__, 'LargeObject')

    def test_module_name(self):
        self.assertEqual(self.obj.__class__.__module__, 'pg')

    def test_oid(self):
        self.assertIsInstance(self.obj.oid, int)
        self.assertNotEqual(self.obj.oid, 0)

    def test_pgcn(self):
        self.assertIs(self.obj.pgcnx, self.pgcnx)

    def test_error(self):
        self.assertIsInstance(self.obj.error, str)
        self.assertEqual(self.obj.error, '')

    def test_str(self):
        self.obj.open(pg.INV_WRITE)
        data = b'some object to be printed'
        self.obj.write(data)
        oid = self.obj.oid
        r = str(self.obj)
        self.assertEqual(r, f'Opened large object, oid {oid}')
        self.obj.close()
        r = str(self.obj)
        self.assertEqual(r, f'Closed large object, oid {oid}')

    def test_repr(self):
        r = repr(self.obj)
        self.assertTrue(r.startswith('<pg.LargeObject object'), r)

    def test_open(self):
        # noinspection PyShadowingBuiltins
        open = self.obj.open
        # testing with invalid parameters
        self.assertRaises(TypeError, open)
        self.assertRaises(TypeError, open, pg.INV_READ, pg.INV_WRITE)
        open(pg.INV_READ)
        # object is already open
        self.assertRaises(IOError, open, pg.INV_READ)

    def test_close(self):
        close = self.obj.close
        # testing with invalid parameters
        self.assertRaises(TypeError, close, pg.INV_READ)
        # object is not yet open
        self.assertRaises(IOError, close)
        self.obj.open(pg.INV_READ)
        close()
        self.assertRaises(IOError, close)

    def test_read(self):
        read = self.obj.read
        # testing with invalid parameters
        self.assertRaises(TypeError, read)
        self.assertRaises(ValueError, read, -1)
        self.assertRaises(TypeError, read, 'invalid')
        self.assertRaises(TypeError, read, 80, 'invalid')
        # reading when object is not yet open
        self.assertRaises(IOError, read, 80)
        data = b'some data to be read'
        self.obj.open(pg.INV_WRITE)
        self.obj.write(data)
        self.obj.close()
        self.obj.open(pg.INV_READ)
        r = read(80)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, data)
        self.obj.close()
        self.obj.open(pg.INV_READ)
        r = read(8)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, data[:8])
        self.obj.close()

    def test_write(self):
        write = self.obj.write
        # testing with invalid parameters
        self.assertRaises(TypeError, write)
        self.assertRaises(TypeError, write, -1)
        self.assertRaises(TypeError, write, '', 'invalid')
        # writing when object is not yet open
        self.assertRaises(IOError, write, 'invalid')
        data = b'some data to be written'
        self.obj.open(pg.INV_WRITE)
        write(data)
        self.obj.close()
        self.obj.open(pg.INV_READ)
        r = self.obj.read(80)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, data)

    def test_write_latin1_bytes(self):
        read = self.obj.read
        self.obj.open(pg.INV_WRITE)
        self.obj.write('käse'.encode('latin1'))
        self.obj.close()
        self.obj.open(pg.INV_READ)
        r = read(80)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r.decode('latin1'), 'käse')

    def test_write_utf8_bytes(self):
        read = self.obj.read
        self.obj.open(pg.INV_WRITE)
        self.obj.write('käse'.encode())
        self.obj.close()
        self.obj.open(pg.INV_READ)
        r = read(80)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r.decode(), 'käse')

    def test_write_utf8_string(self):
        read = self.obj.read
        self.obj.open(pg.INV_WRITE)
        self.obj.write('käse')
        self.obj.close()
        self.obj.open(pg.INV_READ)
        r = read(80)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r.decode(), 'käse')

    def test_seek(self):
        seek = self.obj.seek
        # testing with invalid parameters
        self.assertRaises(TypeError, seek)
        self.assertRaises(TypeError, seek, 0)
        self.assertRaises(TypeError, seek, 0, pg.SEEK_SET, pg.SEEK_END)
        self.assertRaises(TypeError, seek, 'invalid', pg.SEEK_SET)
        self.assertRaises(TypeError, seek, 0, 'invalid')
        # seeking when object is not yet open
        self.assertRaises(IOError, seek, 0, pg.SEEK_SET)
        data = b'some data to be seeked'
        self.obj.open(pg.INV_WRITE)
        self.obj.write(data)
        self.obj.close()
        self.obj.open(pg.INV_READ)
        seek(0, pg.SEEK_SET)
        r = self.obj.read(9)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, b'some data')
        seek(4, pg.SEEK_CUR)
        r = self.obj.read(2)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, b'be')
        seek(-10, pg.SEEK_CUR)
        r = self.obj.read(4)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, b'data')
        seek(0, pg.SEEK_SET)
        r = self.obj.read(4)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, b'some')
        seek(-6, pg.SEEK_END)
        r = self.obj.read(4)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, b'seek')

    def test_tell(self):
        tell = self.obj.tell
        # testing with invalid parameters
        self.assertRaises(TypeError, tell, 0)
        # telling when object is not yet open
        self.assertRaises(IOError, tell)
        data = b'some story to be told'
        self.obj.open(pg.INV_WRITE)
        self.obj.write(data)
        r = tell()
        self.assertIsInstance(r, int)
        self.assertEqual(r, len(data))
        self.obj.close()
        self.obj.open(pg.INV_READ)
        r = tell()
        self.assertIsInstance(r, int)
        self.assertEqual(r, 0)
        self.obj.seek(5, pg.SEEK_SET)
        r = tell()
        self.assertIsInstance(r, int)
        self.assertEqual(r, 5)

    def test_unlink(self):
        unlink = self.obj.unlink
        # testing with invalid parameters
        self.assertRaises(TypeError, unlink, 0)
        # unlinking when object is still open
        self.obj.open(pg.INV_WRITE)
        self.assertIsNotNone(self.obj.oid)
        self.assertNotEqual(0, self.obj.oid)
        self.assertRaises(IOError, unlink)
        data = b'some data to be sold'
        self.obj.write(data)
        self.obj.close()
        # unlinking after object has been closed
        unlink()
        self.assertIsNone(self.obj.oid)
        # unlinking after object has been already unlinked
        self.assertRaises(pg.IntegrityError, unlink)

    def test_unlink_inexistent(self):
        unlink = self.obj.unlink
        self.obj.open(pg.INV_WRITE)
        self.obj.close()
        self.pgcnx.query(f'select lo_unlink({self.obj.oid})')
        self.assertRaises(IOError, unlink)

    def test_size(self):
        size = self.obj.size
        # testing with invalid parameters
        self.assertRaises(TypeError, size, 0)
        # sizing when object is not yet open
        self.assertRaises(IOError, size)
        # sizing an empty object
        self.obj.open(pg.INV_READ)
        r = size()
        self.obj.close()
        self.assertIsInstance(r, int)
        self.assertEqual(r, 0)
        # sizing after adding some data
        data = b'some data to be sized'
        self.obj.open(pg.INV_WRITE)
        self.obj.write(data)
        self.obj.close()
        # sizing when current position is zero
        self.obj.open(pg.INV_READ)
        r = size()
        self.obj.close()
        self.assertIsInstance(r, int)
        self.assertEqual(r, len(data))
        self.obj.open(pg.INV_READ)
        # sizing when current position is not zero
        self.obj.seek(5, pg.SEEK_SET)
        r = size()
        self.obj.close()
        self.assertIsInstance(r, int)
        self.assertEqual(r, len(data))
        # sizing after adding more data
        data += b' and more data'
        self.obj.open(pg.INV_WRITE)
        self.obj.write(data)
        self.obj.close()
        self.obj.open(pg.INV_READ)
        r = size()
        self.obj.close()
        self.assertIsInstance(r, int)
        self.assertEqual(r, len(data))

    def test_export(self):
        export = self.obj.export
        # testing with invalid parameters
        self.assertRaises(TypeError, export)
        self.assertRaises(TypeError, export, 0)
        self.assertRaises(TypeError, export, 'invalid', 0)
        f: Any
        if windows:
            # NamedTemporaryFiles don't work well here
            fname = 'temp_test_pg_largeobj_export.txt'
            f = open(fname, 'wb')  # noqa: SIM115
        else:
            f = tempfile.NamedTemporaryFile()  # noqa: SIM115
            fname = f.name
        data = b'some data to be exported'
        self.obj.open(pg.INV_WRITE)
        self.obj.write(data)
        # exporting when object is not yet closed
        self.assertRaises(IOError, export, f.name)
        self.obj.close()
        export(fname)
        if windows:
            f.close()
            f = open(fname, 'rb')  # noqa: SIM115
        r = f.read()
        f.close()
        if windows:
            os.remove(fname)
        self.assertIsInstance(r, bytes)
        self.assertEqual(r, data)

    def test_export_in_existent(self):
        export = self.obj.export
        with tempfile.NamedTemporaryFile() as f:
            self.obj.open(pg.INV_WRITE)
            self.obj.close()
            self.pgcnx.query(f'select lo_unlink({self.obj.oid})')
            self.assertRaises(IOError, export, f.name)


if __name__ == '__main__':
    unittest.main()
