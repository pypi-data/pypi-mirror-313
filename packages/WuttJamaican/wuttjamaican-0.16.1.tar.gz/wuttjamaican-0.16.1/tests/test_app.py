# -*- coding: utf-8; -*-

import os
import shutil
import sys
import tempfile
import warnings
import uuid as _uuid
from unittest import TestCase
from unittest.mock import patch, MagicMock

import pytest
from mako.template import Template

import wuttjamaican.enum
from wuttjamaican import app as mod
from wuttjamaican.progress import ProgressBase
from wuttjamaican.conf import WuttaConfig
from wuttjamaican.util import UNSPECIFIED
from wuttjamaican.testing import FileTestCase


class TestAppHandler(FileTestCase):

    def setUp(self):
        self.setup_files()
        self.config = WuttaConfig(appname='wuttatest')
        self.app = mod.AppHandler(self.config)
        self.config.app = self.app

    def test_init(self):
        self.assertIs(self.app.config, self.config)
        self.assertEqual(self.app.handlers, {})
        self.assertEqual(self.app.appname, 'wuttatest')

    def test_get_enum(self):
        self.assertIs(self.app.get_enum(), wuttjamaican.enum)

    def test_load_object(self):

        # just confirm the method works on a basic level; the
        # underlying function is tested elsewhere
        obj = self.app.load_object('wuttjamaican.util:UNSPECIFIED')
        self.assertIs(obj, UNSPECIFIED)

    def test_get_appdir(self):

        mockdir = self.mkdir('mockdir')

        # default appdir
        with patch.object(sys, 'prefix', new=mockdir):

            # default is returned by default
            appdir = self.app.get_appdir()
            self.assertEqual(appdir, os.path.join(mockdir, 'app'))

            # but not if caller wants config only
            appdir = self.app.get_appdir(configured_only=True)
            self.assertIsNone(appdir)

            # also, cannot create if appdir path not known
            self.assertRaises(ValueError, self.app.get_appdir, configured_only=True, create=True)

        # configured appdir
        self.config.setdefault('wuttatest.appdir', mockdir)
        appdir = self.app.get_appdir()
        self.assertEqual(appdir, mockdir)

        # appdir w/ subpath
        appdir = self.app.get_appdir('foo', 'bar')
        self.assertEqual(appdir, os.path.join(mockdir, 'foo', 'bar'))

        # subpath is created
        self.assertEqual(len(os.listdir(mockdir)), 0)
        appdir = self.app.get_appdir('foo', 'bar', create=True)
        self.assertEqual(appdir, os.path.join(mockdir, 'foo', 'bar'))
        self.assertEqual(os.listdir(mockdir), ['foo'])
        self.assertEqual(os.listdir(os.path.join(mockdir, 'foo')), ['bar'])

    def test_make_appdir(self):

        # appdir is created, and 3 subfolders added by default
        tempdir = tempfile.mkdtemp()
        appdir = os.path.join(tempdir, 'app')
        self.assertFalse(os.path.exists(appdir))
        self.app.make_appdir(appdir)
        self.assertTrue(os.path.exists(appdir))
        self.assertEqual(len(os.listdir(appdir)), 4)
        shutil.rmtree(tempdir)

        # subfolders still added if appdir already exists
        tempdir = tempfile.mkdtemp()
        self.assertTrue(os.path.exists(tempdir))
        self.assertEqual(len(os.listdir(tempdir)), 0)
        self.app.make_appdir(tempdir)
        self.assertEqual(len(os.listdir(tempdir)), 4)
        shutil.rmtree(tempdir)

    def test_render_mako_template(self):
        output_conf = self.write_file('output.conf', '')
        template = Template("""\
[wutta]
app_title = WuttaTest
""")
        output = self.app.render_mako_template(template, {}, output_path=output_conf)
        self.assertEqual(output, """\
[wutta]
app_title = WuttaTest
""")

        with open(output_conf, 'rt') as f:
            self.assertEqual(f.read(), output)

    def test_resource_path(self):
        result = self.app.resource_path('wuttjamaican:templates')
        self.assertEqual(result, os.path.join(os.path.dirname(mod.__file__), 'templates'))

    def test_make_session(self):
        try:
            from wuttjamaican import db
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        session = self.app.make_session()
        self.assertIsInstance(session, db.Session.class_)

    def test_short_session(self):
        short_session = MagicMock()
        mockdb = MagicMock(short_session=short_session)

        with patch.dict('sys.modules', **{'wuttjamaican.db': mockdb}):

            with self.app.short_session(foo='bar') as s:
                short_session.assert_called_once_with(
                    foo='bar', factory=self.app.make_session)

    def test_get_setting(self):
        try:
            import sqlalchemy as sa
            from sqlalchemy import orm
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        Session = orm.sessionmaker()
        engine = sa.create_engine('sqlite://')
        session = Session(bind=engine)
        session.execute(sa.text("""
        create table setting (
                name varchar(255) primary key,
                value text
        );
        """))
        session.commit()

        value = self.app.get_setting(session, 'foo')
        self.assertIsNone(value)

        session.execute(sa.text("insert into setting values ('foo', 'bar');"))
        value = self.app.get_setting(session, 'foo')
        self.assertEqual(value, 'bar')

    def test_save_setting(self):
        try:
            import sqlalchemy as sa
            from sqlalchemy import orm
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        Session = orm.sessionmaker()
        engine = sa.create_engine('sqlite://')
        session = Session(bind=engine)
        session.execute(sa.text("""
        create table setting (
                name varchar(255) primary key,
                value text
        );
        """))
        session.commit()

        # value null by default
        value = self.app.get_setting(session, 'foo')
        self.assertIsNone(value)

        # unless we save a value
        self.app.save_setting(session, 'foo', '1')
        session.commit()
        value = self.app.get_setting(session, 'foo')
        self.assertEqual(value, '1')

    def test_delete_setting(self):
        try:
            import sqlalchemy as sa
            from sqlalchemy import orm
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        Session = orm.sessionmaker()
        engine = sa.create_engine('sqlite://')
        session = Session(bind=engine)
        session.execute(sa.text("""
        create table setting (
                name varchar(255) primary key,
                value text
        );
        """))
        session.commit()

        # value null by default
        value = self.app.get_setting(session, 'foo')
        self.assertIsNone(value)

        # unless we save a value
        self.app.save_setting(session, 'foo', '1')
        session.commit()
        value = self.app.get_setting(session, 'foo')
        self.assertEqual(value, '1')

        # but then if we delete it, should be null again
        self.app.delete_setting(session, 'foo')
        session.commit()
        value = self.app.get_setting(session, 'foo')
        self.assertIsNone(value)

    def test_continuum_is_enabled(self):

        # false by default
        with patch.object(self.app, 'providers', new={}):
            self.assertFalse(self.app.continuum_is_enabled())

        # but "any" provider technically could enable it...
        class MockProvider:
            def continuum_is_enabled(self):
                return True
        with patch.object(self.app, 'providers', new={'mock': MockProvider()}):
            self.assertTrue(self.app.continuum_is_enabled())

    def test_model(self):
        try:
            from wuttjamaican.db import model
        except ImportError:
            pytest.skip("test not relevant without sqlalchemy")

        self.assertNotIn('model', self.app.__dict__)
        self.assertIs(self.app.model, model)

    def test_get_model(self):
        try:
            from wuttjamaican.db import model
        except ImportError:
            pytest.skip("test not relevant without sqlalchemy")

        self.assertIs(self.app.get_model(), model)

    def test_get_title(self):
        self.assertEqual(self.app.get_title(), 'WuttJamaican')

    def test_get_node_title(self):

        # default
        self.assertEqual(self.app.get_node_title(), 'WuttJamaican')

        # will fallback to app title
        self.config.setdefault('wuttatest.app_title', "WuttaTest")
        self.assertEqual(self.app.get_node_title(), 'WuttaTest')

        # will read from config
        self.config.setdefault('wuttatest.node_title', "WuttaNode")
        self.assertEqual(self.app.get_node_title(), 'WuttaNode')

    def test_get_node_type(self):

        # default
        self.assertIsNone(self.app.get_node_type())

        # will read from config
        self.config.setdefault('wuttatest.node_type', 'warehouse')
        self.assertEqual(self.app.get_node_type(), 'warehouse')

    def test_get_distribution(self):

        try:
            from sqlalchemy.orm import Query
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        # works with "non-native" objects
        query = Query({})
        dist = self.app.get_distribution(query)
        self.assertEqual(dist, 'SQLAlchemy')

        # can override dist via config
        self.config.setdefault('wuttatest.app_dist', 'importlib_metadata')
        dist = self.app.get_distribution()
        self.assertEqual(dist, 'importlib_metadata')

        # but the provided object takes precedence
        dist = self.app.get_distribution(query)
        self.assertEqual(dist, 'SQLAlchemy')

    def test_get_distribution_pre_python_3_10(self):

        # the goal here is to get coverage for code which would only
        # run on python 3,9 and older, but we only need that coverage
        # if we are currently testing python 3.10+
        if sys.version_info.major == 3 and sys.version_info.minor < 10:
            pytest.skip("this test is not relevant before python 3.10")

        importlib_metadata = MagicMock()
        importlib_metadata.packages_distributions = MagicMock(
            return_value={
                'wuttjamaican': ['WuttJamaican'],
                'config': ['python-configuration'],
            })

        orig_import = __import__

        def mock_import(name, *args, **kwargs):
            if name == 'importlib.metadata':
                raise ImportError
            if name == 'importlib_metadata':
                return importlib_metadata
            return orig_import(name, *args, **kwargs)

        with patch('builtins.__import__', side_effect=mock_import):

            # default should always be WuttJamaican (right..?)
            dist = self.app.get_distribution()
            self.assertEqual(dist, 'WuttJamaican')

            # also works with "non-native" objects
            from config import Configuration
            config = Configuration({})
            dist = self.app.get_distribution(config)
            self.assertEqual(dist, 'python-configuration')

            # hacky sort of test, just in case we can't deduce the
            # package dist based on the obj - easy enough since we
            # have limited the packages_distributions() above
            dist = self.app.get_distribution(42)
            self.assertIsNone(dist)

            # can override dist via config
            self.config.setdefault('wuttatest.app_dist', 'importlib_metadata')
            dist = self.app.get_distribution()
            self.assertEqual(dist, 'importlib_metadata')

            # but the provided object takes precedence
            dist = self.app.get_distribution(config)
            self.assertEqual(dist, 'python-configuration')

            # hacky test again, this time config override should win
            dist = self.app.get_distribution(42)
            self.assertEqual(dist, 'importlib_metadata')

    def test_get_version(self):
        from importlib.metadata import version

        try:
            from sqlalchemy.orm import Query
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        # works with "non-native" objects
        query = Query({})
        ver = self.app.get_version(obj=query)
        self.assertEqual(ver, version('SQLAlchemy'))

        # can override dist via config
        self.config.setdefault('wuttatest.app_dist', 'python-configuration')
        ver = self.app.get_version()
        self.assertEqual(ver, version('python-configuration'))

        # but the provided object takes precedence
        ver = self.app.get_version(obj=query)
        self.assertEqual(ver, version('SQLAlchemy'))

        # can also specify the dist
        ver = self.app.get_version(dist='passlib')
        self.assertEqual(ver, version('passlib'))

    def test_make_title(self):
        text = self.app.make_title('foo_bar')
        self.assertEqual(text, "Foo Bar")

    def test_make_uuid(self):
        uuid = self.app.make_uuid()
        self.assertEqual(len(uuid), 32)

    def test_make_true_uuid(self):
        uuid = self.app.make_true_uuid()
        self.assertIsInstance(uuid, _uuid.UUID)

    def test_progress_loop(self):

        def act(obj, i):
            pass

        # with progress
        self.app.progress_loop(act, [1, 2, 3], ProgressBase,
                               message="whatever")

        # without progress
        self.app.progress_loop(act, [1, 2, 3], None,
                               message="whatever")

    def test_get_session(self):
        try:
            import sqlalchemy as sa
            from sqlalchemy import orm
        except ImportError:
            pytest.skip("test not relevant without sqlalchemy")

        model = self.app.model
        user = model.User()
        self.assertIsNone(self.app.get_session(user))

        Session = orm.sessionmaker()
        engine = sa.create_engine('sqlite://')
        mysession = Session(bind=engine)
        mysession.add(user)
        session = self.app.get_session(user)
        self.assertIs(session, mysession)

    def test_get_person(self):
        people = self.app.get_people_handler()
        with patch.object(people, 'get_person') as get_person:
            get_person.return_value = 'foo'
            person = self.app.get_person('bar')
            get_person.assert_called_once_with('bar')
            self.assertEqual(person, 'foo')

    def test_get_auth_handler(self):
        from wuttjamaican.auth import AuthHandler

        auth = self.app.get_auth_handler()
        self.assertIsInstance(auth, AuthHandler)

    def test_get_email_handler(self):
        from wuttjamaican.email import EmailHandler

        mail = self.app.get_email_handler()
        self.assertIsInstance(mail, EmailHandler)

    def test_get_install_handler(self):
        from wuttjamaican.install import InstallHandler

        install = self.app.get_install_handler()
        self.assertIsInstance(install, InstallHandler)

    def test_get_people_handler(self):
        from wuttjamaican.people import PeopleHandler

        people = self.app.get_people_handler()
        self.assertIsInstance(people, PeopleHandler)

    def test_send_email(self):
        from wuttjamaican.email import EmailHandler

        with patch.object(EmailHandler, 'send_email') as send_email:
            self.app.send_email('foo')
            send_email.assert_called_once_with('foo')


class TestAppProvider(TestCase):

    def setUp(self):
        self.config = WuttaConfig(appname='wuttatest')
        self.app = mod.AppHandler(self.config)
        self.config._app = self.app

    def test_constructor(self):

        # config object is expected
        provider = mod.AppProvider(self.config)
        self.assertIs(provider.config, self.config)
        self.assertIs(provider.app, self.app)
        self.assertEqual(provider.appname, 'wuttatest')

        # but can pass app handler instead
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            provider = mod.AppProvider(self.app)
        self.assertIs(provider.config, self.config)
        self.assertIs(provider.app, self.app)

    def test_get_all_providers(self):

        class FakeProvider(mod.AppProvider):
            pass

        # nb. we specify *classes* here
        fake_providers = {'fake': FakeProvider}

        with patch('wuttjamaican.app.load_entry_points') as load_entry_points:
            load_entry_points.return_value = fake_providers

            # sanity check, we get *instances* back from this
            providers = self.app.get_all_providers()
            load_entry_points.assert_called_once_with('wutta.app.providers')
            self.assertEqual(len(providers), 1)
            self.assertIn('fake', providers)
            self.assertIsInstance(providers['fake'], FakeProvider)

    def test_hasattr(self):

        class FakeProvider(mod.AppProvider):
            def fake_foo(self):
                pass

        self.app.providers = {'fake': FakeProvider(self.config)}

        self.assertTrue(hasattr(self.app, 'fake_foo'))
        self.assertFalse(hasattr(self.app, 'fake_method_does_not_exist'))

    def test_getattr(self):

        # enum
        self.assertNotIn('enum', self.app.__dict__)
        self.assertIs(self.app.enum, wuttjamaican.enum)

        # now we test that providers are loaded...

        class FakeProvider(mod.AppProvider):
            def fake_foo(self):
                return 42

        # nb. using instances here
        fake_providers = {'fake': FakeProvider(self.config)}

        with patch.object(self.app, 'get_all_providers') as get_all_providers:
            get_all_providers.return_value = fake_providers

            self.assertNotIn('providers', self.app.__dict__)
            self.assertIs(self.app.providers, fake_providers)
            get_all_providers.assert_called_once_with()

    def test_getattr_model(self):
        try:
            import wuttjamaican.db.model
        except ImportError:
            pytest.skip("test not relevant without sqlalchemy")

        # model
        self.assertNotIn('model', self.app.__dict__)
        self.assertIs(self.app.model, wuttjamaican.db.model)

    def test_getattr_providers(self):

        # collection of providers is loaded on demand
        self.assertNotIn('providers', self.app.__dict__)
        self.assertIsNotNone(self.app.providers)

        # custom attr does not exist yet
        self.assertRaises(AttributeError, getattr, self.app, 'foo_value')

        # but provider can supply the attr
        self.app.providers['mytest'] = MagicMock(foo_value='bar')
        self.assertEqual(self.app.foo_value, 'bar')


class TestGenericHandler(TestCase):

    def setUp(self):
        self.config = WuttaConfig(appname='wuttatest')
        self.app = mod.AppHandler(self.config)
        self.config._app = self.app

    def test_constructor(self):
        handler = mod.GenericHandler(self.config)
        self.assertIs(handler.config, self.config)
        self.assertIs(handler.app, self.app)
        self.assertEqual(handler.appname, 'wuttatest')
