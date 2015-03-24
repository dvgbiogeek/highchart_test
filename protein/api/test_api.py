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
        """Assert that user json has 6 protein objects."""
        resp = self.api_client.get('/api/v1/protein/')
        records = self.deserialize(resp)['objects']
        self.assertEqual(len(records), 6)

    def test_protein_has_expected_data(self):
        """
        Assert that a protein object displays data for id, name, resource_uri,
        and sequence.
        """
        resp = self.api_client.get('/api/v1/protein/')
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            "id": 1,
            "name": "cytochrome c",
            "resource_uri": "/api/v1/protein/1/",
            "sequence": "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLE\r\nNPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"
            })
