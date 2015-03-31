from tastypie.test import ResourceTestCase


class ProteinApiTest(ResourceTestCase):
    """Tests for the /protein/ API endpoint."""

    fixtures = ['protein.json']

    def setup(self):
        """Setup basic view client."""
        super(ProteinApiTest, self).setup()

    def test_protein_api_is_JSON(self):
        """Assert that the protein API is displayed as a JSON dictionary."""
        resp = self.api_client.get('/api/v1/protein/', format='json')
        self.assertValidJSONResponse(resp)

    def test_protein_list_has_objects(self):
        """Assert that user json has 5 protein objects."""
        resp = self.api_client.get('/api/v1/protein/')
        records = self.deserialize(resp)['objects']
        self.assertEqual(len(records), 5)

    def test_protein_has_expected_data(self):
        """
        Assert that a protein object displays data for id, name, resource_uri,
        and sequence.
        """
        resp = self.api_client.get('/api/v1/protein/')
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            "id": 6,
            "name": "cytochrome c oxidase subunit 4 isoform 1",
            "resource_uri": "/api/v1/protein/6/",
            "sequence": "MLATRVFSLVGKRAISTSVCVRAHESVVKSEDFSLPAYMDRRDHPLPEVAHVKHLSASQKALKEKEKASWSSLSMDEKVELYRIKFKESFAEMNRGSNEWKTVVGGAMFFIGFTALVIMWQKHYVYGPLPQSFDKEWVAKQTKRMLDMKVNPIQGLASKWDYEKNEWKK"
            })


class GlossaryApiTest(ResourceTestCase):
    """Tests for the 'api/v1/glossary/' endpoint."""

    fixtures = ['glossary.json']

    def setup(self):
        """Setup basic view client."""
        super(GlossaryApiTest, self).setup()

    def test_glossary_api_is_JSON(self):
        """Assert that the glossary API is displayed as a JSON dictionary."""
        resp = self.api_client.get('/api/v1/glossary/', format='json')
        self.assertValidJSONResponse(resp)

    def test_glossary_list_has_objects(self):
        """Assert that json has one glossary object."""
        resp = self.api_client.get('/api/v1/glossary/')
        records = self.deserialize(resp)['objects']
        self.assertEqual(len(records), 1)

    def test_glossary_object_has_expected_data(self):
        """
        Assert that glossary object displays data for id, term, definition,
        resource_uri, and reference.
        """
        resp = self.api_client.get('/api/v1/glossary/')
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            "id": 1,
            "term": "protein",
            "definition": "globular string of amino acids",
            "reference": "my butt",
            "resource_uri": "/api/v1/glossary/1/"
            })
