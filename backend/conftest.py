"""Running tests
scope
    function    run once per test
    class       run once per class of tests
    module      run once per module
    session     run once per session

"""
import pytest

from tests.factories import *


@pytest.fixture
def generate_datasets(db):
    def _method(n):
        return DatasetFactory.create_batch(n)
    
    return _method


@pytest.fixture
def generate_taxonomy_strings(db, specimen_sub_type_factory, material_technology_factory, 
                              type_material_factory, specimen_type_factory):
    
    models = {
        "specimen_sub_type": [],
        "material_technology": [],
        "material_type": [],
        "specimen_type": [],
    }

    models['specimen_sub_type'] = specimen_sub_type_factory.create_batch(size=4)
    models['material_technology'] = material_technology_factory.create_batch(size=5)

    for i in range(3):
        if i == 0:
            technologies = models['material_technology'][:2]
        elif i == 1:
            technologies = models['material_technology'][:3]
        else:
            technologies = models['material_technology']

        models['material_type'].append(
            type_material_factory.create(technology=technologies))
        
    for i in range(2):
        if i == 0:
            specimen_sub_types = models['specimen_sub_type'][:1]
            material_types = models['material_type'][:1]
        else:
            specimen_sub_types = models['specimen_sub_type'][1:]
            material_types = models['material_type'][1:]
            
        models['specimen_type'].append(
            specimen_type_factory.create(
                specimen_sub_type=specimen_sub_types,
                material_type=material_types,
            )
        )

    return models


@pytest.fixture
def new_affiliation(db, affiliation_factory):
    model = affiliation_factory.create()
    return model


@pytest.fixture
def new_person(db, person_factory, affiliation_factory):
    affiliation1 = affiliation_factory.create()
    model = person_factory.create(affiliation=[affiliation1])
    return model


@pytest.fixture
def new_experimental_facility(db, experimental_facility_factory):
    model = experimental_facility_factory.create()
    return model


@pytest.fixture
def new_discipline(db, engineering_discipline_factory):
    model = engineering_discipline_factory.create()
    return model


@pytest.fixture
def new_experiment_type(db, experiment_type_factory):
    model = experiment_type_factory.create()
    return model


@pytest.fixture
def new_experiment_scale(db, experiment_scale_factory):
    model = experiment_scale_factory.create()
    return model


@pytest.fixture
def new_license(db, license_factory):
    model = license_factory.create()
    return model


@pytest.fixture
def new_dataset(db, dataset_factory):
    model = dataset_factory.create()
    return model


@pytest.fixture
def new_specimen_sub_type(db, specimen_sub_type_factory):
    model = specimen_sub_type_factory.create()
    return model


@pytest.fixture
def new_material_technology(db, material_technology_factory):
    model = material_technology_factory.create()
    return model


@pytest.fixture
def new_material_type(db, type_material_factory):
    model = type_material_factory.create()
    return model


@pytest.fixture
def new_specimen_type(db, specimen_type_factory):
    model = specimen_type_factory.create()
    return model
