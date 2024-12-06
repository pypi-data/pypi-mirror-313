from .clienttestcase import ClientTestCase as ClientTestCase_, fixtures
from heaserver.service import client
from heaobject.registry import Component
from heaobject.organization import Organization


class ClientTestCase(ClientTestCase_):

    def setUp(self) -> None:
        super().setUp()
        self.c = Component()
        self.c.from_dict(fixtures['components'][0])

    async def test_get_no_component(self):
        self.assertEqual(None, await client.get_component(self.app, Organization.get_type_name()))

    async def test_get_component(self):
        self.assertEqual(self.c, await client.get_component(self.app, self.c.resources[0].resource_type_name))

    async def test_get_no_resource_url(self):
        self.assertEqual(None, await client.get_resource_url(self.app, Organization.get_type_name()))

    async def test_get_resource_url(self):
        self.assertEqual('http://localhost/foo/folders', await client.get_resource_url(self.app, self.c.resources[0].resource_type_name))
