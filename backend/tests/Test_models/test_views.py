"""Notes:
Facility APIs are not tested - CountryField()
"""
import random
import pytest
from rest_framework.test import APIClient

from tests import factories


api_url = '/api/v1'
client = APIClient()


def test_most_downloaded_datasets(generate_datasets):
    """API most-downloaded-datasets

    1. Creates a set of dependent taxonomySearch models
    2. Creates 5 datasets
    3. Order the datasets from max downloads to min (for validation)
    4. Make an API call to query 4 most downloaded datasets
    """
    validate = sorted([[_.downloads, _.experiment_title]
                      for _ in generate_datasets(5)], key=lambda x: x[0])[::-1][:4]

    # API call
    response = client.get(f'{api_url}/most-downloaded-datasets/')

    actual = []
    for dataset in response.data:
        actual.append([
            dataset['downloads'],
            dataset['experiment_title'],
        ])

    # validate order of appearance
    assert actual == validate


def test_datasets_search(db):
    """API search-datasets
    Query filters based on experiment_title, keywords, experiment_description, pi__first_name, pi__last_name, facility__name

    1. Create several datasets that include the same keyword in different fields
    2. Query all of them
    3. Count should match
    """
    query_word = "qwerty"

    # Create more than 4 models
    # but only 4 models will have the query_word
    models = []
    factories.DatasetFactory.create()
    models.append(factories.DatasetFactory.create(
        experiment_title=f"{query_word} tests for something"
    ))
    models.append(factories.DatasetFactory.create(
        keywords=f"{query_word}, reinforced, concrete"
    ))
    models.append(factories.DatasetFactory.create(
        experiment_description=f"{query_word} doing different things for tests"
    ))
    models.append(factories.DatasetFactory.create(
        experiment_pi=[factories.PersonFactory.create(
            first_name=query_word,
        )],
        year_of_experiment=None,
    ))
    # facility = [factories.ExperimentalFacilityFactory.create(name=query_word)]
    # factories.DatasetFactory.create(experiment_facility=facility)
    factories.DatasetFactory.create()

    # expected order of appearance
    validate = sorted([[_.year_of_experiment, _.experiment_title]
                      for _ in models], key=lambda x: (x[0] is not None, x[0]), reverse=True)

    # Make an API call
    payload = {
        'query': query_word,
    }
    response = client.post(f'{api_url}/datasets/search/', payload)

    # actual order of appearance
    actual = []
    for dataset in response.data:
        actual.append([
            dataset['year_of_experiment'],
            dataset['experiment_title'],
        ])

    # must find 4 datasets
    assert len(response.data) == 4
    # validate order of appearance from recent to old
    assert actual == validate


@pytest.mark.parametrize('taxonomy_query, count', [
    ("", 10),
    ('/ST/', 3),
    ('/AA/AAA/ST/STT/', 2),
    ('/BB/AA//zz/zA/', 6),
    ('/BBBBB/AAAAAA/', 0),
])
def test_query_datasets_by_taxonomy(taxonomy_query, count, generate_datasets):
    """API query-datasets-by-taxonomy
    1. Create a taxonomy query (parametrize)
    2. Filter all datasets by an attribute (e.g., specimen-type)
    3. Filter all datasets by several attributes (e.g., specimen-sub-type as well)
    """
    # generate 10 datasets
    models = generate_datasets(10)

    if taxonomy_query != "":
        cases = random.sample(models, count)

        for case in cases:
            case.taxonomy += taxonomy_query
            case.save()

    payload = {
        'tax': taxonomy_query,
    }
    response = client.post(f'{api_url}/datasets/explore-results/', payload)

    assert len(response.data) == count


def test_get_dataset_by_id(new_dataset, generate_datasets):
    """API dataset-page
    Query a specific dataset by its ID
    """
    # create 3 datasets but query only one
    generate_datasets(2)
    response = client.get(f'{api_url}/datasets/{new_dataset.id}/')

    assert response.data['id'] == new_dataset.id


@pytest.mark.parametrize('number_of_datasets', [
    (1),
    (3),
    (0),
])
def test_get_pi_by_slug(number_of_datasets, generate_datasets, new_person):
    """API pi-page
    Query a specific PI by its slug
    """
    models = generate_datasets(number_of_datasets)

    for model in models:
        model.experiment_pi.set([new_person])

    response = client.get(f'{api_url}/people/{new_person.slug}/')
    
    assert response.data['id'] == new_person.id
    assert len(response.data['creator_datasets']) == number_of_datasets


def test_get_material_types(generate_taxonomy_strings):
    """API material-types
    Query all taxonomy strings of material types
    """
    # API does not return the list sorted, so for assertion sort here
    names = sorted([model.short_name for model in generate_taxonomy_strings['material_type']])

    response = client.get(f'{api_url}/taxonomy/get-material-types/')
    names_response = sorted([name['short_name'] for name in response.data])

    assert names == names_response


@pytest.mark.parametrize('item', [0, 1, 2])
def test_get_specific_material_type(item, generate_taxonomy_strings):
    """API material-type
    Based on selected material type, get all matching children-taxonomies
    """
    material_types = generate_taxonomy_strings['material_type']
    material = material_types[item]
    material_id = material.id
    number_of_technologies = len(material.technology.all())
    
    # make an API call and retrieve material with its children technologies
    response = client.get(f'{api_url}/taxonomy/get-material-types/{material_id}/')

    assert response.data['id'] == material_id
    assert number_of_technologies == len(response.data['technology'])


def test_get_specimen_types(generate_taxonomy_strings):
    """API specimen-types
    Get all specimen types
    """
    names = sorted([model.short_name for model in generate_taxonomy_strings['specimen_type']])

    response = client.get(f'{api_url}/taxonomy/get-specimen-types/')
    names_response = sorted([name['short_name'] for name in response.data])

    assert names == names_response


@pytest.mark.parametrize('item', [0, 1])
def test_get_specific_specimen_type(item, generate_taxonomy_strings):
    """API specimen-type
    Based on selected specimen type, get all matching children-taxonomies
    """
    specimen_types = generate_taxonomy_strings['specimen_type']
    specimen = specimen_types[item]
    specimen_id = specimen.id
    number_of_materials = len(specimen.material_type.all())
    number_of_specimen_sub_type = len(specimen.specimen_sub_type.all())
    
    # make an API call and retrieve specimen with its children
    response = client.get(f'{api_url}/taxonomy/get-specimen-types/{specimen_id}/')

    assert response.data['id'] == specimen_id
    assert number_of_materials == len(response.data['material_type'])
    assert number_of_specimen_sub_type == len(response.data['specimen_sub_type'])
    